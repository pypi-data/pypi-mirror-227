import json
import time

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Dict, Iterator, List, Optional

from packaging.version import Version

from vmray.rest_api import VMRayRESTAPI
from vmray.rest_api.version import __version__


DEFAULT_USER_AGENT = f"VMRayIntegrationKit/{__version__}"


class VMRayAPIWrapper(VMRayRESTAPI):
    def __init__(self, server: str, api_key: str,
                 verify_cert: bool = True, connector_name: Optional[str] = None):
        super().__init__(server, api_key, verify_cert=verify_cert, connector_name=connector_name)

    def system_info(self) -> Dict[str, Any]:
        return self.call("GET", "/rest/system_info")

    def get_platform_version(self) -> Version:
        system_info = self.system_info()
        return Version(system_info["version"])

    def get_analyses_by_submission_id(self, submission_id: int) -> List[Dict[str, Any]]:
        return self.call("GET", f"/rest/analysis?analysis_submission_id={submission_id}")

    def get_report(self, analysis_id: int) -> BinaryIO:
        return self.call(
            "GET",
            f"/rest/analysis/{analysis_id}/archive/logs/summary_v2.json",
            raw_data=True
        )

    def get_analysis_screenshots(self, analysis_id: int) -> BinaryIO:
        """Get the screenshots for a given analysis ID.

           This function is only available on VMRay Platform Server 2023.4.0 and
           later.
        """
        return self.call(
            "GET",
            f"/rest/analysis/{analysis_id}/archive/screenshots",
            raw_data=True
        )

    def get_vtis_by_sample_id(self, sample_id: int) -> Dict[str, Any]:
        return self.call("GET", f"/rest/sample/{sample_id}/vtis")

    def get_sample_info(self, sample_id: int) -> Dict[str, Any]:
        return self.call("GET", f"/rest/sample/{sample_id}")

    def get_artifacts(self, sample_id: int, all_artifacts: bool) -> Dict[str, Any]:
        return self.call("GET", f"/rest/sample/{sample_id}/iocs/all_artifacts/{all_artifacts}")

    def get_submission(self, submission_id: int) -> Dict[str, Any]:
        return self.call("GET", f"/rest/submission/{submission_id}")

    def get_submissions(self, last_submission_id: Optional[int], limit: int = 100) -> List[Dict[str, Any]]:
        params = {"_order": "asc", "_limit": limit}

        if last_submission_id:
            if self.get_platform_version() >= Version("4.0.1"):
                # _last_id parameter was introduced in 4.0 and fixed in 4.0.1
                # greater than
                params["_last_id"] = last_submission_id
            else:
                # greater than or equals
                params["_min_id"] = last_submission_id + 1

        data = self.call("GET", "/rest/submission", params=params)
        return data

    def get_submissions_by_sample_id(self, sample_id: int) -> List[Dict[str, Any]]:
        return self.call("GET", f"/rest/submission?submission_sample_id={sample_id}")

    def submission_finished(self, submission_id: int) -> bool:
        return self.get_submission(submission_id)["submission_finished"]

    def submit(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.call("POST", "/rest/sample/submit", params=params)


@dataclass
class SubmissionResult:
    _api: VMRayAPIWrapper
    submission_id: int
    _sample_id: int = field(init=False)
    child_sample_ids: List[int] = field(default_factory=list)
    classifications: List[str] = field(default_factory=list)
    threat_names: List[str] = field(default_factory=list)
    verdict: Optional[str] = None
    verdict_reason: Optional[str] = None

    def __post_init__(self) -> None:
        sub = self._api.get_submission(self.submission_id)
        self._sample_id = sub["submission_sample_id"]

        if sub["submission_finished"]:
            self._update()

    def _update(self) -> None:
        """Update this `SampleResult`. This method is called automatically.

        Exceptions:
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        sample_info = self._api.get_sample_info(self._sample_id)
        self.child_sample_ids = sample_info.get("sample_child_sample_ids", [])
        self.classifications = sample_info.get("sample_classifications", [])
        self.threat_names = sample_info.get("sample_threat_names", [])
        self.verdict = sample_info.get("sample_verdict")
        self.verdict_reason = sample_info.get("sample_verdict_reason_description")

    def serialize(self) -> int:
        return self.submission_id

    def is_finished(self) -> bool:
        """Checks, if a submission is finished.

        Only use this method when a sample was submitted in non-blocking mode,
        otherwise `SampleResult` is fully initialized.

        Exception:
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        is_finished = self._api.submission_finished(self.submission_id)
        if is_finished:
            self._update()

        return is_finished

    def get_vtis(self) -> Dict[str, Any]:
        """Get threat indicators for a sample.

        Exceptions:
            KeyError: The VTI result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        return self._api.get_vtis_by_sample_id(self._sample_id)["threat_indicators"]

    def get_artifacts(self, ioc_only: bool = True) -> Dict[str, Any]:
        """Get all artifacts for a sample.

        Parameters:
            ioc_only : bool
                only return artifacts that are Indicators Of Compromise (IOC)

        Exceptions:
            KeyError: The artifacts result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        return self._api.get_artifacts(self._sample_id, not ioc_only)["iocs"]

    def get_reports(self) -> List[Dict[str, Any]]:
        """Get all reports for a submission.

        Exceptions:
            KeyError: The analysis result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        reports = list(self.iter_reports())
        return reports

    def iter_reports(self) -> Iterator[Dict[str, Any]]:
        """Iterator for all reports for a submission.

        Exceptions:
            KeyError: The analysis result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        analyses = self._api.get_analyses_by_submission_id(self.submission_id)

        for analysis in analyses:
            analysis_id = analysis["analysis_id"]
            report = self._api.get_report(analysis_id)
            yield json.load(report)

    def get_analysis_screenshots(self) -> List[BinaryIO]:
        screenshots = list(self.iter_analysis_screenshots())
        return screenshots

    def iter_analysis_screenshots(self) -> Iterator[BinaryIO]:
        analyses = self._api.get_analyses_by_submission_id(self.submission_id)

        for analysis in analyses:
            if analysis.get("analysis_analyzer_name") in ["vmray", "vmray_web"]:
                yield self._api.get_analysis_screenshots(analysis_id=analysis["analysis_id"])


class VMRaySubmissionKit:
    """A class to submit files and URLs on VMRay Platform."""

    def __init__(self, server: str,
                 api_key: str,
                 verify_cert: bool = True,
                 connector_name: Optional[str] = None) -> None:
        """
        Parameters:
            server : str
                URL to the VMRay Platform server
            api_key :str
                API key for VMRay Platform server
            verify_cert : bool
                verify SSL/TLS certificate of VMRay Platform server
            connector_name: Optional[str]
                A string that describes the script/program that uses the integration kit.
                E.g., <product_name>/<version>.
        """

        if connector_name:
            user_agent = f"{DEFAULT_USER_AGENT} ({connector_name})"
        else:
            user_agent = DEFAULT_USER_AGENT

        self._webhook_params = {}
        self._api = VMRayAPIWrapper(server, api_key, verify_cert)
        self._api.user_agent = user_agent

    def _wait_for_submissions(self, submissions: List[Dict[str, Any]]) -> None:
        """Wait for submissions to finish."""

        submission_ids = [submission["submission_id"] for submission in submissions]

        while True:
            submissions_finished = []
            for submission_id in submission_ids:
                finished = self._api.submission_finished(submission_id)
                submissions_finished.append(finished)

            if all(finished for finished in submissions_finished):
                break

            time.sleep(5)

    def _submit(self, blocking: bool, params: Dict[str, Any]) -> List[SubmissionResult]:
        """Submit a sample to VMRay Platform and process the result.

        Exceptions:
            ValueError: The submission result is invalid.
        """

        if "webhook_notification" in params and self._webhook_params:
            raise ValueError("Webhooks set multiple times.")

        if self._webhook_params:
            params["webhook_notification"] = json.dumps(self._webhook_params)

        result = self._api.submit(params)

        try:
            submissions = result["submissions"]
            _ = [s["submission_id"] for s in submissions]
        except KeyError as exc:
            raise ValueError("The submission result is invalid") from exc

        if not blocking:
            return [
                SubmissionResult(self._api, s["submission_id"])
                for s in submissions
            ]

        self._wait_for_submissions(submissions)

        results = []
        for submission in submissions:
            sample_result = SubmissionResult(self._api, submission["submission_id"])
            results.append(sample_result)

        return results

    def submit_file(
        self, sample_path: Path, blocking: bool = True, params: Optional[Dict[str, Any]] = None
    ) -> List[SubmissionResult]:
        """Submit a file on VMRay Platform.

        Parameters:
            sample_path : Path
                Path to a file you want to analyze.
            blocking : bool
                Wait for an analysis to finish before returning.
            params : Optional[Dict[str, Any]]
                Key/Value pairs to configure the analysis.
                More documentation can be found in the API docs.

        Exceptions:
            FileNotFoundError: An error indicating that the file couldn't be found.
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        if not params:
            params = {}

        with sample_path.open("rb") as fobj:
            params["sample_file"] = fobj
            return self._submit(blocking, params)

    def submit_url(
        self, url: str, blocking: bool = True, params: Optional[Dict[str, Any]] = None
    ) -> List[SubmissionResult]:
        """Submit a URL on VMRay Platform.

        Parameters:
            url : str
                URL to a website you want to analyze.
            blocking : bool
                Wait for an analysis to finish before returning.
            params : Optional[Dict[str, Any]]
                Key/Value pairs to configure the analysis.
                More documentation can be found in the API docs.

        Exceptions:
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        if not params:
            params = {}

        params["sample_url"] = url
        return self._submit(blocking, params)

    def iter_submissions(self, last_submission_id: Optional[int], limit: int = 100) -> Iterator[SubmissionResult]:
        """An iterator for finished submissions.

        Retrieves submissions based on `last_submissions_id` where `limit` determines
        how many per iteration.

        Parameters:
            last_submission_id : Optional[int]
                A submission ID to start with.
                The first submission is used if ID is `0` or `None`.
            limit : int
                Number of submissions to fetch for one iteration.

        Exceptions:
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        submissions = self._api.get_submissions(last_submission_id, limit)

        for submission in submissions:
            try:
                sample_result = SubmissionResult(self._api, submission["submission_id"])
            except KeyError as exc:
                raise ValueError("The submission result is invalid") from exc

            yield sample_result

    def set_webhook(self, url: str,
                    verify_tls: Optional[bool] = None,
                    timeout: Optional[float] = None,
                    retries: Optional[int] = None,
                    headers: Optional[Dict[str, str]] = None):
        """Sets parameters for a webhook which will be triggered once all analyses are done.

        The given url will receive a POST request containing information about the submission once
        all analyses have either run successfully or failed permanently.

        Parameters:
            url: str
                The URL the POST should be sent to. Must be an URL of either http or https scheme
            verify_tls: Optional[bool]
                Select if the server should verify TLS certificate of the webhook target
                Server default will be used if left unset.
            timeout: Optional[int]
                Connection timeout when connecting to the webhook target.
                Server default will be used if left unset.
            retries: Optional[int]
                Number of retries in addition to the initial attempt to deliver the webhook
                Server default will be used if left unset.
            headers: Optional[Dict[str,str]]
                Specify headers that should be set when making the request
                Server default will be used if left unset.

        """
        params = {"url": url}

        for param, param_name in [(verify_tls, "verify_tls"),
                                  (timeout, "timeout"),
                                  (retries, "retries"),
                                  (headers, "headers")]:
            if param is not None:
                params[param_name] = param

        self._webhook_params = params

    def unset_webhook(self):
        """ Removes stored parameters for a submission WebHook.

        After calling this method, subsequent submissions will not call a WebHook upon completion.
        To enable WebHooks again, call the set_webhook(..) method with parameters.
        """
        self._webhook_params = {}

    def deserialize(self, submission_id: int) -> SubmissionResult:
        """Deserialize `SubmissionResult` from a value returned by `SubmissionResult.serialize`"""

        return SubmissionResult(self._api, submission_id)

    def get_submissions_from_sample_id(self, sample_id: int) -> List[SubmissionResult]:
        """Get a list of submissions related to a sample ID

        Exceptions:
            ValueError: The submission result is invalid.
            VMRayRESTAPIError: An error occurred while interacting with VMRay Platform.
        """

        submissions = []
        for submission in self._api.get_submissions_by_sample_id(sample_id):
            try:
                submissions.append(SubmissionResult(self._api, submission["submission_id"]))
            except KeyError as exc:
                raise ValueError("The submission result is invalid") from exc

        return submissions

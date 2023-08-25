import glob

from setuptools import find_namespace_packages, setup


EXAMPLE_SCRIPTS = list(glob.glob("examples/*.py"))


setup(
    # metadata
    name="vmray_rest_api",
    version="6.0.0",  # please update also the version in vmray.rest_api.version
    url="https://www.vmray.com",
    author="VMRay",
    author_email="info@vmray.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    license="Proprietary",
    description="VMRay REST API Client and Integration Kit",

    # options
    python_requires=">=3.8",
    install_requires=[
        "packaging",
        "requests",
    ],
    packages=find_namespace_packages(include=["vmray.*"]),
    scripts=EXAMPLE_SCRIPTS,
    data_files=[
        ("", ["LICENSE", "README.md"]),
    ],
    zip_safe=False,
)

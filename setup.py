import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dialog-api-pytest",
    version="0.0.1",
    author="Dialog QA Team",
    author_email="zs@dlg.im",
    description="Pytest-based tests for Dialog gRPC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.transmit.im/projects/AUTT/repos/server-test-suite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
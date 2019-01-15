""" Python packaging for irobotframework

    Automagically installs kernelspecs, probably more later...
"""
import setuptools
from pathlib import Path
import re


NAME = "irobotframework"
HERE = Path(__file__).parent.resolve()
SRC = HERE / "src" / NAME
RESOURCES = SRC / "resources"
VERSION_RE = r""".*__version__ = (['"])(\d+\.\d+\.\d+)\1.*"""


setup_args = dict(
    name=NAME,
    version=re.findall(VERSION_RE, (SRC / "_version.py").read_text())[0][1],
    description="Jupyter integration for Robot Framework",
    license="BSD-3-Clause",
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/gtri/irobotframework",
    author="Georgia Tech Research Corporation",
    author_email="opensource@gtri.gatech.edu",
    data_files=[
        (
            "share/jupyter/kernels/robotframework",
            [str(p.relative_to(HERE)) for p in RESOURCES.glob("*")],
        )
    ],
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=[
        "ipykernel>=5.1",
        "IPython>=7.2",
        "robotframework>=3.1",
        "importnb>=0.5.2",
    ],
    tests_require=["jupyter_kernel_test", "robotframework-seleniumlibrary", "pytest"],
    keywords=["Interactive", "Interpreter", "Shell", "Testing", "Web"],
    classifiers=[
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    zip_safe=False,
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)

import os
from glob import glob
from os.path import basename, splitext

import setuptools

if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
else:
    version = os.environ["CI_JOB_ID"]

base_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_path, "README.md")) as f:
    README = f.read()

REQUIREMENTS = ["Jinja2"]

setuptools.setup(
    # name="kobo-highlights-extractor",
    # description = "A package to extract highlights from kobo books",
    version=version,
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    python_requires=">=3.11",
    keywords=["kobo", "ereader"],
    install_requires=REQUIREMENTS,
)

import os
from glob import glob
from os.path import basename, splitext

import setuptools

base_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_path, "README.md")) as f:
    README = f.read()

REQUIREMENTS = ["Jinja2"]

setuptools.setup(
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    python_requires=">=3.11",
    keywords=["kobo", "ereader"],
    install_requires=REQUIREMENTS,
)

import setuptools
from pathlib import Path

setuptools.setup(
    name="moshpdf11451435231",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"])
)
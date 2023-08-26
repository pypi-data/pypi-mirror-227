import setuptools
from pathlib import Path

setuptools.setup(
    name="asmita_matplotlib",
    version="1.0",  # Use a string for the version
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages()
)


from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

REQUIREMENTS = [
    "requests",
    "requests_cache",
    "beautifulsoup4",
    "pandas",
    "tqdm",
    "termcolor",
]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Office/Business :: Financial",
    "Topic :: Internet",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]

setup(
    name="Xchanger",
    version="0.1.1 ",
    description="A Python module to get and save exchange rates in different formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maaz Ali",
    author_email="devlprkhan04@gmail.com",
    url="https://github.com/MaazAli04/XC",
    packages=["fx"],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords="real-time exchange rates",
)

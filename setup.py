from setuptools import setup, find_packages
from generate_gitignore.version import __version__

setup(
    name="generate-gitignore",
    version=__version__,
    author="Kristián Kunc",
    author_email="kristian@kristn.co.uk",
    description="A CLI tool for generating .gitignore files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kristiankunc/generate-gitignore",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "argparse",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "generate-gitignore=generate_gitignore.main:main",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

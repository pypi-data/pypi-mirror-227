from setuptools import setup

def readme():
    with open("README.md", "r") as rfile:
        contents = rfile.read()
        rfile.close()
    return contents

setup(
    name="octopype",
    version="0.1.0",
    description="GitHub API Wrapper written in Python.",
    long_description_content_type="text/markdown",
    long_description=readme(),
    author="BLUEAMETHYST-Studios",
    maintainer="BLUEAMETHYST-Studios",
    url="https://github.com/BLUEAMETHYST-Studios/octopype",
    keywords=[
        "github",
        "api",
        "wrapper",
        "http"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
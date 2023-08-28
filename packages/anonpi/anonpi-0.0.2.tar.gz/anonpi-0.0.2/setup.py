from setuptools import setup , find_packages
from anonpi.version import version


with open("README.MD", "r") as fh:
    long_description = fh.read()

setup(
    name="anonpi",
    version=version,
    author = "EvenueStar",
    description = "The \"anonpi\" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        'Programming Language :: Python :: Implementation',
        "Topic :: Education"
    ],
    packages=find_packages(),
    keywords=[
        "anon",
        "joker",
        "calling",
        "api",
        "anonpi",
        "anonpi.co",
        "anonpi python",
        "anonpi python module",
        "anonpi python package",
        "anonpi python api",
        "anonpi api"
        "anonpi python calling api",
        "calling api",
        "calling api python",
        "calling api python module",
        "calling api python package",
        "calling system",
    ]
)


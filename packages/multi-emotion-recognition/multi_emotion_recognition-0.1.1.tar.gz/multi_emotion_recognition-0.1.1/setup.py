#!/usr/bin/env python
import os

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()
with open(os.path.join("src", "version.txt")) as f:
    version = f.read().strip()

setup(
    name="multi_emotion_recognition",
    version=version,

    description="detect multiple emotions in a sentence including [anger, anticipation, disgust, fear, joy, love, optimism, pessimism, sadness,\
                    surprise, trust]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jinfen Li",
    author_email="jli284@syr.edu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    url="https://github.com/JinfenLi/multi_emotion_recognition",
    license="MIT",
    install_requires=["lightning==2.0.7", "torch > 2.0",
                      "emotlib==1.0.1",
                      "numpy==1.25.2", "pandas==2.0.3",
                      "protobuf==3.20.0", "rich==13.5.2", "torchmetrics==1.1.0",
                      "tqdm==4.66.1",
                      "transformers==4.31.0"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),


)

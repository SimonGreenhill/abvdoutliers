from setuptools import setup, find_packages
import json

with open("metadata.json", "r", encoding="utf-8") as fp:
    metadata = json.load(fp)


setup(
    name="lexibank_abvdoutliers",
    description=metadata["title"],
    license=metadata["license"],
    url=metadata["url"],
    py_modules=["lexibank_abvdoutliers"],
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(where='.'),
    entry_points={
        "lexibank.dataset": [
            "abvdoutliers=lexibank_abvdoutliers:Dataset",
        ],
        "cldfbench.commands": [
            "abvdoutliers=abvdoutliers_commands",
        ],
    },
    extras_require={"test": ["pytest-cldf"]},
    install_requires=[
        "pylexibank>=2.1",
        "cldfbench>=1.14.1",
        "clldutils~=3.21.0",
        "nexusmaker>=2.0.6",
    ],
)

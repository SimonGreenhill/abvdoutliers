from setuptools import setup
import json

with open('metadata.json', 'r', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_abvdoutliers',
    description=metadata['title'],
    license=metadata['license'],
    url=metadata['url'],
    py_modules=['lexibank_abvdoutliers'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'abvdoceanic=lexibank_abvdoutliers:Dataset',
        ],
    },
    extras_require={"test": ["pytest-cldf"]},
    install_requires=[
        'pylexibank>=2.1',
        'nexusmaker',
    ]
)

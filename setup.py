import sys
from pathlib import Path

import setuptools

if sys.version_info < (3, 11):
    sys.exit('Sorry, panoptes requires Python >= 3.11')

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name='panoptes-ui',
    version='1.1.1',
    url='https://github.com/panoptes-organization/panoptes',
    license='MIT',
    author='panoptes-organization',
    author_email='georgekostoulas@gmail.com, agardelakos@gmail.com, fgypas@gmail.com, gntalaperas@gmail.com, dimitris.afe@gmail.com, rekoumisd@gmail.com, vsochat@stanford.edu',
    description="panoptes: monitor computational workflows in real time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
    entry_points={
        'console_scripts': ['panoptes=panoptes:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "flask >= 1.1.1",
        "humanfriendly >= 4.18",
        "marshmallow >= 3.0.1",
        "SQLAlchemy >= 1.3.7",
    ],
    extras_require={
        "dev": [
            "pytest >= 5.3.0",
            "requests >= 2.22.0",
        ],
    },
    include_package_data=True,
)

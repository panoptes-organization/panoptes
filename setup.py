import sys
from setuptools import setup
import setuptools

if sys.version_info < (3, 6):
    sys.exit('Sorry, panoptes requires Python >= 3.6')

setup(
    name='panoptes-ui',
    version='0.2.0',
    url='https://github.com/panoptes-organization/panoptes',
    license='MIT',
    author='panoptes-organization',
    author_email='georgekostoulas@gmail.com, agardelakos@gmail.com, fgypas@gmail.com, gntalaperas@gmail.com, dimitris.afe@gmail.com, rekoumisd@gmail.com, vsochat@stanford.edu',
    description="panoptes: monitor computational workflows in real time",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['panoptes=panoptes:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "flask >= 1.1.1",
        "humanfriendly >= 4.18",
        "marshmallow >= 3.0.1",
        "pytest >= 5.3.0",
        "requests >= 2.22.0",
        "SQLAlchemy >= 1.3.7",
    ],
    include_package_data=True,
)

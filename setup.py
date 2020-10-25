import sys
from setuptools import setup
import setuptools

if sys.version_info < (3, 6):
    sys.exit('Sorry, panoptes requires Python >= 3.6')

requirements = []

with open("requirements.txt") as fp:
    for line in fp:
        requirements.append(line.replace("==", ">="))

setup(
    name='panoptes',
    version='0.1.0',
    url='https://github.com/panoptes-organization/panoptes',
    license='MIT',
    author='panoptes-organization',
    author_email='georgekostoulas@gmail.com, agardelakos@gmail.com, fgypas@gmail.com, gntalaperas@gmail.com',
    description="panoptes: monitor computational workflows in real time",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=['panoptes.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)

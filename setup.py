import subprocess

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class NPMInstall(build_py):
    def run(self):
        subprocess.check_call("pip install -r requirements.txt", shell=True)
        subprocess.check_call("nodeenv -p", shell=True)
        subprocess.check_call(["npm --prefix ./server/static install ./server/static"], shell=True)
        # self.run_command("npm --prefix ./server/static install ./server/static")
        build_py.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='panoptes',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/panoptes-organization/panoptes',
    license='MIT',
    author='panoptes-organization',
    author_email='georgekostoulas@gmail.com, agardelakos@gmail.com, fgypas@gmail.com, gntalaperas@gmail.com',
    description=long_description,
    cmdclass={
        'npm_install': NPMInstall
    },
)

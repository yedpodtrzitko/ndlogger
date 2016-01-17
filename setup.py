from os.path import join, dirname
from setuptools import setup, find_packages

with open('PROJECT', 'r') as f:
    PROJECT = f.read().strip()

project_version = __import__(PROJECT)
version = project_version.__versionstr__

with open(join(dirname(__file__), 'requirements.txt')) as f:
    requirements = [x.strip() for x in f.readlines()]

setup(
    name=PROJECT,
    version=version,
    classifiers=['Private :: Do Not Upload'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        %s=%s.cli:main
    ''' % (PROJECT, PROJECT),
)

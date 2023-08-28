from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

setup(
    name='urlincode2',
    version='0.5.10',
    packages=find_packages(),
    url='http://192.168.9.3:1234/',
    license='Testing Azure',
    project_urls= {
    	'Homepage': 'http://192.168.9.3:1234/',
        'Bug Tracker': 'http://192.168.9.3:1234/',
        'Source Code': 'http://192.168.9.3:1234/'
    }
)


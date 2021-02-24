# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in room_booking/__init__.py
from room_booking import __version__ as version

setup(
	name='room_booking',
	version=version,
	description='room booking',
	author='eneegy',
	author_email='n/a',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

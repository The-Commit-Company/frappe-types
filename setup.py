from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_types/__init__.py
from frappe_types import __version__ as version

setup(
	name="frappe_types",
	version=version,
	description="Typescript type definition generator for Frappe DocTypes",
	author="Nikhil Kothari",
	author_email="nik.kothari22@live.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

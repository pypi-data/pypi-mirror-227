from setuptools import setup, find_packages


setup(
	name="hactool0",
	version="0.15.0",
	description="This tool can help you a lot",
	long_description=open("README.md", encoding="utf-8").read(),
	url="",
	author="GhostShadow",
	license="GNU",
	keywords=["hactool", "pyp"],
	packages=find_packages(),
	include_package_data=True,
	install_requires=["keyboard", "pyperclip"]
)
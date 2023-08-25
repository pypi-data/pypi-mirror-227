from setuptools import setup,find_packages


setup(
  name='hactool0',
  version='0.13.2',
  description='This tool can help you a lot',
  long_description=open('README.md').read(),
  author='GhostShadow',
  license='GNU',
  keywords='hactool',
  packages=find_packages(),
  include_package_data=True,
  install_requires=['keyboard','pyperclip']
)
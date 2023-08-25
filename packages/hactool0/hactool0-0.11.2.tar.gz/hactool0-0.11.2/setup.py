from setuptools import setup, find_packages


setup(
  name='hactool0',
  version='0.11.2',
  description='This tool can help you a lot',
  long_description=open('README.md').read(),
  url='',
  author='GhostShadow',
  license='GNU',
  keywords='hactool',
  packages=find_packages(),
  install_requires=['colorama','keyboard','numpy','pick','playsound','pyautogui','pyperclip','tabulate']
)
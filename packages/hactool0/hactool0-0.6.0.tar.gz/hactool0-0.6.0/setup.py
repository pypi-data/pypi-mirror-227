from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='hactool0',
  version='0.6.0',
  description='hactool',
  long_description=open('README.md').read(),
  url='',
  author='GhostShadow',
  license='GNU',
  classifiers=classifiers,
  keywords='hactool',
  packages=find_packages(),
  install_requires=['time','pyperclip','pyautogui','playsound','os','pyTwistyScrambler']
)

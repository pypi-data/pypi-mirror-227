from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='numbars',
  version='1.0.3',
  description='A python library that allows you to add, subtract, multiply, divide, and randomize numbers.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='zelofi',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator, numbers, add, subract, multiply, divide, randomize', 
  packages=find_packages(),
  install_requires=[''] 
)
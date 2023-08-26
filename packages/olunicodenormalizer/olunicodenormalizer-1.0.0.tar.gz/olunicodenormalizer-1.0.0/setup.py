
#------------------------------------------------------------
from __future__ import print_function
#------------------------------------------------------------
from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.10'
]
 
setup(
  name='olunicodenormalizer',
  version='1.0.0',
  description='Olchiki Unicode Normalization Toolkit',
  long_description=open('README.md',encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt',encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Shivnath Kisku',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords=['olchiki','unicode','text normalization','indic'], 
  packages=find_packages(),
  install_requires=[''] 
)
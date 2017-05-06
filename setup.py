from setuptools import setup, find_packages
from distutils.version import StrictVersion
from importlib import import_module
import re


def get_version(verbose=1):
    """ Extract version information from source code """

    try:
        with open('VZcomp/version.py', 'r') as f:
            ln = f.readline()
            # print(ln)
            m = re.search('.* ''(.*)''', ln)
            version = (m.group(1)).strip('\'')
    except Exception as E:
        print(E)
        version = 'none'
    if verbose:
        print('get_version: %s' % version)
    return version


def readme():
    with open('README.md') as f:
        return f.read()


def license():
    with open('LICENSE.txt') as f:
        return f.read()

setup(name='VZcomp',
      version=get_version(),
      use_2to3=False,
      author='Ramiro Sagastizabal',
      author_email='sagastizabal.ramiro@gmail.com',
      maintainer='Ramiro Sagastizabal',
      maintainer_email='sagastizabal.ramiro@gmail.com',
      description='Python based quantum compiler '
                  'uses the VirtualZ compilation explained in the notes '
                   'developed as member of the DiCarlo-lab at '
                    'QuTech, Delft University of Technology',
      long_description=readme(),
      url='https://github.com/elrama-/VZcomp',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering'
      ],
      license=license(),
      # if we want to install without tests:
      # packages=find_packages(exclude=["*.tests", "tests"]),
      packages=find_packages(),
      install_requires=[
          'numpy>=1.10',
      ],
      test_suite='pycqed.tests',
      zip_safe=False)

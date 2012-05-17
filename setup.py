from setuptools import setup, find_packages, Extension
import sys, os

version = '0.1.0'

install_requires = [
    # -*- Extra requirements: -*-
    'simplecoremidi>=0.2.2',
    ]

setup(name='musi',
      version=version,
      description="A library for making music and noise with MIDI",
      long_description=open("README", "r").read(),
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "License :: OSI Approved :: MIT License",
        ],
      keywords='MIDI, music',
      author='Mike Verdone',
      author_email='mike.verdone+musi@gmail.com',
      url='https://github.com/sixohsix/musi',
      license=open('LICENSE', 'r').read(),
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

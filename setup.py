from setuptools import setup, find_packages
import sys, os

version = '0.1'
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

setup(name='greenlight',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[],
      keywords='gevent',
      author='Ian McCracken',
      author_email='ian.mccracken@gmail.com',
      url='http://concisionandconcinnity.blogspot.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['gevent'],
      entry_points="""
      """,
      )

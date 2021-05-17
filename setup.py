#!/usr/bin/env python3

from setuptools import setup

setup(name='bulk_commands',
      version='0.1',
      description='Script to run bulk commands',
      url='/var/adm/projects/development/bulk_commands',
      author='Daryl Stark',
      author_email='github@dstark.nl',
      license='GNU GPLv3',
      entry_points = {
            'console_scripts': [
                'bulk_commands=bulk:main'
                ],
            },
      zip_safe=False)

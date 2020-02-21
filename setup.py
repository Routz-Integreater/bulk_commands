#!/usr/bin/env python3

from setuptools import setup

setup(name='setup',
      version='0.1',
      description='Script om bulk commandos uit te voeren',
      url='/var/adm/projects/development/bulk_commands',
      author='Daryl Stark',
      author_email='daryl.stark@kpn.com',
      license='GNU GPLv3',
      entry_points = {
            'console_scripts': [
                'bulk_commands=bulk:main'
                ],
            },
      zip_safe=False)

# setup.py
# -*- coding: UTF-8 -*-
try:
    from setuptools import setup
except:
    from distutils.core import setup

def get_version():
    return 50 #import subprocess
    rev = subprocess.check_output(['git', 'rev-list', 'HEAD', '--count']).decode().strip()
    return rev or u'unknown'

setup(name='oxtimelines',
    version='0.%s' % get_version() ,
    scripts=[
        'bin/oxtimelines',
    ],
    packages=[
        'oxtimelines',
    ],
    author='0x2620',
    author_email='0x2620@0x2620.org',
    url="https://wiki.0x2620.org/wiki/oxtimelines",
    download_url="http://code.0x2620.org/oxtimelines/download",
    license="GPLv3",
    description='extract timelines from videos',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)


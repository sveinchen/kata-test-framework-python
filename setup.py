#!/usr/bin/env python

import os
import sys

from setuptools import Command, find_packages, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

version_file = os.path.join(
    BASE_DIR,
    'kata_test_framework/version.txt'
)


class VersionCommand(Command):

    description = "generate version number, and write to version file"
    user_options = [
        ('in-place', 'i', 'edit file in-place'),
    ]

    def run(self):
        try:
            from setuptools_scm import get_version
        except ImportError:
            sys.stderr.write("[FAILED] this command requires 'setuptools_scm'"
                             " to be installed!\n")
            sys.exit(1)
        else:
            if self.in_place:
                version = get_version(root=BASE_DIR, write_to=version_file)
                sys.stdout.write("[DONE] write version %r to %r\n"
                                 % (version, version_file))
            else:
                version = get_version(root=BASE_DIR)
                sys.stdout.write("%r\n" % version)

    def initialize_options(self):
        self.in_place = None

    def finalize_options(self):
        self.in_place = False if self.in_place is None else True


install_requires = [
]

with open(version_file, "r") as fd:
    version = fd.readline().strip()

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name="kata-test-framework",
    version=version,
    author="sveinchen",
    author_email="sveinchen@gmail.com",
    url="https://sveinchen.github.io/kata-test-framework",
    packages=find_packages(include=['kata_test_framework',
                                    'kata_test_framework.*']),
    entry_points={
        'console_scripts': [
            'kata-test = kata_test_framework.runner2:run',
        ],
    },
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'version': VersionCommand,
    },
)

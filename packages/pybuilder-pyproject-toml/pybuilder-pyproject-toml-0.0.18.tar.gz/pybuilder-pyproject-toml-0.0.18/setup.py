#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup, Extension
from setuptools.command.install import install as _install


class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()



if __name__ == '__main__':
    setup(
        name = 'pybuilder-pyproject-toml',
        version = '0.0.18',
        description = 'PyBuilder plugin for getting information from pyproject.toml file or environment variables',
        long_description = '\nPlease, see https://github.com/chylek/pybuilder-pyproject-toml for more information.\n',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7'
        ],
        keywords = '',

        author = 'Martin Gruber, Adam Chýlek',
        author_email = 'martin.gruber@email.cz, adam@chylek.eu',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT',

        url = 'https://github.com/chylek/pybuilder-pyproject-toml',
        project_urls = {},

        scripts = [],
        packages = ['pybuilder_pyproject_toml'],
        namespace_packages = [],
        py_modules = [],
        ext_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        include_package_data = False,
        install_requires = ['toml'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
        setup_requires = [],
    )

# -*- coding: utf-8 -*-
import operator
import os
import re
from functools import reduce

from pybuilder.core import init

__author__ = u"Martin Grůber, Adam Chýlek"

try:
    string_types = basestring
except NameError:
    string_types = str


def read_from(filename):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)) as f:
        result = f.read()
    return result


@init
def init_pyproject_plugin(project, logger):
    project.plugin_depends_on("toml", "~=0.10.0")


def section_get(config, section, option, fallback=None):
    try:
        subsections = section.split(".")
        return reduce(operator.getitem, subsections, config)[option]
    except KeyError:
        return fallback


@init
def init_from_pyproject(project, logger):
    import toml
    
    pyproject_filename = os.path.join(project.basedir, "pyproject.toml")
    try:
        config = toml.load(pyproject_filename)
    except Exception as e:
        logger.error(f"pyproject_toml plugin: pyproject.toml not loaded ({pyproject_filename}), {e}")
    else:
        logger.info(f"pyproject_toml plugin: Loaded configuration from {pyproject_filename}")
    name = os.environ.get("PYB_SCFG_NAME", section_get(config, "metadata", "name"))
    version = os.environ.get("PYB_SCFG_VERSION", section_get(config, "metadata", "version"))
    if version and version.startswith("file: "):
        version = read_from(version.split(maxsplit=1)[1])
    distutils_commands = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), os.environ.get(
            "PYB_SCFG_DISTUTILS_COMMANDS", ""
        ).split()
    )))
    if not distutils_commands:
        section_get(config, "tool.pybuilder", "distutils_commands", fallback=["sdist"])
    distutils_upload_repository = os.environ.get(
        "PYB_SCFG_UPLOAD_REPOSITORY", section_get(config, "tool.pybuilder", "distutils_upload_repository", fallback=None)
    )
    copy_resources_glob = section_get(config, "tool.pybuilder", "copy_resources_glob", fallback=[])

    package_data = section_get(config, "files", "package_data", fallback={})

    if not package_data and "options.package_data" in config:
        package_data = config["options.package_data"]

    cython_include_modules = section_get(config, "tool.pybuilder", "cython_include_modules", fallback=[])
    cython_exclude_modules = section_get(config, "tool.pybuilder", "cython_exclude_modules", fallback=[])
    cython_remove_python_sources = section_get(config, "tool.pybuilder", "cython_remove_python_sources", fallback=False)
    cython_compiler_directives = section_get(config, "tool.pybuilder","cython_compiler_directives", fallback={})
    
    coverage_break_build_from_cfg = section_get(config, "coverage:report", "fail_under", fallback=None)
    if coverage_break_build_from_cfg is None:
        coverage_break_build_from_cfg = section_get(config, "tool.pytest.ini_options", "coverage_break_build_threshold", fallback=None)
    pytest_coverage_break_build_threshold = os.environ.get(
        "PYB_SCFG_PYTEST_COVERAGE_BREAK_BUILD_THRESHOLD",
        coverage_break_build_from_cfg
    )

    pytest_coverage_html = section_get(config, "tool.pytest.ini_options", "coverage_html", fallback=False)
    pytest_coverage_annotate = section_get(config, "tool.pytest.ini_options", "coverage_annotate", fallback=False)

    docstr_coverage_config = section_get(config, "tool.docstr_coverage", "config", fallback=None)
    docstr_coverage_fail_under = section_get(config, "tool.docstr_coverage", "fail_under", fallback=None)

    scm_ver_version_scheme = section_get(config, "tool.setuptools_scm", "version_scheme", fallback=None)
    scm_ver_version_scheme = os.environ.get("PYB_SCFG_SCM_VERSION_SCHEME", scm_ver_version_scheme)
    scm_ver_local_scheme = section_get(config, "tool.setuptools_scm", "local_scheme", fallback=None)
    scm_ver_local_scheme = os.environ.get("PYB_SCFG_SCM_VERSION_SCHEME", scm_ver_local_scheme)
    scm_ver_root = section_get(config, "tool.setuptools_scm", "root", fallback=None)
    scm_ver_root = os.environ.get("PYB_SCFG_SCM_ROOT", scm_ver_root)
    scm_ver_relative_to = section_get(config, "tool.setuptools_scm", "relative_to", fallback=None)
    scm_ver_relative_to = os.environ.get("PYB_SCFG_SCM_RELATIVE_TO", scm_ver_relative_to)

    # analyze - Python flake8 linting
    # publish - create distributions (sdist, bdist)
    # upload - upload to the PyPI server
    # clean - clean all temporary files
    # sphinx_generate_documentation - generate sphinx documentation
    default_task = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), os.environ.get(
            "PYB_SCFG_DEFAULT_TASK", "").split())))
    if not default_task:
        default_task = section_get(config, "tool.pybuilder", "default_task", fallback=["analyze", "publish", "clean"])


    if name:
        project.set_property("name", name)
        # Setting property is not enough
        project.name = name
        logger.debug("pyproject_toml plugin: Name set to: {}".format(name))

    if version:
        project.set_property("version", version)
        # Setting property is not enough
        project.version = project.get_property("version")
        logger.debug("pyproject_toml plugin: Version set to: {}".format(version))

    if default_task:
        # Setting property is breaking this thing...
        # project.set_property("default_task", default_task)
        project.default_task = default_task
        logger.debug("pyproject_toml plugin: Default task set to: {}".format(default_task))

    if distutils_commands:
        project.set_property_if_unset("distutils_commands", distutils_commands)
        logger.debug("pyproject_toml plugin: Distutils commands set to: {}".format(distutils_commands))

    # TWINE_REPOSITORY_URL environment variable is preferred
    if os.environ.get("TWINE_REPOSITORY_URL") is None and distutils_upload_repository is not None:
        project.set_property_if_unset("distutils_upload_repository", distutils_upload_repository)
        logger.debug("pyproject_toml plugin: Upload repository set to: {}".format(distutils_upload_repository))

    if len(cython_include_modules):
        # Cython extension modules definition
        project.set_property_if_unset("distutils_cython_ext_modules", [{
            "module_list": cython_include_modules,
            "exclude": cython_exclude_modules,
        }])
        logger.debug("pyproject_toml plugin: Included cython modules: {}".format(cython_include_modules))
        logger.debug("pyproject_toml plugin: Excluded cython modules: {}".format(cython_exclude_modules))

    if cython_remove_python_sources:
        # Remove the original Python source files from the distribution
        project.set_property_if_unset("distutils_cython_remove_python_sources", cython_remove_python_sources)
        logger.debug("pyproject_toml plugin: Remove python sources when cythonized: {}".format(cython_remove_python_sources))
    if cython_compiler_directives:
        project.set_property_if_unset("distutils_cython_compiler_directives", cython_compiler_directives)
        logger.debug("pyproject_toml plugin: Set cython compiler directives: {}".format(cython_compiler_directives))
    if copy_resources_glob:
        package_data.values()
        # Make the full files paths from the package name and the pattern; replace '.' in the package name with '/'
        package_data_patterns = [["/".join([k.replace(".", "/"), vi]) for vi in v] for k, v in package_data.items()]
        logger.debug(f"pyproject_toml plugin: package_data_patterns: {package_data_patterns}")
        project.set_property_if_unset("copy_resources_glob", copy_resources_glob + reduce(
            operator.concat, package_data_patterns, [])
         )
        logger.debug(f"pyproject_toml plugin: Configured resource copying glob: {copy_resources_glob}")

    if package_data:
        project.package_data.update(package_data.items())
        logger.debug("pyproject_toml plugin: Added some package data")

    try:
        pytest_coverage_break_build_threshold = int(pytest_coverage_break_build_threshold)
    except (ValueError, TypeError):
        pytest_coverage_break_build_threshold = None
    if pytest_coverage_break_build_threshold is not None:
        project.set_property_if_unset("pytest_coverage_break_build_threshold", pytest_coverage_break_build_threshold)
        logger.debug("pyproject_toml plugin: PyTest coverage break threshold set to {}".format(pytest_coverage_break_build_threshold))

    try:
        docstr_coverage_fail_under = int(docstr_coverage_fail_under)
    except (ValueError, TypeError):
        docstr_coverage_fail_under = None
    if docstr_coverage_fail_under is not None:
        project.set_property_if_unset("docstr_coverage_fail_under", docstr_coverage_fail_under)
        logger.debug("pyproject_toml plugin: Docstring coverage fail under set to {}".format(docstr_coverage_fail_under))

    if docstr_coverage_config:
        project.set_property_if_unset("docstr_coverage_config", docstr_coverage_config)
        logger.debug("pyproject_toml plugin: Docstring coverage config set to {}".format(docstr_coverage_config))

    if scm_ver_version_scheme:
        project.set_property_if_unset("scm_ver_version_scheme", scm_ver_version_scheme)
        logger.debug("pyproject_toml plugin: SCM version_scheme set to {}".format(scm_ver_version_scheme))

    if scm_ver_local_scheme:
        project.set_property_if_unset("scm_ver_local_scheme", scm_ver_local_scheme)
        logger.debug("pyproject_toml plugin: SCM local_scheme set to {}".format(scm_ver_local_scheme))

    if scm_ver_root:
        project.set_property_if_unset("scm_ver_root", scm_ver_root)
        logger.debug("pyproject_toml plugin: SCM root set to {}".format(scm_ver_root))

    if scm_ver_relative_to:
        project.set_property_if_unset("scm_ver_relative_to", scm_ver_relative_to)
        logger.debug("pyproject_toml plugin: SCM relative_to set to {}".format(scm_ver_relative_to))

    project.set_property_if_unset("pytest_coverage_html", pytest_coverage_html)
    logger.debug("pyproject_toml plugin: PyTest coverage HTML set to {}".format(pytest_coverage_html))

    project.set_property_if_unset("pytest_coverage_annotate", pytest_coverage_annotate)
    logger.debug("pyproject_toml plugin: PyTest coverage annotateL set to {}".format(pytest_coverage_annotate))

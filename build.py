#   -*- coding: utf-8 -*-
from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin('pypi:pybuilder_pytest')
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("pypi:vulture")
use_plugin("pypi:interrogate")

name = "neorg-discord-bot"
default_task = "publish"

@init
def set_properties(project):
    project.build_depends_on('coverage')
    project.depends_on('flask')
    project.get_property("pytest_extra_args").append("-x")
    project.set_property('coverage_break_build', False)
    project.set_property('flake8_break_build', False)

# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" Pure python tests of kernel behavior
"""
import jupyter_kernel_test

from . import RobotBase


class Basics(RobotBase, jupyter_kernel_test.KernelTests):
    """ Basic tests of kernel functionality
    """

    file_extension = ".robot"

    code_hello_world = """%%python module NotAModule
print("hello, world")
"""

    code_generate_error = """%%python module NotAModule
raise Exception("hello, world")
"""


class MoreErrors(RobotBase, jupyter_kernel_test.KernelTests):
    code_generate_error = """%%python module NotAModule
__import__("sys").exit(0)
"""

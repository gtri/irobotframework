# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" Pure python tests of kernel behavior
"""
import jupyter_kernel_test

from . import RobotBase


class InspectTest(RobotBase, jupyter_kernel_test.KernelTests):
    code_inspect_sample = """
*** Settings ***
Library  BuiltIn"""


class InspectTest2(RobotBase, jupyter_kernel_test.KernelTests):
    code_inspect_sample = """
*** Test Cases ***
Look at this
    Log Many"""


class InspectTest3(RobotBase, jupyter_kernel_test.KernelTests):
    code_inspect_sample = """
*** Task ***
Look at this
    Log Many"""

# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License
from unittest.mock import patch

import pytest
import jupyter_kernel_test

from irobotframework.magic.robot import cell_magic_tidy

from . import RobotBase, IPythonMagicBase
from .utils import fake_validate


TIDY = "%%tidy\n"


@pytest.mark.parametrize(
    "dirty,expected",
    [
        ("*test case*", "*** test case ***"),
        ("*task*", "*** task ***"),
        ("*tasks*", "*** tasks ***"),
        ("| *test case* |", "*** test case ***"),
        ("| *task* |", "*** task ***"),
        ("| *variable* |", "*** variable ***"),
    ],
)
def test_tidy(dirty, expected):
    clean = cell_magic_tidy(f"{TIDY}{dirty}")["payload"][0]["text"]
    assert clean == expected, "the text is cleaned properly"


REGISTER_MAGIC = """%%python module NotAModule
from irobotframework.magic.robot import register_robot_cell_magic

def magic_shout(code, **kwargs):
    return dict(
        status="ok",
        payload=[
            dict(source="set_next_input", text=code.upper(), replace=True)
        ])

register_robot_cell_magic("SHOUT", r"%%SHOUT", magic_shout)
"""

USE_MAGIC = """%%SHOUT
*** tasks ***
the force should be unrelenting
    Log  fus ro dah
"""

UNREGISTER_MAGIC = """%%python module NotAModule
from irobotframework.magic.robot import unregister_robot_cell_magic

unregister_robot_cell_magic("SHOUT")
"""


class MagicTests(RobotBase, jupyter_kernel_test.KernelTests):
    def test_irobotframework_register_magic(self):
        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=USE_MAGIC)
            assert reply["content"]["status"] == "ok"
            assert not reply["content"]["payload"]
            assert outputs

        reply, outputs = self.execute_helper(code=REGISTER_MAGIC)
        assert reply["content"]["status"] == "ok"

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=USE_MAGIC)
            assert reply["content"]["status"] == "ok"
            assert USE_MAGIC.upper() in reply["content"]["payload"][0]["text"]

        reply, outputs = self.execute_helper(code=UNREGISTER_MAGIC)
        assert reply["content"]["status"] == "ok"

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=USE_MAGIC)
            assert reply["content"]["status"] == "ok"
            assert not reply["content"]["payload"]


FAIL_TEST = """*** tasks ***
Fails
  Should Be Equal as Integers  0  1
"""

WIN_TEST = """*** tasks ***
Wins
  Should Be Equal as Integers  1  1
"""

SET_TEST_COUNT = """
test_count = 10
"""

SO_MUCH_WIN_TEST = """*** tasks ***
{% for i in range(test_count) %}
Win {{ i }}
  Should Be Equal as Integers  1  1
{% endfor %}
"""

PRINT_FOO = "print(foo)"


class MagicReportTests(IPythonMagicBase, jupyter_kernel_test.KernelTests):
    """ A test for using robot magic in ipython
    """

    def execute_magic(self, body, args=""):
        return self.execute_helper(code=f"%%robot {args}\n{body}")

    def test_ipython_robot_magic_fail_noargs(self):
        """ does failing work?
        """
        self.activate_magic()

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_magic(FAIL_TEST)
            assert reply["content"]["status"] != "ok"
            assert outputs

    def test_ipython_robot_magic_win_noargs(self):
        """ does winning work?
        """
        self.activate_magic()

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_magic(WIN_TEST)
            assert reply["content"]["status"] == "ok"
            assert len(outputs) == 4

    def test_ipython_robot_magic_win_assign(self):
        """ does assigning to a local variable work?
        """
        self.activate_magic()

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_magic(WIN_TEST, "-a foo")
            assert reply["content"]["status"] == "ok", reply
            assert outputs

        reply, outputs = self.execute_magic(PRINT_FOO)
        print(reply)
        assert reply["content"]["status"] == "ok", [reply, outputs]

    def test_ipython_robot_magic_fail_noraise(self):
        """ does failing not raise an exception when specified?
        """
        self.activate_magic()

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_magic(FAIL_TEST, "-x")
            assert reply["content"]["status"] == "ok", reply
            assert outputs

    def test_ipython_robot_magic_win_jinja(self):
        """ does jinja work?
        """
        self.activate_magic()

        self.execute_helper(code=USE_MAGIC)
        self.execute_helper(code=SET_TEST_COUNT)

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_magic(SO_MUCH_WIN_TEST, "-j")
            assert reply["content"]["status"] == "ok", reply
            assert len(outputs) == 22

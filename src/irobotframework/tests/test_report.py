# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

from pathlib import Path
from unittest.mock import patch
import subprocess
import sys

import jupyter_kernel_test

from . import RobotBase, IPythonMagicBase
from .utils import fake_validate

KERNELS = Path(sys.prefix) / "share" / "jupyter" / "kernels"

LOGO = KERNELS / "robotframework" / "logo-64x64.png"

IMAGE_TASK = f"""*** Settings ***
Library  OperatingSystem

*** Tasks ***
Make an image
    Copy File  {str(LOGO)}  ${{OUTPUT_DIR}}
    Log  <img src="./{ LOGO.name }">
"""


JSON_TASK = """*** Tasks ***
Make some JSON
    Return some JSON

*** Keywords ***
Return some JSON
    ${json} =  Set Variable   {"a": 1, "b": true, "c": null, "d": [], "e": {}}
    [return]  ${json}
"""

ERROR_TASK = """*** Tasks ***
This will Fail
    This is not a keyword
"""


class ServerBase(object):
    @classmethod
    def setUpClass(cls):
        super(ServerBase, cls).setUpClass()
        cls.proc = subprocess.Popen(
            ["python", "-m", "http.server", "18000", "--bind", "127.0.0.1"]
        )

    @classmethod
    def tearDownClass(cls):
        super(ServerBase, cls).tearDownClass()
        cls.proc.terminate()


class ReportTests(ServerBase, RobotBase, jupyter_kernel_test.KernelTests):
    def test_irobotframework_report_image(self):
        """ does the image reporter work?
        """
        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=IMAGE_TASK, timeout=60)
            assert reply["content"]["status"] == "ok"
            assert any("image/png" in output["content"]["data"] for output in outputs)

    def test_irobotframework_report_json(self):
        """ does the JSON reporter work?
        """
        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=JSON_TASK)
            print(reply, outputs)
            assert reply["content"]["status"] == "ok"
            assert any(
                "application/json" in output["content"]["data"] for output in outputs
            )

    def test_irobotframework_report_error(self):
        """ does the error reporter work?
        """
        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=ERROR_TASK)
            assert reply["content"]["status"] != "ok"
            assert outputs


MAGIC_JSON_TASK = f"""%%robot
{JSON_TASK}
"""

MAGIC_IMAGE_TASK = f"""%%robot
{IMAGE_TASK}
"""

MAGIC_ERROR_TASK = f"""%%robot
{ERROR_TASK}
"""


class MagicReportTests(ServerBase, IPythonMagicBase, jupyter_kernel_test.KernelTests):
    """ A test for using robot magic in ipython
    """

    def test_ipython_robot_report_json(self):
        """ does the JSON reporter work?
        """
        self.activate_magic()

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=MAGIC_JSON_TASK)
            print(reply, outputs)
            assert reply["content"]["status"] == "ok"
            assert any(
                "application/json" in output["content"]["data"] for output in outputs
            )

    def test_ipython_robot_report_image(self):
        """ does the image reporter work?
        """
        self.activate_magic()

        with patch("jupyter_kernel_test.validate_message", fake_validate):
            reply, outputs = self.execute_helper(code=MAGIC_IMAGE_TASK, timeout=60)
            assert reply["content"]["status"] == "ok"
            assert any("image/png" in output["content"]["data"] for output in outputs)

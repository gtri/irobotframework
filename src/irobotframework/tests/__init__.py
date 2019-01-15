# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License


class RobotBase(object):
    """ Common attributes for multiple test cases
    """

    kernel_name = "robotframework"
    language_name = "robotframework"


class IPythonMagicBase(object):
    RELOAD = """%reload_ext irobotframework"""

    kernel_name = "python3"
    language_name = "python"

    def activate_magic(self):
        """ enable robot magic
        """
        reply, outputs = self.execute_helper(code=IPythonMagicBase.RELOAD)
        assert reply["content"]["status"] == "ok"
        assert not outputs

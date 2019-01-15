# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re


def taskify(robot_text):
    """ Make a test case into a task
    """
    return re.sub(r"Test( Case)?", "Task", robot_text)


def fake_validate(msg, msg_type=None, parent_id=None):
    """ You might need to skip validating some messages
    """
    pass

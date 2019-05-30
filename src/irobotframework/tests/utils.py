# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re

import nose.tools as nt
from jupyter_kernel_test import messagespec_common as msc
from jupyter_kernel_test import validate_message as _validate_message


def _data_changed(self, change):
    if isinstance(change, msc.string_types):
        return
    for k, v in change["new"].items():
        assert msc.mime_pat.match(k)
        if "json" in k:
            if v is not None:
                nt.assert_is_instance(
                    v, msc.string_types + (dict, list, bool, int, float)
                )
        else:
            nt.assert_is_instance(v, msc.string_types)


msc.MimeBundle._data_changed = _data_changed


def taskify(robot_text):
    """ Make a test case into a task
    """
    return re.sub(r"Test( Case)?", "Task", robot_text)


def fake_validate(msg, msg_type=None, parent_id=None):
    """ You might need to skip validating some messages
    """
    if msg["msg_type"] == "update_display_data":
        return
    return _validate_message(msg, msg_type, parent_id)

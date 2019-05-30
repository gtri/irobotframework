# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

# Derived from robotkernel
# Copyright (c) 2018, Asko Soukka
# Distributed under the terms of the BSD-3-Clause License

""" An interactive Robot Framework runner
"""
from collections import defaultdict
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import importnb
from robot.running import TestSuiteBuilder
from traitlets.config import LoggingConfigurable

from . import irobot

VDOM_MIME = "application/vdom.v1+json"
ICONS = {"INIT": "▷", "PASS": "⬜", "FAIL": "❌"}
COLORS = {"INIT": "#333", "PASS": "#999", "FAIL": "red"}


class InteractiveRunner(LoggingConfigurable):
    """ An interactive Robot Framework runner
    """

    def __init__(self, silent=False):
        super().__init__()
        self.silent = silent
        self._tmpdir = TemporaryDirectory()
        self.path = Path(self._tmpdir.name)

        self.suite = None
        self.results = None
        self.stdout = None
        self._handlers = defaultdict(list)

        self.test_data = irobot.TestCaseString()

    def __del__(self):
        self._tmpdir.cleanup()

    @property
    def failed(self):
        """ wrapper for crazy-long path
        """
        try:
            return self.results.statistics.total.critical.failed
        except AttributeError:
            return 0

    def populate(self, *code):
        """ Populate with some code lines
        """
        list(map(self.test_data.populate, code))
        return self

    def clear_tests(self):
        """ Clear the tests table
        """
        self.test_data.testcase_table.tests.clear()
        return self

    def build(self, name="Untitled Test Suite"):
        """ Build a test suite
        """
        # pylint: disable=W0212
        self.suite = TestSuiteBuilder()._build_suite(self.test_data)
        self.suite._name = name
        return self

    def on_suite(self, handler):
        """ Set a listener for start events
        """
        self._handlers[irobot.SuiteEventListener].append(handler)

    def on_status(self, handler):
        """ Set a listener for status events
        """
        self._handlers[irobot.StatusEventListener].append(handler)

    def on_return_value(self, handler):
        """ Set a listener for return values
        """
        self._handlers[irobot.ReturnValueListener].append(handler)

    def on_import(self, handler):
        """ Set a listener for imports
        """
        self._handlers[irobot.ImportListener].append(handler)

    def run(self):
        """ Run the built suite
        """
        with importnb.Notebook():
            with StringIO() as stdout:
                self.results = self.suite.run(
                    outputdir=str(self.path),
                    stdout=stdout,
                    listener=sum(
                        [
                            list(map(klass, handlers))
                            for klass, handlers in self._handlers.items()
                        ],
                        [],
                    ),
                )
                self.stdout = stdout.getvalue().strip().splitlines()

        return self


class KernelRunner(InteractiveRunner):
    """ A kernel-aware runner
    """

    def __init__(self, kernel, code, silent=False, history=None):
        super().__init__(silent=silent)
        self.return_values = []
        self.kernel = kernel

        self.populate(*(history or []))
        self.clear_tests()
        self.populate(code)
        self.total_tests = 0
        self.tests_completed = 0
        self.imports = {}

    def run(self):
        """ Actually execute the test cases, and show a progress bar
        """
        display_id = str(uuid4())
        progress = dict(
            tagName="div",
            attributes=dict(style=dict(display="flex", flexWrap="wrap")),
            children=[],
        )

        if not self.silent:

            @self.on_suite
            def on_suite(attributes):
                """ handle the start of a suite
                """
                self.total_tests = attributes["totaltests"]
                progress["children"] = [
                    dict(
                        tagName="div",
                        children=[],
                        attributes=dict(
                            style=dict(
                                borderBottom="solid 1px #eee",
                                flex="1",
                                margin="0.25em",
                                padding="0.25em",
                                minHeight="1.5em",
                            )
                        ),
                    )
                    for i in range(self.total_tests)
                ]
                self.send_display_data({VDOM_MIME: progress}, display_id=display_id)

            @self.on_status
            def on_status(attributes):
                """ handle status responses
                """
                parent = progress["children"][self.tests_completed]

                if "status" in attributes:
                    child = parent["children"][-1]
                    status = attributes["status"]
                    icon = ICONS.get(status, ICONS["FAIL"])
                    child["children"] = icon

                else:
                    status = "INIT"
                    icon = ICONS["INIT"]
                    child = dict(
                        tagName="span",
                        children=icon,
                        attributes=dict(
                            style=dict(marginLeft="0.25em", transition="all 0.2s")
                        ),
                    )

                    parent["children"].append(child)

                child["attributes"]["title"] = f"""{attributes["kwname"]}: {status}"""
                child["attributes"]["style"].update(color=COLORS[status])

                self.send_update_display_data(
                    {VDOM_MIME: progress}, display_id=display_id
                )

            @self.on_return_value
            def on_return_value(name, attributes, return_value=None):
                """ handle a return value
                """
                if "endtime" in attributes:
                    self.return_values.append(return_value)
                    self.tests_completed += 1
                else:
                    progress["children"][self.tests_completed]["attributes"].update(
                        title=name
                    )

            @self.on_import
            def on_import(name, attributes):
                self.imports[name] = attributes

        super().run()

    def send_display_data(self, data=None, metadata=None, display_id=None):
        """ Send some display data to the frontend
        """
        if isinstance(data, str):
            self.kernel.send_response(
                self.kernel.iopub_socket, "display_data", {"data": {"text/plain": data}}
            )
        else:
            self.kernel.send_response(
                self.kernel.iopub_socket,
                "display_data",
                {
                    "data": data or {},
                    "metadata": metadata or {},
                    "transient": {"display_id": display_id},
                },
            )

    def send_update_display_data(self, data=None, metadata=None, display_id=None):
        """ Update a display
        """
        # noqa: E501
        self.kernel.send_response(
            self.kernel.iopub_socket,
            "update_display_data",
            {
                "data": data or {},
                "metadata": metadata or {},
                "transient": {"display_id": display_id},
            },
        )

    def send_execute_result(self, data=None, metadata=None, display_id=None):
        """ Send an execute_response message
        """
        self.kernel.send_response(
            self.kernel.iopub_socket,
            "execute_result",
            {
                "data": data or {},
                "metadata": metadata or {},
                "transient": {"display_id": display_id},
                "execution_count": self.kernel.execution_count,
            },
        )

# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

# Derived from robotkernel
# Copyright (c) 2018, Asko Soukka
# Distributed under the terms of the BSD-3-Clause License


""" Interactive implementations of Robot Framework primitives
"""
import inspect
import os
from io import BytesIO, StringIO
from pathlib import Path

from robot.errors import DataError
from robot.output import LOGGER
from robot.parsing import TestCaseFile
from robot.parsing.model import KeywordTable, TestCaseFileSettingTable, _TestData
from robot.parsing.populators import FromFilePopulator
from robot.parsing.robotreader import RobotReader
from robot.parsing.settings import Fixture
from robot.parsing.tablepopulators import NullPopulator
from robot.tidy import Tidy
from robot.utils import get_error_message


class EventListener(object):
    """ Base Robot Framework event listener
    """

    # pylint: disable=R0903
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, callback):
        self.callback = callback


class SuiteEventListener(EventListener):
    """ A listener for Robot Framework suite events
    """

    # pylint: disable=R0903,W0613
    def start_suite(self, name, attributes):
        """ Called at the start of a suite
        """
        self.callback(attributes)


class StatusEventListener(EventListener):
    """ A listener for Robot Framework status events
    """

    # pylint: disable=R0903,W0613
    def end_keyword(self, name, attributes):
        """ Called at the end of a keyword
        """
        self.callback(attributes)

    def start_keyword(self, name, attributes):
        """ Called at the end of a keyword
        """
        self.callback(attributes)


class ReturnValueListener(EventListener):
    """ A listener for Robot Framework return values
    """

    # pylint: disable=W0613
    def __init__(self, callback):
        super().__init__(callback)
        self.return_value = None

    def end_keyword(self, name, attributes):
        """ Called at the end of a keyword
        """
        frame = inspect.currentframe()
        while frame is not None:
            if "return_value" in frame.f_locals:
                self.return_value = frame.f_locals.get("return_value")
                break
            frame = frame.f_back

    def start_test(self, name, attributes):
        """ Called at the start of a test
        """
        self.callback(name, attributes)

    def end_test(self, name, attributes):
        """ Called at the end of a test
        """
        self.callback(name, attributes, self.return_value)


class ImportListener(EventListener):
    """ A listener for import events
    """

    def library_import(self, name, attributes):
        """ Do something when a library is imported
        """
        self.callback(name, attributes)

    def resource_import(self, name, attributes):
        """ Do something when a resource is imported
        """
        self.callback(name, attributes)


class FromStringPopulator(FromFilePopulator):
    """ A populator for plain old strings
    """

    # pylint: disable=W0231,W0221
    def __init__(self, datafile):
        self._datafile = datafile
        self._populator = NullPopulator()
        self._curdir = os.getcwd()  # Jupyter running directory for convenience

    def populate(self, source):
        """ Populate from the string
        """
        LOGGER.info("Parsing string '%s'." % source)
        try:
            RobotReader().read(BytesIO(source.encode("utf-8")), self)
        except Exception:
            raise DataError(get_error_message())


class TestCaseString(TestCaseFile):
    """ A test case defined in a string
    """

    # pylint: disable=W0221
    def __init__(self, parent=None, source=None):
        source = source or str(Path(os.getcwd()) / "<irobotframework>.robot")
        super().__init__(parent, source)
        self.setting_table = SafeSettingsTable(self)
        self.keyword_table = OverridingKeywordTable(self)
        _TestData.__init__(self, parent, source)

    def populate(self, source):
        """ Populate the test from a string
        """
        FromStringPopulator(self).populate(source)
        return self


class SafeSettingsTable(TestCaseFileSettingTable):
    """ An overloaded settings table
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.suite_setup = OverridingFixture("Suite Setup", self)
        self.suite_teardown = OverridingFixture("Suite Teardown", self)
        self.test_setup = OverridingFixture("Test Setup", self)
        self.test_teardown = OverridingFixture("Test Teardown", self)


class OverridingFixture(Fixture):
    """ An overloaded fixture
    """

    def populate(self, value, comment=None):
        """ Always reset setting before populating it
        """
        self.reset()
        super().populate(value, comment)


class OverridingKeywordTable(KeywordTable):
    """ An overloaded keyword table
    """

    def add(self, name):
        """ Always clear previous definition
        """
        for i in range(len(self.keywords)):
            if self.keywords[i].name == name:
                del self.keywords[i]
                break
        return super().add(name)


class StringTidy(Tidy):
    """ A tidier for in-memory strings
    """

    def file(self, path, output=None):
        data = self._parse_data(path)
        with StringIO() as string_output:
            data.save(output=string_output, format="txt")
            return string_output.getvalue().strip()

    # pylint: disable=W0221
    def _parse_data(self, source):
        """ Always populate from the source
        """
        return TestCaseString().populate(source)

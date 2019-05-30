# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" IPython magics for Robot Framework
"""
import argparse

from IPython import get_ipython
from IPython.core.magic import Magics, cell_magic, magics_class

from ..reporter import KernelReporter
from ..runner import KernelRunner

try:
    from jinja2 import Template
except ImportError:
    Template = None


# magic placeholder for default jinja value
USER_NS = "<user_ns>"


ROBOT_PARSER = argparse.ArgumentParser()
ROBOT_PARSER.add_argument("-s", "--silent", default=0, action="count")
ROBOT_PARSER.add_argument("-x", "--no-raise", default=0, action="count")
ROBOT_PARSER.add_argument("-r", "--return", dest="return_", default=0, action="count")
ROBOT_PARSER.add_argument("-a", "--assign", default=None)

if Template:
    ROBOT_PARSER.add_argument("-j", "--jinja", default=None, const=USER_NS, nargs="?")


class RobotMagicError(RuntimeError):
    """ A custom error that will be thrown by a failing Robot suite
    """


@magics_class
class RobotMagic(Magics):
    """ IPython magics for configuring and executing Robot Framework tests

        Accepts the following command-line style arguments:
        -s --silent            minimize output
        -r --return            return the Runner instance
        -x --no-raise          don't raise an error if a test fails
        -a --assign VAR_NAME   assign to a named variable
        -j --jinja [CONTEXT]   preprocess with Jinja with the user's namespace
                               or given context
    """

    @cell_magic
    def robot(self, line, cell):
        """ Magic for %%robot
        """
        ipy = get_ipython()
        tokens = filter(len, line.strip().split(" "))
        args = ROBOT_PARSER.parse_args(tokens)

        if Template and args.jinja:
            context = ipy.user_ns if args.jinja == USER_NS else ipy.user_ns[args.jinja]
            cell = Template(cell).render(context)

        runner = KernelRunner(ipy.kernel, cell, silent=bool(args.silent))
        runner.build()

        if runner.suite.tests:
            runner.run()
            reporter = KernelReporter(runner, silent=bool(args.silent))
            reporter.report()

        if args.assign:
            ipy.user_ns[args.assign] = runner.results

        if not args.no_raise and runner.failed:
            raise RobotMagicError(runner.failed)

        if args.return_:
            return runner.results

        return None

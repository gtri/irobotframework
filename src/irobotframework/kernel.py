# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

# Derived from robotkernel
# Copyright (c) 2018, Asko Soukka
# Distributed under the terms of the BSD-3-Clause License

""" A Jupyter Kernel for Robot Framework
"""
import json
import re
from pathlib import Path
from collections import OrderedDict
import uuid
from typing import List, Text, Dict

from ipykernel.ipkernel import IPythonKernel
from ipykernel.kernelapp import IPKernelApp

from ._version import __version__
from . import util, docs
from .runner import KernelRunner
from .reporter import KernelReporter
from .completer import Completer
from .completion_finders import get_default_completion_finders

from .magic.robot import PY_MAGIC_RE, default_robot_cell_magics


__all__ = ["RobotKernel"]

HERE = Path(__file__).parent.resolve()
KERNEL_JSON = json.loads((HERE / "resources" / "kernel.json").read_text())
LANGUAGE_INFO = {
    **{k: v for k, v in KERNEL_JSON.items() if k not in ["argv"]},
    "version": __version__,
    "file_extension": ".robot",
}


class RobotKernel(IPythonKernel):
    """ A Jupyter Kernel for Robot Framework
    """

    # pylint: disable=R0913,C0330,R0901,W0212
    implementation = "irobotframework"  # type: Text
    implementation_version = __version__  # type: Text
    language = LANGUAGE_INFO["language"]  # type: Text
    language_version = LANGUAGE_INFO["version"]  # type: Text
    language_info = LANGUAGE_INFO  # type: Dict
    banner = docs.banner()  # type: Text
    help_links = docs.help_links()  # type: List

    _last_cell_id = None  # type: Text

    robot_magics = None  # type: Dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_robot_magics()
        self.robot_history = OrderedDict()
        self.completer = Completer(parent=self)
        self.completer.completion_finders = get_default_completion_finders()

    def init_robot_magics(self):
        """ add the default magics provided by irobotframework
        """
        self.robot_magics = {}
        self.robot_magics["cell"] = default_robot_cell_magics()

    def do_shutdown(self, restart: bool):
        """ Shutdown the kernel
        """
        self.robot_history = OrderedDict()
        return super().do_shutdown(restart)

    def _is_py_cell(self, code: Text):
        """ is this a python cell?
        """
        return re.match(PY_MAGIC_RE, code.strip())

    def init_metadata(self, parent: Dict) -> Dict:
        """ Initialize metadata.

            Run at the beginning of execution requests. We clean any deleted
            cells from robot history so they don't get re-executed.
        """
        metadata = parent.get("metadata", {})
        # capture this, to be immediately consumed by do_execute
        self._last_cell_id = metadata.get("cellId") or str(uuid.uuid4())
        deleted_cells = metadata.get("deletedCells", [])

        for deleted in deleted_cells:
            self.robot_history.pop(deleted, None)

        return super(RobotKernel, self).init_metadata(parent)

    def robot_prehistory(self, cell_id: Text = None) -> List[Text]:
        """ The history of robot syntax, optionally without the current cell
        """
        return [
            code
            for history_id, code in self.robot_history.items()
            if cell_id is None or (cell_id != history_id)
        ]

    def do_execute(
        self,
        code: Text,
        silent: bool,
        store_history: bool = True,
        user_expressions: Dict = None,
        allow_stdin: bool = False,
    ) -> Dict:
        """ Populate/Execute Robot Framework syntax

            Supports `%%python module ModuleName` cell magic
        """
        # capture the cell id, and reset to avoid races
        cell_id = self._last_cell_id or str(uuid.uuid4())
        self._last_cell_id = None

        magic_response = None
        magicked = False

        try:
            for magic_def in self.robot_magics["cell"].values():
                pattern = magic_def["pattern"]
                magic = magic_def["func"]
                match = re.match(pattern, code.strip())
                if match is not None:
                    magic_response = magic(
                        code,
                        silent=silent,
                        store_history=store_history,
                        user_expressions=user_expressions,
                        allow_stdin=allow_stdin,
                    )
                    magicked = True
                    break

            if magicked:
                if isinstance(magic_response, dict):
                    if "execution_count" not in magic_response:
                        magic_response["execution_count"] = self.execution_count
                    if "user_expressions" not in magic_response:
                        magic_response[
                            "user_expressions"
                        ] = self.shell.user_expressions(user_expressions or {})
                    return magic_response

                if isinstance(magic_response, str):
                    code = magic_response
                else:
                    raise NameError(
                        f"don't know what to do with magic response {magic_response}"
                    )

            runner = KernelRunner(
                self, code, silent=silent, history=self.robot_prehistory(cell_id)
            )
        # pylint: disable=W0703
        except Exception as err:
            err_spec = util.format_error(err)
            if not silent:
                self.send_response(self.iopub_socket, "error", err_spec)
            return dict(status="error", **err_spec)

        # Build
        runner.build()

        # Run
        if runner.suite.tests:
            # actually run!
            runner.run()
            self.execution_count += 1
            reply = KernelReporter(runner, silent=silent).report()
        else:
            reply = dict(status="ok", execution_count=self.execution_count)

        self.completer.imports = runner.imports

        # Save history and update reply
        if reply["status"] == "ok":
            self.robot_history[cell_id] = code
            reply.update(
                execution_count=self.execution_count,
                payload=[],
                user_expressions=self.shell.user_expressions(user_expressions or {}),
            )

        return reply

    def do_complete(self, code: Text, cursor_pos: int) -> Dict:
        """ Find completions for what's under the cursor
        """
        if self._is_py_cell(code):
            return super(RobotKernel, self).do_complete(code, cursor_pos)

        return self.completer.do_complete(code, cursor_pos, self.robot_prehistory())

    def do_inspect(self, code: Text, cursor_pos: int, detail_level: int) -> Dict:
        """ Get inspection information for what's under the cursor
        """
        if self._is_py_cell(code):
            return super(RobotKernel, self).do_inspect(code, cursor_pos)

        return self.completer.do_inspect(
            code, cursor_pos, detail_level, self.robot_prehistory()
        )


def launch():
    """ The main kernel entrypoint which uses the App singleton
    """
    IPKernelApp.launch_instance(kernel_class=RobotKernel)


if __name__ == "__main__":
    launch()

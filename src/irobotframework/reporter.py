# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

# Derived from robotkernel
# Copyright (c) 2018, Asko Soukka
# Distributed under the terms of the BSD-3-Clause License

""" (Aspirationally) configurable outputs for interactive Robot Framework
    runs.
"""
from base64 import b64encode
import json
import re

from traitlets.config import LoggingConfigurable

from robot.reporting import ResultWriter

from . import util

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    PIL = None


class InteractiveReporter(LoggingConfigurable):
    """ A minimally configured reporter
    """

    runner = None
    silent = False

    default_handlers = []

    def __init__(self, runner, silent=False, handlers=None):
        super().__init__()
        self.handlers = handlers or self.default_handlers
        self.runner = runner
        self.silent = silent

    def report(self):
        """ Do a report
        """
        for handler in self.handlers:
            handler(self)

        if not self.runner.failed:
            return dict(status="ok")

        return dict(status="error", **clean_robot_error(self.runner.stdout))


class KernelReporter(InteractiveReporter):
    """ A default set of reporters for interactive kernel usage
    """

    @property
    def default_handlers(self):
        """ Some handlers
        """
        return [report_robot_error, report_last_json, report_images, report_html]


def clean_robot_error(err_lines):
    """ Remove ASCII art and meaningless paths for the time being
    """
    # strip the meaningless header
    if len(err_lines) > 2 and err_lines[0].startswith("==="):
        err_lines = err_lines[3:]
    # strip the meaningless footer
    if len(err_lines) > 2 and err_lines[-2].startswith("==="):
        err_lines = err_lines[:-2]

    return {"ename": "", "evalue": "", "traceback": err_lines}


def report_robot_error(reporter):
    """ Reply error on error
    """
    if reporter.runner.failed and not reporter.silent:
        kernel = reporter.runner.kernel
        kernel.send_response(
            kernel.iopub_socket, "error", clean_robot_error(reporter.runner.stdout)
        )


def report_last_json(reporter):
    """ Display result of the last keyword, if it was a JSON string
    """
    return_values = reporter.runner.return_values

    if return_values and return_values[-1] and not reporter.silent:
        try:
            result = json.loads(return_values[-1].strip())
            reporter.runner.send_execute_result({"application/json": result})
        except (AttributeError, ValueError):
            pass


def report_images(reporter):
    """ rewrite the log to use images
    """
    path = reporter.runner.path

    output_path = path / "output.xml"
    xml = output_path.read_text()
    images = [
        name for name in re.findall('img src="([^"]+)', xml) if (path / name).exists()
    ]

    for src in images:
        src_path = path / src
        img = Image.open(str(src_path))
        mimetype = Image.MIME[img.format]
        raw_data = src_path.read_bytes()

        uri = util.data_uri(mimetype, raw_data)
        xml = (
            xml.replace('a href="{}"'.format(src), "a")
            .replace(
                'img src="{}" width="800px"'.format(src),
                'img src="{}" style="max-width:800px;"'.format(uri),
            )
            .replace('img src="{}"'.format(src), 'img src="{}"'.format(uri))
        )

        if not reporter.silent:
            reporter.runner.send_display_data(
                {mimetype: b64encode(raw_data).decode("utf-8")},
                {mimetype: {"height": img.height, "width": img.width}},
            )
    output_path.write_text(xml)


def report_html(reporter):
    """ Generate report
    """
    path = reporter.runner.path

    output_path = path / "output.xml"
    log_path = path / "log.html"
    report_path = path / "report.html"
    writer = ResultWriter(str(output_path))
    writer.write_results(log=str(log_path), report=str(report_path))

    # Clear status and display results
    if not reporter.silent:
        reporter.runner.send_display_data(
            {
                "text/html": ('<a href="{}">Log</a> | <a href="{}">Report</a>').format(
                    util.javascript_uri(
                        log_path.read_bytes().replace(
                            b'"reportURL":"report.html"', b'"reportURL":null'
                        )
                    ),
                    util.javascript_uri(
                        report_path.read_bytes().replace(
                            b'"logURL":"log.html"', b'"logURL":null'
                        )
                    ),
                )
            }
        )

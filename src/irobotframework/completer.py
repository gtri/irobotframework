# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" Completion and Inspection for Robot Framework Keywords
"""
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, List

from IPython import get_ipython
from robot.libdocpkg import LibraryDocumentation
from robot.libdocpkg.htmlwriter import DocFormatter, JsonConverter
from robot.parsing.datarow import DataRow
from robot.parsing.robotreader import RobotReader
from robot.utils.robotpath import find_file
from traitlets.config import LoggingConfigurable

from .doc_template import DOC_CONTEXT, KW_TEMPLATE, LIB_TEMPLATE
from .util import find_line

SKIP_LIBS = ["Remote"]
RE_IMPORT = r"^\|?\s*(library|resource) ( +|\|)\s*([^ \n]+)"


def register_robot_completion_finder(
    completion_finder: Callable, before: Callable = None, after: Callable = None
):
    """ Add a completion finder

        specify an existing finder with `before` or `after` to fine-tune the
        order in which the finder will have the opportunity to return its matches
    """

    kernel = get_ipython().kernel
    finders = kernel.completer.completion_finders

    if completion_finder in finders:
        kernel.completer.completion_finders.remove(completion_finder)

    if before in finders:
        index = finders.index(before)
    elif after in finders:
        index = finders.index(after) + 1
    else:
        index = 0

    kernel.completer.completion_finders.insert(index, completion_finder)


def unregister_robot_completion_finder(completion_finder: Callable):
    """ Remove a completion finder
    """
    kernel = get_ipython().kernel
    kernel.completer.completion_finders.remove(completion_finder)


class Completer(LoggingConfigurable):
    """ A reusable keyword intelligence provider
    """

    _doc_cache = None  # type: dict
    imports = None  # type: dict
    completion_finders = None  # type: List

    def do_complete(self, code: str, cursor_pos: int, history: List[str]) -> dict:
        """ Handle complete_request payload and return a message spec for a
            set of completions
        """
        matches = []

        line, line_cursor, offset = find_line(code, cursor_pos)

        self.docs(history + [code])

        matches = None
        experimental_matches = None
        metadata = {}

        for finder in self.completion_finders or []:
            try:
                matches, experimental_matches = finder(
                    completer=self,
                    line=line,
                    code=code,
                    cursor_pos=cursor_pos,
                    line_cursor=line_cursor,
                    offset=offset,
                    history=history,
                )
            except Exception as err:
                self.log.error(f"{finder} encountered an error: {err}")

            if matches:
                break

        if experimental_matches:
            metadata = {"_jupyter_types_experimental": experimental_matches}

        return {
            "matches": matches,
            "cursor_end": cursor_pos,
            "cursor_start": offset,
            "metadata": metadata,
            "status": "ok",
        }

    def do_inspect(
        self, code: str, cursor_pos: int, detail_level: int, history: List[str]
    ) -> dict:
        """ Handle inspect payload and return a message spec with some docs
            set of completions
        """
        doc = None

        line, line_cursor, offset = find_line(code, cursor_pos)
        tokens = DataRow(RobotReader.split_row(line)).data

        self.docs(history + [code])

        if len(tokens) > 1:
            if tokens[0].lower() in ["library"]:
                doc = self._lib_html(tokens[1], history)
            elif tokens[0].lower() in ["resource"]:
                source = None
                try:
                    source = find_file(tokens[1])
                except Exception:
                    pass

                if source is not None:
                    doc = self._lib_html(source, history)

        if not doc:
            doc = self._keyword_html(tokens, code, line, line_cursor, offset, history)

        if doc is not None:
            return {
                "status": "ok",
                "data": {"text/html": doc},
                "metadata": {},
                "found": True,
            }
        else:
            return {"status": "ok", "data": {}, "metadata": {}, "found": False}

    def docs(self, history=[]):
        """ Return the docs available from cached, imported libraries and
            and history of the current run
        """
        if self._doc_cache is None:
            self._doc_cache = {}
            for lib in ["BuiltIn"]:
                self._load_libdoc(lib)
        self._update_imports(history)

        docs = dict(**self._doc_cache, **self._history_docs(history))

        return docs

    def _load_libdoc(self, name, source=None, use_cache=True):
        """ Try to load a libdoc, either by name, or named source. Tries to use
            the cache.
        """
        strategies = [name]

        if source is not None and source.endswith(".robot"):
            try:
                strategies += [find_file(source)]
            except Exception:
                pass

        for strategy in strategies:
            if use_cache and strategy in self._doc_cache:
                return self._doc_cache[strategy]

            try:
                libdoc = LibraryDocumentation(strategy)
                self._doc_cache[strategy] = self._doc_cache[name] = libdoc
                return libdoc
            except Exception as err:
                pass
                self.log.debug("Could not load libdoc for %s: %s", strategy, err)

    def _lib_html(self, libname: str, history: List[str]) -> str:
        """ Return documentation for a library (or keyword)

            TODO: keywords, variables
        """
        found = None
        for name, libdoc in self.docs(history).items():
            if libname.lower().strip() == name.lower().strip():
                found = libdoc
                break

        found = found or self._load_libdoc(libname)

        if found is None:
            return

        formatter = DocFormatter(found.keywords, found.doc, found.doc_format)
        libdoc_json = JsonConverter(formatter).convert(found)
        return LIB_TEMPLATE.render(libdoc=libdoc_json, **DOC_CONTEXT)

    def _keyword_html(self, tokens, code, line, line_cursor, offset, history):
        for name, libdoc in self.docs(history).items():
            for kw in libdoc.keywords:
                for token in filter(str, tokens):
                    if kw.name.lower() == token.lower():
                        formatter = DocFormatter([kw], libdoc.doc, libdoc.doc_format)
                        libdoc_json = JsonConverter(formatter).convert(libdoc)
                        libdoc_json["keywords"] = [
                            libkw
                            for libkw in libdoc_json["keywords"]
                            if libkw["name"] == kw.name
                        ]
                        return KW_TEMPLATE.render(libdoc=libdoc_json, **DOC_CONTEXT)

    def _update_imports(self, history=[]):
        for impname, imp in (self.imports or {}).items():
            if impname not in SKIP_LIBS:
                source = imp.get("source")
                if source is not None and source.endswith(".robot"):
                    try:
                        source = find_file(source)
                    except Exception:
                        pass

                self._load_libdoc(impname, source=source)

        for match in re.findall(RE_IMPORT, "\n".join(history), flags=re.I | re.M):
            self._load_libdoc(match[2])

    def _history_docs(self, history: List[str] = None) -> dict:
        hist_with_keywords = self._history_with_keywords(history)
        if not hist_with_keywords:
            return {}

        hist_libdoc = self._history_libdoc(hist_with_keywords)

        if hist_libdoc is None:
            return {}

        return {"__main__": hist_libdoc}

    def _history_libdoc(self, history: List[str]):
        libdoc = None
        keywords = {}

        with TemporaryDirectory() as td:
            tdp = Path(td)
            for i, hist in enumerate(history):
                tmp_lib = tdp / f"{i}.robot"
                tmp_lib.write_text(hist)
                libdoc = self._load_libdoc(str(tmp_lib), use_cache=False)
                if libdoc is None:
                    continue
                for kw in getattr(libdoc, "keywords", []):
                    keywords[kw.name] = kw

        if libdoc is None or not keywords:
            return None

        libdoc.keywords = keywords.values()

        return libdoc

    def _history_with_keywords(self, history: List[str] = None) -> List[str]:
        for hist in history or []:
            if re.match(r"^\*+\s*keywords", hist, flags=re.I):
                yield hist

    def _history_with_imports(self, history: List[str] = None) -> List[str]:
        for hist in history or []:
            if re.match(r"^\*+\s*(library|resource)", hist, flags=re.I):
                yield hist

# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

from nbformat import NO_CONVERT, reads, write

from . import DOCS, TOOLS


def strip():
    """ Remove outputs and execution counts from notebook files, as robot
        notebooks are _really_ huge and unreproducible.
    """
    for root in [DOCS, TOOLS]:
        for ipynb_file in root.rglob("*.ipynb"):
            nbf = reads(ipynb_file.read_text(), NO_CONVERT)
            changed = False
            for cell in nbf.cells:
                if cell.cell_type == "code":
                    if cell.outputs:
                        cell.outputs = []
                        changed = True
                    if cell.execution_count:
                        cell.execution_count = None
                        changed = True
            if changed:
                print(f"remove outputs/execution counts from {ipynb_file}")
                write(nbf, str(ipynb_file))


if __name__ == "__main__":
    strip()

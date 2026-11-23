"""Make the student version of a LUA101 graded notebook from its source in solutions/.

Usage, from the repository's root with the notebook environment active:

    python courses/lua101/tools/student_version.py \
        courses/lua101/solutions/pa1/pa1.ipynb courses/lua101/assignments/pa1/pa1.ipynb

The script applies nbgrader's preprocessors with the settings in the course's
``nbgrader_config.py``:

- ``ClearSolutions`` replaces each region between ``-- BEGIN SOLUTION`` and ``-- END SOLUTION``
  with ``-- YOUR CODE HERE`` and ``error("not implemented")``, and each Markdown answer with
  ``YOUR ANSWER HERE``;
- ``ClearHiddenTests`` removes each region between ``-- BEGIN HIDDEN TESTS`` and
  ``-- END HIDDEN TESTS``;
- ``LockCells`` marks the test cells and other locked cells read-only;
- ``ClearOutput`` removes every output.

It also drops the source's Jupytext pairing, because students receive the notebook alone. Never
edit a student version by hand: change the source, then run this script again. To check that a
committed student version is current, write a fresh one to a temporary path and compare the two
with ``diff``.
"""

from __future__ import annotations

import pathlib
import sys

import nbformat
from nbgrader.preprocessors import ClearHiddenTests, ClearOutput, ClearSolutions, LockCells
from traitlets.config.loader import PyFileConfigLoader

COURSE = pathlib.Path(__file__).resolve().parent.parent


def student_version(source: pathlib.Path, target: pathlib.Path) -> None:
    config = PyFileConfigLoader("nbgrader_config.py", path=str(COURSE)).load_config()
    notebook = nbformat.read(source, as_version=4)
    resources: dict = {}
    for preprocessor in (ClearSolutions, ClearHiddenTests, LockCells, ClearOutput):
        notebook, resources = preprocessor(config=config).preprocess(notebook, resources)
    notebook.metadata.pop("jupytext", None)
    target.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, target)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    student_version(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
    print(f"wrote {sys.argv[2]}")

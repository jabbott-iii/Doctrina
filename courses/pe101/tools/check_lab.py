"""Check a PE101 lab two ways: as students get it, and with its answer key.

Usage, from the repository's root with the notebook environment active:

    python courses/pe101/tools/check_lab.py \
        courses/pe101/modules/01-how-models-produce-text/lab01.ipynb \
        courses/pe101/solutions/labs/lab01_answers.py

1. The lab runs from top to bottom in a fresh kernel exactly as students receive it. Only cells
   tagged ``raises-exception`` may fail: the checks, before their exercise is done, and cells
   that show an error on purpose.
2. Every cell tagged ``answer-<id>`` in the lab is replaced by the cell with the same tag in the
   answer key, and the lab runs again. This time no cell may fail, whatever its tags, so every
   check passes with the key's answers.

The answer key is a Jupytext file kept in ``solutions/``, away from the coursework. The script
changes no file; it runs copies of the notebook in memory. Cells still run in the lab's folder,
so files the lab writes (in its ``scratch`` folder) appear there.
"""

from __future__ import annotations

import copy
import pathlib
import sys

import jupytext
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


def answer_tags(cell) -> list[str]:
    return [tag for tag in cell.metadata.get("tags", []) if tag.startswith("answer-")]


def run(notebook, folder: pathlib.Path, *, strict: bool) -> None:
    client = NotebookClient(
        notebook,
        timeout=300,
        kernel_name="python3",
        resources={"metadata": {"path": str(folder)}},
        force_raise_errors=strict,
    )
    client.execute()


def main(lab_path: str, key_path: str) -> int:
    lab = pathlib.Path(lab_path).resolve()
    student = nbformat.read(lab, as_version=4)

    try:
        run(copy.deepcopy(student), lab.parent, strict=False)
    except CellExecutionError as error:
        print(f"{lab.name}: a cell failed that isn't tagged raises-exception:\n{error}")
        return 1
    print(f"{lab.name}: runs as students receive it")

    key = {tag: cell for cell in jupytext.read(key_path).cells for tag in answer_tags(cell)}
    solved = copy.deepcopy(student)
    used = set()
    for cell in solved.cells:
        for tag in answer_tags(cell):
            if tag not in key:
                print(f"{lab.name}: the key has no cell tagged {tag}")
                return 1
            if key[tag].cell_type != cell.cell_type:
                print(f"{lab.name}: {tag} is a {cell.cell_type} cell in the lab but not in the key")
                return 1
            cell.source = key[tag].source
            used.add(tag)
    unused = sorted(set(key) - used)
    if unused:
        print(f"{lab.name}: the key has answers for tags the lab doesn't use: {', '.join(unused)}")
        return 1

    try:
        run(solved, lab.parent, strict=True)
    except CellExecutionError as error:
        print(f"{lab.name}: a cell failed with the key's answers:\n{error}")
        return 1
    print(f"{lab.name}: every cell runs and every check passes with the key ({len(used)} answers)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))

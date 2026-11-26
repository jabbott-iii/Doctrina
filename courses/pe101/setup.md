# Setting up your environment

You need one thing for this course: a Python environment that runs the lab notebooks. You don't
need an account, an API key, or a network connection after the packages are installed, because no
part of the course calls a language model. Set the environment up before you start Module 1. The
commands below are for Linux and macOS; on Windows, run them inside the Windows Subsystem for
Linux (WSL).

Run every command from the root folder of the repository that holds the course, the folder with
`requirements.txt` in it.

## The notebook environment

The labs are Jupyter notebooks in Python 3.12. Besides Jupyter, they use four packages:
matplotlib for figures, jsonschema to check structured output, PyYAML to read the front matter of
configuration files, and `promptlab`, a small package written for this course. `promptlab` holds
the stand-ins that answer the labs' requests in place of a model, and the loaders for the course's
data.

1. Install Python 3.12 and [uv](https://docs.astral.sh/uv/), a Python package installer.
2. Create the environment and install the course's packages:

   ```bash
   uv venv .venv --python 3.12
   ```

   ```bash
   VIRTUAL_ENV=.venv uv pip install -r requirements.txt
   ```

   The second command ends by listing the packages it installed. It installs `promptlab` from
   the course's folder in editable mode (`-e`), so the labs use the copy in
   `courses/pe101/promptlab/` that you can read.
3. Check `promptlab` with its own tests:

   ```bash
   .venv/bin/pytest -q courses/pe101/promptlab
   ```

   The last line reports how many tests passed, and none failed.
4. Start JupyterLab:

   ```bash
   .venv/bin/jupyter lab
   ```

   JupyterLab opens in your browser.
5. Open the first lab, `courses/pe101/modules/01-how-models-produce-text/lab01.ipynb`, and run
   its setup cell. It prints the versions of Python and the packages the lab uses.

## Running a lab

- Run a lab's cells in order, from the top. If you change an earlier cell, run it again before the
  cells after it.
- Each exercise ends with a check cell. Run it after your answer: it prints `passed`, or it fails
  with a message that says what is wrong. Until you answer an exercise, its check fails on
  purpose.
- To start a lab over, choose **Kernel** > **Restart Kernel and Clear Outputs of All Cells** in
  JupyterLab, then run the cells again from the top.
- Labs never send anything over the network. Where a lab says "the model" answers, a stand-in
  from `promptlab` answers from a script, and the lab says so.

## No coding agent needed

Modules 12 and 13 teach you to prompt and configure Claude Code, a coding agent. Their labs run
offline too, with every check done in code, so you don't need Claude Code installed, and the
course never asks you to run it.

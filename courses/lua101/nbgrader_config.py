"""nbgrader settings for LUA101's graded notebooks.

Every graded cell in this course is a ``%%lua`` cell in a Python notebook, so
the stub that replaces a solution must be Lua, even though nbgrader files it
under the kernel's language, Python. The solution and hidden-test markers are
Lua comments: ``-- BEGIN SOLUTION`` and ``-- BEGIN HIDDEN TESTS``.

Make a student version from a source notebook in ``solutions/`` with
``tools/student_version.py``, which applies nbgrader's preprocessors with these
settings.
"""

c = get_config()  # noqa: F821 (nbgrader and nbconvert define get_config)

c.ClearSolutions.code_stub = {"python": '-- YOUR CODE HERE\nerror("not implemented")'}
c.ClearSolutions.text_stub = "YOUR ANSWER HERE"
c.ClearSolutions.enforce_metadata = True

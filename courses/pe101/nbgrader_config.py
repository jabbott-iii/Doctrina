"""nbgrader settings for PE101's graded notebooks.

The assignments are Python notebooks, so nbgrader's own markers and stubs apply: a solution sits
between ``### BEGIN SOLUTION`` and ``### END SOLUTION``, and the student version replaces it with
``# YOUR CODE HERE`` and ``raise NotImplementedError()``. Hidden tests sit between
``### BEGIN HIDDEN TESTS`` and ``### END HIDDEN TESTS``.

Make a student version from a source notebook in ``solutions/`` with ``tools/student_version.py``,
which applies nbgrader's preprocessors with these settings.
"""

c = get_config()  # noqa: F821 (nbgrader and nbconvert define get_config)

c.ClearSolutions.code_stub = {"python": "# YOUR CODE HERE\nraise NotImplementedError()"}
c.ClearSolutions.text_stub = "YOUR ANSWER HERE"
c.ClearSolutions.enforce_metadata = True

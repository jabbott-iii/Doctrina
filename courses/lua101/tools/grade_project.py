"""Grade a LUA101 Lua project: its hidden tests, and the student's tests against broken versions.

Usage, from the repository's root with the notebook environment active:

    python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa3 path/to/submission
    python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa3 --self-test

The first argument is the project's folder in ``solutions/``. It holds the model solution, the
hidden tests, a model student test suite in ``spec/``, and ``grading.json``:

- ``files``: the solution's files, relative to the project's folder, such as ``["iter.lua"]`` or
  ``["src/csvstats.lua", "bin/csvstats"]``. The first is the main module.
- ``hidden_spec``: the file of hidden tests.
- ``busted_args``: options for every busted run, such as ``["--lpath=./src/?.lua"]``.
- ``broken``: the broken versions. Each is the model with one replacement, ``old`` to ``new``, in
  ``file`` (the main module if absent), which must match exactly once.
- ``tooling``: ``true`` to also run the module 11 tools on the whole submission folder.

A submission is a folder laid out as the handout asks. The script prints:

1. **Hidden tests.** It runs the hidden tests against the submission's files, one describe block
   at a time, so that an endless loop in one part costs only that part's points. Each block's name
   ends with its points, as in ``iter.take (10 points)``, and earns them in proportion to the
   tests in it that pass.
2. **The student's tests, for the rubric's Tests criterion.** It runs the student's specs against
   the model, where every test should pass, and against each broken version. A broken version is
   caught when at least one of the student's tests fails on it.
3. **Tooling,** when ``tooling`` is set: whether the rockspec lints and builds, and whether
   luacheck, StyLua, and lua-language-server find nothing, with LuaCov's coverage of the main
   module, for the rubric.

``--self-test`` grades the model with the model tests, which should earn every point and catch
every broken version. The script changes no file outside temporary folders. Each busted run stops
after 60 seconds, which only an endless loop reaches; a run that times out counts as failing.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_project  # noqa: E402  (the module beside this script)

LUA_BIN = pathlib.Path(sys.prefix) / "lua" / "bin"
ENV = dict(os.environ, PATH=f"{LUA_BIN}{os.pathsep}{os.environ['PATH']}")


def find(name, *folders):
    for folder in (LUA_BIN, *folders):
        if (pathlib.Path(folder) / name).exists():
            return str(pathlib.Path(folder) / name)
    return shutil.which(name)


BUSTED = find("busted")


def lua_pattern(text: str) -> str:
    """Escapes the characters that are magic in Lua patterns."""
    return re.sub(r"([\^$()%.\[\]*+\-?])", r"%\1", text)


class Project:
    def __init__(self, folder: pathlib.Path):
        self.folder = folder
        self.config = json.loads((folder / "grading.json").read_text())
        self.files = self.config.get("files") or [self.config["module"]]
        self.model = {name: (folder / name).read_text() for name in self.files}
        self.hidden = folder / self.config["hidden_spec"]
        self.busted_args = self.config.get("busted_args", [])

    def broken_versions(self):
        for broken in self.config["broken"]:
            name = broken.get("file", self.files[0])
            if self.model[name].count(broken["old"]) != 1:
                sys.exit(f"broken version {broken['description']!r} no longer matches {name}; "
                         "update grading.json")
            sources = dict(self.model)
            sources[name] = sources[name].replace(broken["old"], broken["new"])
            yield broken["description"], sources

    def run_busted(self, sources: dict[str, str], specs: list[pathlib.Path], *options: str):
        """Runs the specs against one version of the solution in a fresh folder; returns busted's
        report, or None if it timed out."""
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            for name, text in sources.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text)
            (root / "spec").mkdir()
            for spec in specs:
                shutil.copy(spec, root / "spec" / spec.name)
            try:
                result = subprocess.run([BUSTED, "-o", "json", *self.busted_args, *options],
                                        cwd=root, env=ENV, capture_output=True, text=True,
                                        timeout=60)
            except subprocess.TimeoutExpired:
                return None
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"successes": [], "failures": [],
                        "errors": [{"name": result.stderr.strip() or result.stdout.strip()}]}


def failed(report) -> bool:
    return report is None or bool(report["failures"] or report["errors"])


def hidden_points(project: Project, sources: dict[str, str]) -> None:
    blocks = re.findall(r'describe\("(([^"]+?) \((\d+) points\))"', project.hidden.read_text())
    possible = sum(int(worth) for _, _, worth in blocks)
    score, failures = 0.0, []
    print("Hidden tests:")
    for name, _, worth in blocks:
        report = project.run_busted(sources, [project.hidden], f"--filter=^{lua_pattern(name)} ")
        if report is None:
            print(f"  {name:44} timed out: an endless loop   0.00 points")
            continue
        passed = len(report["successes"])
        total = passed + len(report["failures"]) + len(report["errors"])
        earned = int(worth) * passed / total if total else 0.0
        score += earned
        failures += report["failures"] + report["errors"]
        print(f"  {name:44} {passed:2} of {total:2} tests pass   {earned:5.2f} points")
    for test in failures:
        print(f"  FAILED: {test.get('name', '?')}")
    print(f"  Total: {score:.2f} of {possible} points")


def student_tests(project: Project, specs: list[pathlib.Path]) -> None:
    print("The student's tests:")
    if not specs:
        print("  no spec files found: the Tests criterion scores 0")
        return
    on_model = project.run_busted(project.model, specs)
    if on_model is None:
        print("  busted timed out on the model solution")
    else:
        count = sum(len(on_model[k]) for k in ("successes", "failures", "errors"))
        print(f"  on the model solution: {len(on_model['successes'])} of {count} tests pass")
        for test in on_model["failures"] + on_model["errors"]:
            print(f"    WRONG TEST, fails on a correct solution: {test.get('name', '?')}")
    caught = 0
    for description, sources in project.broken_versions():
        hit = failed(project.run_busted(sources, specs))
        caught += hit
        print(f"  {'caught' if hit else 'MISSED'}: {description}")
    print(f"  Caught {caught} of {len(project.config['broken'])} broken versions")


def tooling(project: Project, submission: pathlib.Path) -> None:
    """Runs check_project.py's checks on a copy of the whole submission folder."""
    print("Tooling:")
    check_project.check(submission, busted_args=project.busted_args,
                        ignore=(project.config["hidden_spec"], "grading.json", "README.md"))


def main(argv: list[str]) -> None:
    if not BUSTED:
        sys.exit("busted wasn't found; install it as setup.md describes")
    if len(argv) != 2:
        sys.exit(__doc__)
    project = Project(pathlib.Path(argv[0]))
    if argv[1] == "--self-test":
        submission = project.folder
        sources, specs = project.model, sorted((project.folder / "spec").glob("*_spec.lua"))
    else:
        submission = pathlib.Path(argv[1])
        sources = {name: (submission / name).read_text() for name in project.files
                   if (submission / name).exists()}
        specs = sorted((submission / "spec").glob("*_spec.lua"))
    hidden_points(project, sources)
    student_tests(project, specs)
    if project.config.get("tooling"):
        tooling(project, submission)


if __name__ == "__main__":
    main(sys.argv[1:])

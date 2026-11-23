"""Check a Lua project the way LUA101 grades it: its rock, lint, layout, types, and coverage.

Usage, from the repository's root with the notebook environment active:

    python courses/lua101/tools/check_project.py path/to/project
    python courses/lua101/tools/check_project.py path/to/project --lpath='./src/?.lua'

The project is a folder with a rockspec, its Lua code (usually in ``src/``, with commands in
``bin/``), its tests in ``spec/``, and the settings ``.luacheckrc``, ``stylua.toml``, and
``.luacov``. The script works on a copy, so it changes nothing in the project, and runs:

1. ``luarocks lint`` and ``luarocks --tree lua_modules make`` on the first ``*.rockspec``;
2. ``luacheck`` on every ``.lua`` file and every file in ``bin/``;
3. ``stylua --check`` on the same files;
4. ``lua-language-server --check`` on ``src/``, or on the whole folder if there is no ``src/``;
5. if ``.luacov`` exists, ``busted --coverage`` with the given options, then ``luacov``, and
   prints each file's coverage and the number of lines the tests never ran.

It prints ``ok`` or ``FAIL`` for each check, with the first lines of each failure, and exits with
status 0 only if every check passed. Students can run it on their own projects before they submit;
``grade_project.py`` runs the same checks for the rubric.
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

LUA_BIN = pathlib.Path(sys.prefix) / "lua" / "bin"
ENV = dict(os.environ, PATH=f"{LUA_BIN}{os.pathsep}{os.environ['PATH']}")


def find(name, *folders):
    for folder in (LUA_BIN, *folders):
        if (pathlib.Path(folder) / name).exists():
            return str(pathlib.Path(folder) / name)
    return shutil.which(name)


TOOLS = {
    "busted": find("busted"),
    "luarocks": find("luarocks"),
    "luacheck": find("luacheck"),
    "luacov": find("luacov"),
    "stylua": find("stylua", pathlib.Path.home() / ".cargo" / "bin"),
    "lua-language-server": find("lua-language-server", pathlib.Path(sys.prefix) / "luals" / "bin"),
}


def check(project: pathlib.Path, busted_args=(), ignore=()) -> bool:
    """Runs every check on a copy of the project; prints the results; returns True if all pass."""
    with tempfile.TemporaryDirectory() as folder:
        root = pathlib.Path(folder) / "project"
        shutil.copytree(project, root, ignore=shutil.ignore_patterns(
            "lua_modules", "luacov.*.out", ".git", *ignore))

        def run(tool, *args, timeout=300):
            if not TOOLS[tool]:
                return 1, f"{tool} wasn't found; install it as setup.md describes"
            try:
                result = subprocess.run([TOOLS[tool], *args], cwd=root, env=ENV,
                                        capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                return 1, f"{tool} didn't finish in {timeout} seconds"
            return result.returncode, result.stdout + result.stderr

        rockspecs = sorted(root.glob("*.rockspec"))
        code = [str(p.relative_to(root)) for p in sorted(root.rglob("*"))
                if p.is_file() and (p.suffix == ".lua" or p.parent.name == "bin")]
        checks = []
        if rockspecs:
            checks.append(("luarocks lint", run("luarocks", "lint", rockspecs[0].name)))
            checks.append(("luarocks make", run("luarocks", "--tree", "lua_modules", "make",
                                                rockspecs[0].name)))
        else:
            checks.append(("rockspec", (1, "no *.rockspec file in the project")))
        checks.append(("luacheck", run("luacheck", "--no-color", *code)))
        checks.append(("stylua --check", run("stylua", "--check", *code)))
        target = root / "src" if (root / "src").is_dir() else root
        report = pathlib.Path(folder) / "luals.json"
        status, output = run("lua-language-server", f"--check={target}", "--checklevel=Warning",
                             "--check_format=json", f"--check_out_path={report}",
                             f"--logpath={pathlib.Path(folder) / 'luals-log'}")
        if report.exists() and report.stat().st_size > 2:
            found = json.loads(report.read_text())
            output = "\n".join(f"{uri.rsplit('/', 1)[-1]}:{item['range']['start']['line'] + 1}: "
                               f"{item['code']}" for uri, items in found.items() for item in items)
        checks.append(("lua-language-server", (status, output)))
        passed = True
        for name, (status, output) in checks:
            print(f"  {'ok  ' if status == 0 else 'FAIL'} {name}")
            if status != 0:
                passed = False
                for line in output.strip().splitlines()[:8]:
                    print(f"         {line}")
        if (root / ".luacov").exists():
            status, output = run("busted", "--coverage", *busted_args)
            print(f"  {'ok  ' if status == 0 else 'FAIL'} busted --coverage")
            if status != 0:
                passed = False
                for line in output.strip().splitlines()[-8:]:
                    print(f"         {line}")
            run("luacov")
            report_file = root / "luacov.report.out"
            if report_file.exists():
                text = report_file.read_text()
                body, _, summary = text.partition("Summary")
                for match in re.finditer(r"^(\S+\.lua)\s+(\d+)\s+(\d+)\s+([\d.]+%)", summary, re.M):
                    print(f"  coverage of {match.group(1)}: {match.group(4)}")
                missed = [line for line in body.splitlines() if re.match(r"\*+0 ", line)]
                print(f"  lines the tests never ran: {len(missed)}")
        else:
            print("  coverage: no .luacov file in the project")
        return passed


def main(argv: list[str]) -> None:
    if not argv or argv[0].startswith("-"):
        sys.exit(__doc__)
    project = pathlib.Path(argv[0])
    print(f"Checking {project}:")
    sys.exit(0 if check(project, busted_args=argv[1:]) else 1)


if __name__ == "__main__":
    main(sys.argv[1:])

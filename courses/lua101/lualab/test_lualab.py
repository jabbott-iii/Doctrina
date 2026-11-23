"""Tests for lualab: run them with ``pytest courses/lua101/lualab``."""

import pytest

import lualab


@pytest.fixture(autouse=True)
def fresh_states():
    for version in ("5.4", "5.1"):
        lualab.reset(version)


def test_print_and_io_write_reach_python_stdout(capsys):
    lualab.run('print("a", 1, 1.0)\nio.write(1.0, " b\\n")\nio.stdout:write("c\\n")')
    # io.write formats floats with "%.14g", so 1.0 prints as "1" there but "1.0" in print.
    assert capsys.readouterr().out == "a\t1\t1.0\n1 b\nc\n"


def test_stderr_is_captured_separately(capsys):
    lualab.run('local f = io.stderr\nf:write("warning\\n")')
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "warning\n"


def test_a_call_cell_shows_its_results_as_lua_i_does(capsys):
    # io.write returns its file, which lua -i also prints after the text.
    lualab.run('io.write("x\\n")')
    assert capsys.readouterr().out.startswith("x\nfile (0x")


def test_state_persists_between_cells(capsys):
    lualab.run("count = 41\nlocal hidden = 1")
    lualab.run("print(count + 1, hidden)")
    assert capsys.readouterr().out == "42\tnil\n"


def test_an_expression_cell_shows_its_values(capsys):
    lualab.run("1 + 2, 7 // 2, 7 / 2")
    assert capsys.readouterr().out == "3\t3\t3.5\n"


def test_a_statement_cell_shows_nothing(capsys):
    lualab.run("local x = 1")
    assert capsys.readouterr().out == ""


def test_runtime_error_names_the_cell_line():
    with pytest.raises(lualab.LuaError, match=r"^cell:2: attempt to perform arithmetic on a nil"):
        lualab.run("local a = 1\nlocal b = a + nothing")


def test_failed_assert_raises_with_its_message():
    with pytest.raises(lualab.LuaError, match=r"^cell:1: expected 4\nstack traceback:"):
        lualab.run('assert(2 + 2 == 5, "expected 4")')


def test_syntax_error_raises():
    with pytest.raises(lualab.LuaError, match=r"cell:1: .*near"):
        lualab.run("local = 3")


def test_output_before_an_error_is_kept(capsys):
    with pytest.raises(lualab.LuaError):
        lualab.run('print("before")\nerror("boom")')
    assert capsys.readouterr().out == "before\n"


def test_error_objects_use_tostring():
    code = 'error(setmetatable({}, {__tostring = function() return "custom" end}))'
    with pytest.raises(lualab.LuaError, match=r"^custom"):
        lualab.run(code)
    with pytest.raises(lualab.LuaError, match=r"^\(error object is a table value\)"):
        lualab.run("error({})")


def test_no_python_global_and_os_exit_is_disabled(capsys):
    lualab.run("print(python)")
    assert capsys.readouterr().out == "nil\n"
    with pytest.raises(lualab.LuaError, match="os.exit would stop"):
        lualab.run("os.exit(1)")


def test_versions_have_separate_states(capsys):
    lualab.run("print(_VERSION, #{1, nil, 3})", version="5.1")
    lualab.run("print(_VERSION)")
    assert capsys.readouterr().out == "Lua 5.1\t3\nLua 5.4\n"


def test_reset_clears_globals(capsys):
    lualab.run("x = 1")
    lualab.reset()
    lualab.run("print(x)")
    assert capsys.readouterr().out == "nil\n"


def test_magic_shows_lua_errors_and_fails_the_cell(capsys):
    from IPython.testing.globalipapp import start_ipython

    shell = start_ipython()
    shell.run_line_magic("load_ext", "lualab")
    result = shell.run_cell('%%lua\nassert(1 == 2, "one is not two")')
    assert not result.success
    assert "LuaError: cell:1: one is not two" in capsys.readouterr().out


def test_unknown_version_is_rejected():
    with pytest.raises(ValueError, match="unknown Lua version"):
        lualab.run("print(1)", version="6.0")

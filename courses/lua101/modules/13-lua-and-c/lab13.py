# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: tags,-all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lab 13: Lua and C
#
# **Objectives:** LO-13.1, LO-13.2, LO-13.3, LO-13.4\
# **Prerequisites:** the [Module 13 reading](index.md), a C compiler (`gcc` or `clang`), and Lua
# 5.4 installed as [setting up](../../setup.md) describes; the lab needs Linux or macOS\
# **Time:** about 2 hours
#
# You will predict how a sequence of C API calls changes the stack, write a C module with two
# checked functions, finish a C program that runs a Lua script and survives its errors, and write a
# userdata type whose memory the garbage collector frees. Each exercise writes a C file into the
# lab's `scratch` folder, and Python cells compile it and run it, as you would in a terminal.
#
# The `%%lua` cells of the earlier labs can't run this lab's code. Their Lua lives inside Python,
# and a C module built here can't find the functions it calls in it: loading one fails with
# `undefined symbol: lua_settop`. So the checks run the standalone `lua` from the notebook
# environment, which exports those functions. As in the earlier labs, each check cell prints
# `passed` or fails with a message.

# %% [markdown]
# ## Setup
#
# This cell finds the compiler and Lua's headers and library, and defines four helpers:
# `build_module` and `build_program` compile a C file from `scratch`, `run` runs a program there,
# and `lua` runs Lua code there with the standalone interpreter. If anything shows `NOT FOUND`,
# install it as setting up describes, then run the cell again.

# %%
import os
import pathlib
import shutil
import subprocess
import sys

SCRATCH = pathlib.Path("scratch").resolve()
SCRATCH.mkdir(exist_ok=True)
LUA_HOME = pathlib.Path(sys.prefix) / "lua"
LUA = LUA_HOME / "bin" / "lua"
INCLUDE = LUA_HOME / "include"
LIBRARY = next(iter(sorted((LUA_HOME / "lib").glob("liblua*.a"))), None)
CC = os.environ.get("CC") or shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
MACOS = sys.platform == "darwin"


def compile_c(*args):
    """Runs the C compiler in scratch; returns its exit status and its messages."""
    result = subprocess.run([CC, "-O2", "-Wall", "-Wextra", f"-I{INCLUDE}", *args], cwd=SCRATCH,
                            capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def build_module(name):
    """Compiles scratch/<name>.c into a module that require("<name>") loads."""
    shared = ["-bundle", "-undefined", "dynamic_lookup"] if MACOS else ["-shared", "-fPIC"]
    return compile_c(*shared, f"{name}.c", "-o", f"{name}.so")


def build_program(name):
    """Compiles scratch/<name>.c into a program, scratch/<name>, with Lua linked in."""
    libraries = ["-lm"] if MACOS else ["-lm", "-ldl"]
    return compile_c(f"{name}.c", "-o", name, str(LIBRARY), *libraries)


def run(*args):
    """Runs a program in scratch; returns its exit status and its output."""
    result = subprocess.run(list(args), cwd=SCRATCH, capture_output=True, text=True, timeout=60)
    return result.returncode, result.stdout + result.stderr


PRELUDE = """\
package.cpath = "./?.so;" .. package.cpath
local function fails(fn, expected)
  local ok, err = pcall(fn)
  assert(not ok, "this call should raise an error containing: " .. expected)
  assert(tostring(err):find(expected, 1, true),
    ("the error should contain %q; it was %q"):format(expected, tostring(err)))
end
"""


def lua(code):
    """Runs PRELUDE and then the code in scratch with the standalone lua; returns status, output."""
    (SCRATCH / "check.lua").write_text(PRELUDE + code)
    return run(str(LUA), "check.lua")


print("Python", sys.version.split()[0])
print("compiler ", subprocess.run([CC, "--version"], capture_output=True, text=True).stdout
      .splitlines()[0] if CC else "NOT FOUND")
print("lua      ", run(str(LUA), "-v")[1].strip() if LUA.exists() else "NOT FOUND")
print("headers  ", INCLUDE if (INCLUDE / "lua.h").exists() else "NOT FOUND")
print("library  ", LIBRARY or "NOT FOUND")

# %% [markdown]
# ## 1. The stack
#
# `stack.c` runs the C API operations you give it on the command line, one per argument, and
# prints the stack after each one, bottom first. It knows `pushinteger N`, `pushstring WORD`,
# `pushnil`, `pushboolean true` or `false`, `pushvalue I`, `remove I`, `insert I`, `replace I`,
# `settop N`, and `pop N`. Run the next two cells to write and compile it.

# %%
# %%writefile scratch/stack.c
/* Runs the stack operations given as arguments, and prints the stack after each one. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lua.h"
#include "lauxlib.h"

static void show(lua_State *L, const char *step) {
  printf("%-18s", step);
  for (int i = 1; i <= lua_gettop(L); i++) {
    switch (lua_type(L, i)) {
      case LUA_TNUMBER: printf(" %lld", (long long)lua_tointeger(L, i)); break;
      case LUA_TSTRING: printf(" '%s'", lua_tostring(L, i)); break;
      case LUA_TBOOLEAN: printf(" %s", lua_toboolean(L, i) ? "true" : "false"); break;
      default: printf(" %s", luaL_typename(L, i)); break;
    }
  }
  printf("\n");
}

int main(int argc, char **argv) {
  lua_State *L = luaL_newstate();
  for (int a = 1; a < argc; a++) {
    char op[32];
    char arg[64] = "";
    if (sscanf(argv[a], "%31s %63s", op, arg) < 1) continue;
    int n = atoi(arg);
    if (strcmp(op, "pushinteger") == 0) lua_pushinteger(L, n);
    else if (strcmp(op, "pushstring") == 0) lua_pushstring(L, arg);
    else if (strcmp(op, "pushnil") == 0) lua_pushnil(L);
    else if (strcmp(op, "pushboolean") == 0) lua_pushboolean(L, strcmp(arg, "true") == 0);
    else if (strcmp(op, "pushvalue") == 0) lua_pushvalue(L, n);
    else if (strcmp(op, "remove") == 0) lua_remove(L, n);
    else if (strcmp(op, "insert") == 0) lua_insert(L, n);
    else if (strcmp(op, "replace") == 0) lua_replace(L, n);
    else if (strcmp(op, "settop") == 0) lua_settop(L, n);
    else if (strcmp(op, "pop") == 0) lua_pop(L, n);
    else { fprintf(stderr, "unknown operation: %s\n", op); return 1; }
    show(L, argv[a]);
  }
  lua_close(L);
  return 0;
}

# %%
status, output = build_program("stack")
assert status == 0, "stack.c didn't compile:\n" + output


def show_stack(ops):
    """Runs the operations with stack.c; returns the stack after each one, as printed."""
    status, output = run("./stack", *ops)
    assert status == 0, output
    return [line[len(op):].strip() for op, line in zip(ops, output.splitlines())]


print(run("./stack", "pushinteger 10", "pushstring hi", "pushnil", "pushvalue -3", "remove 2",
          "insert 1", "settop 2")[1])

# %% [markdown]
# That is the sequence from the reading. Try your own in the next cell: change `MINE` and run it
# again. Keep every index within the stack: the C API doesn't check, so an index past the top is a
# bug whose result is undefined, not an error message.

# %%
MINE = ["pushstring x", "pushinteger 1", "pushinteger 2", "insert 1", "pop 1"]
print("\n".join(show_stack(MINE)))

# %% [markdown]
# ### Exercise L13.1 (LO-13.1, ★, about 20 minutes)
#
# Predict the stack after each step of `OPS`, without running them. Write each as `stack.c` prints
# it, bottom first, separated by spaces: integers as digits, strings in single quotes, and `nil`,
# `true`, and `false` as words. The first two are done. Then run the check, which names the steps
# you got wrong; work out why before you run `show_stack(OPS)` to see them.

# %%
OPS = ["pushinteger 1", "pushinteger 2", "pushstring a", "pushvalue 1", "insert -3", "replace 1",
       "pushboolean true", "remove -2", "settop 4", "pop 2"]

# %% tags=["answer-L13.1"]
PREDICTION = [
    "1",
    "1 2",
    # your predictions for the other eight steps
]

# %% tags=["raises-exception"]
assert len(PREDICTION) == len(OPS), f"predict all {len(OPS)} steps; you have {len(PREDICTION)}"
actual = show_stack(OPS)
wrong = [f"{n} ({op})" for n, (op, guess, real) in enumerate(zip(OPS, PREDICTION, actual), 1)
         if " ".join(guess.split()) != real]
assert not wrong, "these steps are wrong: " + ", ".join(wrong)
print("passed")

# %% [markdown]
# ## 2. A C module
#
# ### Exercise L13.2 (LO-13.2, ★★, about 30 minutes)
#
# Write the two functions of the module `intmath` in the next cell:
#
# - `intmath.gcd(a, b)` returns the greatest common divisor of two integers, which is never
#   negative; `gcd(7, 0)` is 7 and `gcd(0, 0)` is 0.
# - `intmath.divmod(a, b)` returns two integers, `a // b` and `a % b`, equal to what Lua's own
#   operators give. C's `/` rounds toward zero, but Lua's `//` rounds down, so the two differ when
#   `a` and `b` have different signs and `b` doesn't divide `a`: `-7 // 2` is -4 in Lua, and
#   `-7 / 2` is -3 in C. For `b == 0`, raise `bad argument #2 to 'divmod' (division by zero)`.
#
# Check both arguments with `luaL_checkinteger`, so that `gcd(1.5, 2)` raises `number has no
# integer representation`. The check leaves out `math.mininteger`, whose absolute value doesn't fit
# in an integer, and for which C's `a / b` overflows when `b` is -1.
#
# <details>
# <summary>Hint</summary>
#
# For `gcd`, Euclid's algorithm: replace `(x, y)` with `(y, x % y)` until `y` is 0, starting from
# the absolute values. For `divmod`, compute `q = a / b` and `r = a % b` in C; when `r` isn't 0 and
# has a different sign from `b`, subtract 1 from `q` and add `b` to `r`.
# </details>

# %% tags=["answer-L13.2"]
# %%writefile scratch/intmath.c
/* intmath: integer functions written in C. */
#include "lua.h"
#include "lauxlib.h"

/* gcd(a, b): the greatest common divisor of two integers, never negative. */
static int l_gcd(lua_State *L) {
  /* your code here */
  return luaL_error(L, "gcd isn't written yet");
}

/* divmod(a, b): a // b and a % b, rounded the way Lua rounds them. */
static int l_divmod(lua_State *L) {
  /* your code here */
  return luaL_error(L, "divmod isn't written yet");
}

static const luaL_Reg functions[] = {
  { "gcd", l_gcd },
  { "divmod", l_divmod },
  { NULL, NULL },
};

int luaopen_intmath(lua_State *L) {
  luaL_newlib(L, functions);
  return 1;
}

# %% tags=["raises-exception"]
status, warnings = build_module("intmath")
assert status == 0, "intmath.c didn't compile:\n" + warnings
status, output = lua("""
local intmath = require("intmath")
for _, case in ipairs({ { 12, 18, 6 }, { -12, 18, 6 }, { 12, -18, 6 }, { 7, 0, 7 }, { 0, 7, 7 },
                        { 0, 0, 0 }, { 17, 5, 1 }, { math.maxinteger, 1, 1 } }) do
  local a, b, want = table.unpack(case)
  local got = intmath.gcd(a, b)
  assert(got == want and math.type(got) == "integer",
    ("gcd(%d, %d) should be the integer %d; got %s"):format(a, b, want, tostring(got)))
end
for _, a in ipairs({ 7, -7, 6, -6, 0, 1, -1, math.maxinteger }) do
  for _, b in ipairs({ 2, -2, 3, -3, 7, 1, -1, math.maxinteger }) do
    local q, r = intmath.divmod(a, b)
    assert(q == a // b and r == a % b and math.type(q) == "integer" and math.type(r) == "integer",
      ("divmod(%d, %d) gave %s, %s; Lua gives %d, %d"):format(a, b, tostring(q), tostring(r),
        a // b, a % b))
  end
end
fails(function() return intmath.divmod(7, 0) end, "bad argument #2 to 'divmod' (division by zero)")
fails(function() return intmath.gcd(1.5, 2) end, "bad argument #1 to 'gcd' (number has no integer")
fails(function() return intmath.divmod(7, "x") end, "bad argument #2 to 'divmod' (number expected")
print("passed")
""")
print(output)
assert status == 0, "a check failed"
assert "warning" not in warnings, "fix the compiler's warnings:\n" + warnings

# %% [markdown]
# ## 3. A program that runs Lua
#
# `scorer` is a C program that scores words with a Lua script: `./scorer rules.lua lua bad half`
# loads `rules.lua`, calls its function `score` for each word, and prints each score and the total.
# A script is code the program doesn't control, so `scorer` must report each failure and go on.
# Run the next cell, which writes the script the check uses.

# %%
# %%writefile scratch/rules.lua
function score(word)
  if word == "bad" then
    error("no score for bad")
  end
  if word == "half" then
    return 0.5
  end
  return #word
end

# %% [markdown]
# ### Exercise L13.3 (LO-13.3, ★★, about 30 minutes)
#
# Write `call_score` in the next cell. It calls the script's global `score` with the word, in
# protected mode. If the call raises an error, it prints `<word>: error: <message>`, with the
# error's message. If the result isn't an integer, it prints `<word>: error: score must return an
# integer`. Otherwise it stores the result in `*result` and returns 1. Whatever happens, it leaves
# the stack as it found it: `main` prints the stack's size at the end, which must be 0. The check
# expects this output for the words `lua bad half tables`:
#
# ```text
# lua: 3
# bad: error: rules.lua:3: no score for bad
# half: error: score must return an integer
# tables: 6
# total: 9
# stack: 0
# ```

# %% tags=["answer-L13.3"]
# %%writefile scratch/scorer.c
/* scorer: scores each word given on the command line with the function score in a Lua script. */
#include <stdio.h>
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"

/* Calls the script's score(word). On success, stores the result in *result and returns 1. On
   failure, prints "<word>: error: <message>" and returns 0. Either way, it leaves the stack as it
   found it. */
static int call_score(lua_State *L, const char *word, lua_Integer *result) {
  /* your code here */
  (void)L; (void)word; (void)result;
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "usage: scorer SCRIPT WORD...\n");
    return 2;
  }
  lua_State *L = luaL_newstate();
  luaL_openlibs(L);
  if (luaL_dofile(L, argv[1]) != LUA_OK) {
    fprintf(stderr, "scorer: %s\n", lua_tostring(L, -1));
    lua_close(L);
    return 1;
  }
  lua_Integer total = 0;
  for (int i = 2; i < argc; i++) {
    lua_Integer score;
    if (call_score(L, argv[i], &score)) {
      printf("%s: %lld\n", argv[i], (long long)score);
      total += score;
    }
  }
  printf("total: %lld\nstack: %d\n", (long long)total, lua_gettop(L));
  lua_close(L);
  return 0;
}

# %% tags=["raises-exception"]
status, warnings = build_program("scorer")
assert status == 0, "scorer.c didn't compile:\n" + warnings
expected = """\
lua: 3
bad: error: rules.lua:3: no score for bad
half: error: score must return an integer
tables: 6
total: 9
stack: 0
"""
status, output = run("./scorer", "rules.lua", "lua", "bad", "half", "tables")
assert output == expected, f"expected:\n{expected}\ngot:\n{output}"
words = ["bad", "half", "ok"] * 50
status, output = run("./scorer", "rules.lua", *words)
assert output.endswith("total: 100\nstack: 0\n"), \
    "with 150 words, the stack must still end empty:\n" + output[-200:]
(SCRATCH / "empty.lua").write_text("local nothing = true\n")
status, output = run("./scorer", "empty.lua", "lua")
assert output.startswith("lua: error: attempt to call a nil value"), \
    "a script without score should give an error for each word:\n" + output
assert "warning" not in warnings, "fix the compiler's warnings:\n" + warnings
print("passed")

# %% [markdown]
# Now break the script on purpose. Change `rules.lua` so that it doesn't parse, run its cell, and
# run the next cell: `scorer` should print the syntax error and exit with status 1. Then restore the
# script.

# %%
print(run("./scorer", "rules.lua", "lua", "tables"))

# %% [markdown]
# ## 4. Full userdata
#
# ### Exercise L13.4 (LO-13.4, ★★★, about 40 minutes)
#
# The module `bitset` holds a set of bits numbered from 1 to its size, in memory that C allocates.
# The next cell has everything but four functions. Write them:
#
# - `bitset_new`: `bitset.new(size)` checks that `size` is an integer from 1 to `INT_MAX`, or
#   raises `bad argument #1 to 'new' (size out of range)`. It creates the userdata with
#   `lua_newuserdatauv`, gives it the metatable registered as `"bitset"`, allocates
#   `(size + WORD_BITS - 1) / WORD_BITS` words of zeros with `calloc`, raises `not enough memory`
#   if that fails, adds 1 to `live`, and returns the bitset.
# - `bitset_set`: `b:set(i)` sets bit `i` and returns `b`, so calls can be chained.
# - `bitset_test`: `b:test(i)` returns `true` if bit `i` is set, and `false` otherwise.
# - `bitset_gc`: `__gc` frees the words, sets the pointer to `NULL`, and subtracts 1 from `live`,
#   but only if the words haven't been freed already: a program can call `__gc` itself, and the
#   collector calls it again later.
#
# Use `check_bitset` and `check_index`, which raise errors such as `bad argument #1 to 'set' (index
# out of range)`. Bit `i`, counting from 0, is in word `i / WORD_BITS`, at position
# `i % WORD_BITS`; `bitset_count` shows how to read it, and `words[w] |= 1UL << p` sets it.
#
# <details>
# <summary>Hint</summary>
#
# Set `b->words = NULL` and call `luaL_setmetatable` before `calloc`. If `calloc` fails, the
# error leaves a userdata whose `__gc` will still run, and it must find `NULL` there, not an
# uninitialized pointer.
# </details>

# %% tags=["answer-L13.4"]
# %%writefile scratch/bitset.c
/* bitset: a fixed-size set of bits, held in memory that C allocates. */
#include <limits.h>
#include <stdlib.h>
#include "lua.h"
#include "lauxlib.h"

#define WORD_BITS (sizeof(unsigned long) * CHAR_BIT)

typedef struct {
  unsigned long *words; /* the bits, WORD_BITS to a word; NULL once freed */
  lua_Integer size;     /* the number of bits */
} Bitset;

static int live = 0; /* bitsets created and not yet freed */

static Bitset *check_bitset(lua_State *L) {
  return (Bitset *)luaL_checkudata(L, 1, "bitset");
}

/* The bit index at argument 2, checked to be from 1 to the bitset's size, counted from 0. */
static lua_Integer check_index(lua_State *L, Bitset *b) {
  lua_Integer i = luaL_checkinteger(L, 2);
  luaL_argcheck(L, 1 <= i && i <= b->size, 2, "index out of range");
  return i - 1;
}

/* bitset.new(size): a bitset of size bits, all clear. */
static int bitset_new(lua_State *L) {
  /* your code here */
  return luaL_error(L, "new isn't written yet");
}

/* b:set(i): sets bit i; returns b. */
static int bitset_set(lua_State *L) {
  /* your code here */
  return luaL_error(L, "set isn't written yet");
}

/* b:test(i): true if bit i is set. */
static int bitset_test(lua_State *L) {
  /* your code here */
  return luaL_error(L, "test isn't written yet");
}

/* b:count(): the number of bits set. */
static int bitset_count(lua_State *L) {
  Bitset *b = check_bitset(L);
  lua_Integer n = 0;
  for (lua_Integer i = 0; i < b->size; i++) n += (b->words[i / WORD_BITS] >> (i % WORD_BITS)) & 1UL;
  lua_pushinteger(L, n);
  return 1;
}

/* #b: the number of bits. */
static int bitset_len(lua_State *L) {
  lua_pushinteger(L, check_bitset(L)->size);
  return 1;
}

/* tostring(b): "bitset(<size>): <count> set". */
static int bitset_tostring(lua_State *L) {
  Bitset *b = check_bitset(L);
  bitset_count(L);
  lua_pushfstring(L, "bitset(%I): %I set", (LUAI_UACINT)b->size, (LUAI_UACINT)lua_tointeger(L, -1));
  return 1;
}

/* Frees the bits, once: the collector, or a program, may call __gc again. */
static int bitset_gc(lua_State *L) {
  /* your code here */
  (void)L;
  return 0;
}

/* bitset.live(): the number of bitsets not yet freed. */
static int bitset_live(lua_State *L) {
  lua_pushinteger(L, live);
  return 1;
}

static const luaL_Reg methods[] = {
  { "set", bitset_set },
  { "test", bitset_test },
  { "count", bitset_count },
  { "__len", bitset_len },
  { "__tostring", bitset_tostring },
  { "__gc", bitset_gc },
  { NULL, NULL },
};

static const luaL_Reg functions[] = {
  { "new", bitset_new },
  { "live", bitset_live },
  { NULL, NULL },
};

int luaopen_bitset(lua_State *L) {
  luaL_newmetatable(L, "bitset");
  luaL_setfuncs(L, methods, 0);
  lua_pushvalue(L, -1);
  lua_setfield(L, -2, "__index");
  luaL_newlib(L, functions);
  return 1;
}

# %% [markdown]
# The first check tests the methods and their errors.

# %% tags=["raises-exception"]
status, warnings = build_module("bitset")
assert status == 0, "bitset.c didn't compile:\n" + warnings
status, output = lua("""
local bitset = require("bitset")
local b = bitset.new(100)
assert(#b == 100 and b:count() == 0, "a new bitset of 100 bits has none set")
assert(b:set(1) == b, "set should return the bitset")
b:set(64):set(65):set(100):set(64)
for _, i in ipairs({ 1, 64, 65, 100 }) do
  assert(b:test(i) == true, "bit " .. i .. " should be set")
end
for _, i in ipairs({ 2, 63, 66, 99 }) do
  assert(b:test(i) == false, "bit " .. i .. " should be clear")
end
assert(tostring(b) == "bitset(100): 4 set", "got " .. tostring(b))
assert(getmetatable(b).__name == "bitset", "give the userdata the metatable registered as bitset")
fails(function() b:set(101) end, "bad argument #1 to 'set' (index out of range)")
fails(function() b:test(0) end, "bad argument #1 to 'test' (index out of range)")
fails(function() b.set({}, 1) end, "bad argument #1 to 'set' (bitset expected, got table)")
fails(function() bitset.new(0) end, "bad argument #1 to 'new' (size out of range)")
fails(function() bitset.new(2.5) end, "number has no integer representation")
print("passed")
""")
print(output)
assert status == 0, "a check failed"
assert "warning" not in warnings, "fix the compiler's warnings:\n" + warnings

# %% [markdown]
# The second check tests the bitsets' lifetime. Before you run it, predict what `bitset.live()`
# returns after the loop, and again after `collectgarbage`. The check runs in a new `lua` process,
# so `live` starts at 0. A crash here, with a status such as -6 and a message about `free`, means
# that `__gc` freed the same memory twice.

# %% tags=["raises-exception"]
status, output = lua("""
local bitset = require("bitset")
local keep = bitset.new(10)
for _ = 1, 100 do bitset.new(1000) end
print("live after the loop:", bitset.live())
collectgarbage("collect")
print("live after collecting:", bitset.live())
assert(bitset.live() == 1, "only keep is still in use, so live should be 1")
local mt = getmetatable(keep)
mt.__gc(keep)
mt.__gc(keep)
assert(bitset.live() == 0, "__gc called twice should free keep once; live should be 0")
keep = nil
collectgarbage("collect")
assert(bitset.live() == 0, "the collector's own call to __gc must not count keep again")
print("passed")
""")
print(output)
assert status == 0, f"a check failed, with status {status}"

# %% [markdown]
# After the loop, `live` is probably less than 101: the collector ran while the loop allocated, and
# freed some of the bitsets nothing referred to; in the course's setup it printed 86 in one run and
# 72 in another, depending on the code around the loop. After
# `collectgarbage("collect")`, a full collection, only `keep` is left. The collector paces itself by
# the memory Lua allocated, though, and counts only each bitset's 16-byte structure, not the 128
# bytes of words that `calloc` gave it; the reading shows what that does to a program with a large
# heap.
#
# ## Summary
#
# - The stack's indices name positions from the bottom (1, 2, …) or the top (-1, -2, …), and every
#   operation moves values among them; predicting a sequence by hand is how you debug C code that
#   misplaces one.
# - A C module checks each argument, pushes its results, and returns their number, and its error
#   messages name the argument, as Lua's own functions do.
# - A host calls scripts with `lua_pcall`, reports what fails, and pops every result and message,
#   so the stack ends where it started however many calls fail.
# - Full userdata gives a C structure a metatable, methods, and a type check, and `__gc` frees its C
#   memory once, however many times it runs.
#
# Next, do the [Module 13 practice](practice.md), and hand in the final project's milestone.

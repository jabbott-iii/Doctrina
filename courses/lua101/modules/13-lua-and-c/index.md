# Module 13: Lua and C

**Objectives:** LO-13.1, LO-13.2, LO-13.3, LO-13.4\
**Prerequisites:** [Module 6](../06-errors-modules-and-tests/index.md) and
[Module 7](../07-metatables/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 13](lab13.ipynb), 1.5 for the
[practice](practice.md), and 3 toward the milestone of the
[capstone project](../../assignments/final-project/README.md), which follows this module

Lua was built to live inside programs written in C, and it talks to them through a small
interface, the **C API**. The API works in two directions. **Extending** Lua means writing
functions in C that Lua code calls, for speed or to reach a C library. **Embedding** Lua means a C
program that runs Lua code, which is how Neovim, Redis, games, and most other hosts use it. This
module covers both, and full userdata, which lets Lua hold a C structure as a value of its own. It
explains the C it uses as it goes; you should be able to read short functions in any C-like
language.

## Enough C to follow along

C is compiled, with static types and manual memory. Five features appear below:

- **Types:** `int` and `long long` are integers, `double` is a float, `size_t` is a size in bytes,
  and `char *` points at text. Lua's own `lua_Integer` and `lua_Number` are its integer and float.
- **Pointers:** `Buffer *b` holds the address of a `Buffer`, and `b->length` reads a field through
  it. `NULL` is the pointer to nothing.
- **Structs:** `typedef struct { char *data; size_t length; } Buffer;` declares a record type.
- **Memory:** `malloc` and `realloc` allocate memory, and `free` releases it; nothing does it for
  you.
- **Headers:** `#include "lua.h"` brings in the API's declarations, `lauxlib.h` the auxiliary
  library (`luaL_…` functions), and `lualib.h` the standard libraries.

Compile with `gcc`, giving it the folder of the headers with `-I`; on macOS, the `gcc` command runs
Apple's Clang, which accepts the options used here. The course's headers are in
`.venv/lua/include`, and the Lua library is `.venv/lua/lib/liblua54.a`.

## The stack

C and Lua can't share values directly: C has no type for "any Lua value", and Lua's garbage
collector must know about every value still in use. So every exchange goes through a **virtual
stack** of Lua values that belongs to the `lua_State`, the C handle of a Lua interpreter. C pushes
values onto the stack, Lua takes them from there, and results come back the same way. While a value
is on the stack, the collector knows it is in use.

Positions on the stack are **indices**. Index 1 is the bottom, and negative indices count from the
top: -1 is the top value, -2 the one under it. The functions come in families:

| Family | Examples | What they do |
| :- | :- | :- |
| Push | `lua_pushinteger`, `lua_pushnumber`, `lua_pushstring`, `lua_pushnil`, `lua_pushvalue(L, i)` | Put a value on top; `pushvalue` copies the value at index `i` |
| Read | `lua_tointeger`, `lua_tonumber`, `lua_tostring`, `lua_type`, `lua_isinteger` | Read the value at an index, without removing it |
| Check | `luaL_checkinteger`, `luaL_checknumber`, `luaL_checkstring` | Read an argument, or raise `bad argument #n to 'name'` |
| Arrange | `lua_gettop`, `lua_settop(L, n)`, `lua_pop(L, n)`, `lua_remove`, `lua_insert` | Count, cut, pop, remove, and move values |

Here is a sequence of calls, with the stack, bottom first, after each one:

```text
pushinteger 10             10
pushstring 'hi'            10 'hi'
pushnil                    10 'hi' nil
pushvalue -3               10 'hi' nil 10
remove 2                   10 nil 10
insert 1                   10 10 nil
settop 2                   10 10
```

`pushvalue -3` copied the value three from the top, 10. `remove 2` removed the value at index 2 and
moved the ones above it down. `insert 1` moved the top value to index 1, shifting the others up.
`settop 2` cut the stack to two values. Lab 13 has you trace sequences like this one and check your
answers against a C program that prints the stack.

The API doesn't check indices or room by default. An index past the top is a bug whose result is
undefined, not an error. When Lua calls a C function, it guarantees room for 20 more values
(`LUA_MINSTACK`); a function that may push more, such as one that pushes every item of a list, first
calls `lua_checkstack(L, n)`, which grows the stack or returns 0 if it can't.

The stack is a deliberate design, and it bridges two differences between the languages. Lua's
values carry their types while the program runs, but C's types are fixed when it compiles; and Lua
frees memory with a garbage collector, while C frees it by hand. Because C refers to Lua values by
their stack index instead of holding them itself, the collector always knows which values C is
using. The designers' article on the API, in "Further reading", discusses the design.

## C functions that Lua can call

A C function that Lua can call has one signature: it takes the `lua_State`, finds its arguments on
the stack at indices 1 to `lua_gettop(L)`, pushes its results, and returns how many it pushed:

```c
/* clamp(x, lo, hi): x limited to the range from lo to hi. */
static int l_clamp(lua_State *L) {
  lua_Number x = luaL_checknumber(L, 1);
  lua_Number lo = luaL_checknumber(L, 2);
  lua_Number hi = luaL_checknumber(L, 3);
  luaL_argcheck(L, lo <= hi, 2, "lo must not be greater than hi");
  lua_pushnumber(L, x < lo ? lo : (x > hi ? hi : x));
  return 1;   /* one result */
}
```

The `luaL_check…` functions read an argument, or raise an error that names it: in a script,
`mathx.clamp("x", 0, 1)` fails with `bad argument #1 to 'clamp' (number expected, got string)`,
after the script's name and line. (Called through `pcall(mathx.clamp, "x", 0, 1)`, with no line of
Lua making the call, the message names the function `'mathx.clamp'` instead.) `luaL_argcheck`
raises the same kind of error for a condition of your own. A C function that returns two results
pushes two values and returns 2, as `l_sum` does, and as `divmod` in Lab 13 will. It takes any
number of arguments, so `lua_gettop(L)` tells it how many it got:

```c
/* sum(...): the sum of any number of numbers, and how many there were. */
static int l_sum(lua_State *L) {
  int n = lua_gettop(L);
  lua_Number total = 0;
  for (int i = 1; i <= n; i++) total += luaL_checknumber(L, i);
  lua_pushnumber(L, total);
  lua_pushinteger(L, n);
  return 2;   /* mathx.sum(1, 2, 3.5) returns 6.5 and 3 */
}
```

### A C module

A C module is a shared library with one exported function, `luaopen_` followed by the module's
name, which `require` calls. It builds the module's table, usually from a list of names and
functions:

```c
static const luaL_Reg functions[] = {
  { "clamp", l_clamp },
  { "sum", l_sum },
  { NULL, NULL },          /* marks the end of the list */
};

int luaopen_mathx(lua_State *L) {
  luaL_newlib(L, functions);   /* a new table holding the functions */
  return 1;                    /* the table is the module */
}
```

On Linux, compile it into `mathx.so`; on macOS, replace `-shared` with
`-bundle -undefined dynamic_lookup`:

```bash
gcc -O2 -Wall -shared -fPIC -I.venv/lua/include mathx.c -o mathx.so
```

`require("mathx")` searches `package.cpath`, as it searches `package.path` for Lua files, finds
`./mathx.so`, and calls `luaopen_mathx`. A rockspec builds C modules the same way: a `builtin`
build with `modules = { mathx = "csrc/mathx.c" }` compiles the file with the right flags for the
system.

## Embedding Lua in a C program

A C program that runs Lua creates a state, loads the libraries, runs a script, and calls the
script's functions:

```c
lua_State *L = luaL_newstate();          /* a new, empty interpreter */
luaL_openlibs(L);                        /* the standard libraries */
if (luaL_dofile(L, "script.lua") != LUA_OK) {
  fprintf(stderr, "host: %s\n", lua_tostring(L, -1));   /* the error message is on top */
}
lua_getglobal(L, "transform");           /* push the function */
lua_pushinteger(L, 2);                   /* push its argument */
if (lua_pcall(L, 1, 1, 0) != LUA_OK) {   /* call with 1 argument, expecting 1 result */
  fprintf(stderr, "host: %s\n", lua_tostring(L, -1));
} else {
  printf("%lld\n", (long long)lua_tointeger(L, -1));
}
lua_pop(L, 1);                           /* the result, or the message */
lua_close(L);                            /* free everything */
```

Link the program with Lua's library, and the math and dynamic-loading libraries it uses:

```bash
gcc -O2 -Wall -I.venv/lua/include host.c -o host .venv/lua/lib/liblua54.a -lm -ldl
```

Three rules keep an embedding program correct:

- **Call Lua with `lua_pcall`, never `lua_call`, from the host.** `lua_pcall` catches an error,
  leaves the message on the stack, and returns a status. An error outside any protected call goes
  to Lua's **panic function**, which by default prints the message and aborts the whole program.
- **Keep the stack balanced.** Pop each result and each error message once you have used them. A
  loop that forgets one leaves a value per pass, and nothing complains until the stack reaches its
  limit, `LUAI_MAXSTACK`, a million values in a standard build. In a test, a host that called a
  function and never popped its result ran 999,996 passes before `lua_pcall` failed with
  `stack overflow`. Checking that `lua_gettop(L)` is back to its starting value at the end of each
  pass catches the mistake on the first pass.
- **Check the type of what comes back.** A script can return anything; `lua_isinteger` or
  `luaL_checkinteger` in a protected call make the host's assumptions explicit.

## Full userdata

A C structure becomes a Lua value through **full userdata**: a block of memory that Lua allocates,
that C fills in, and that the garbage collector frees when Lua no longer refers to it. Like a
table, it can have a metatable, which gives it methods and metamethods. Here is part of a growable
text buffer; Lab 13 builds a similar type, a set of bits:

```c
typedef struct { char *data; size_t length, capacity; } Buffer;

static int buffer_new(lua_State *L) {
  Buffer *b = (Buffer *)lua_newuserdatauv(L, sizeof(Buffer), 0);  /* the memory, on the stack */
  b->data = NULL;
  b->length = b->capacity = 0;
  luaL_setmetatable(L, "Buffer");       /* the metatable registered under the name "Buffer" */
  return 1;
}

static int buffer_gc(lua_State *L) {
  Buffer *b = (Buffer *)luaL_checkudata(L, 1, "Buffer");
  free(b->data);                        /* free what C allocated */
  b->data = NULL;                       /* so that a second call can't free it twice */
  return 0;
}

int luaopen_buffer(lua_State *L) {
  luaL_newmetatable(L, "Buffer");       /* create the metatable, and register its name */
  luaL_setfuncs(L, methods, 0);         /* append, __tostring, __len, __gc */
  lua_pushvalue(L, -1);
  lua_setfield(L, -2, "__index");       /* methods are found in the metatable itself */
  luaL_newlib(L, functions);            /* new */
  return 1;
}
```

`luaL_checkudata(L, 1, "Buffer")` is the userdata's type check: a call on another value, such as
`b.append({}, "x")`, raises `bad argument #1 to 'append' (Buffer expected, got table)`. `__gc`
frees the C memory, because Lua frees only the userdata's own block, not the memory C allocated for
it. Lua calls `__gc` at some collection after the last reference is gone, or when the state closes,
so it must be safe on any buffer, used or not. A **light userdata**, by contrast, is a bare C
pointer with no memory, metatable, or collection of its own; use it as a key, not as an object.

The collector also doesn't see the memory C allocated. It decides when to run from the memory Lua
itself allocated, so a userdata of 16 bytes that holds 125 KB counts as 16 bytes. In a test with
Lab 13's bit sets, on Linux with Lua 5.4.8, a program with 169 MB of Lua tables created 20,000 bit
sets of 125 KB each and kept none of them, yet all 20,000 were still alive at the end: about 2.5 GB
of C memory that no collection had come for. A type that holds a large or scarce resource needs a
way to release it explicitly, with `__gc` as the safety net.

## Common misconceptions

| Belief | What the API does | Example that breaks it |
| :- | :- | :- |
| A C function returns its result with `return` | It pushes results and returns how many | `return 1` after pushing one value |
| Negative and positive indices are different values | Both name positions in the same stack | With three values, -1 and 3 are the same |
| `lua_tostring` removes the value | Reading leaves the stack unchanged | Pop what you no longer need |
| `lua_call` is fine in a host | An unprotected error aborts the program | Use `lua_pcall` and check its status |
| Lua frees everything a userdata holds | It frees only the userdata's own block | `__gc` must `free` what C allocated |
| `__gc` runs as soon as the last reference goes | At some later collection, or at `lua_close` | Close resources explicitly too, with a method or `<close>` |
| The collector sees the memory a userdata holds | It counts only the userdata's own block | 20,000 dropped bit sets of 125 KB each, all still alive |
| A C module must be linked with Lua's library | It calls the functions of the program that loads it, which the standalone `lua` exports | Linking `liblua54.a` into `mathx.so` failed here with `recompile with -fPIC` |

## Summary

- Every value passes between C and Lua through the state's stack: index 1 is the bottom, -1 the
  top, and `push`, `to`, `check`, and `settop` functions move and read values.
- A C function for Lua reads its arguments from the stack, checks them with `luaL_check…`, pushes
  its results, and returns their number; `luaopen_name` builds the module that `require` loads.
- A host creates a state, runs scripts, and calls them with `lua_pcall`, popping every result and
  error message, so the stack stays balanced and errors never abort it.
- Full userdata holds a C structure that the collector manages; its metatable gives it methods, a
  type check through `luaL_checkudata`, and a `__gc` that frees the C side.

## Self-check

1. The stack holds `1 2 3` (bottom first). What does it hold after `lua_pushvalue(L, 1)`, then
   `lua_remove(L, -2)`, then `lua_insert(L, 2)`?

   <details>
   <summary>Answer</summary>

   `1 2 3 1`, then `1 2 1` (the value at -2, 3, is removed), then `1 1 2` (the top, 1, moves to
   index 2).
   </details>

2. A C function pushes a string and a number, then returns 1. What does the Lua caller receive?

   <details>
   <summary>Answer</summary>

   Only the number: Lua takes the top `n` values as the results, so with `return 1` it takes the
   number, the last value pushed, and discards the string.
   </details>

3. Why does a host call scripts with `lua_pcall` and not `lua_call`?

   <details>
   <summary>Answer</summary>

   An error in a script called with `lua_call`, outside any protected call, goes to the panic
   function, which aborts the host. `lua_pcall` catches it and returns a status with the message on
   the stack, so the host can report it and go on.
   </details>

4. A host calls a script's function in a loop, and after about a million passes `lua_pcall` starts
   failing with `stack overflow`. What is the likely bug?

   <details>
   <summary>Answer</summary>

   It leaves a value on the stack each pass, typically a result or an error message it never pops.
   Each pass should end with `lua_gettop(L)` where it started.
   </details>

5. A userdata wraps a file handle from a C library. Why isn't `__gc` enough to close the file?

   <details>
   <summary>Answer</summary>

   The collector runs `__gc` at some later collection, which may be long after the program stopped
   using the file, or only at `lua_close`. Give the type a `close` method, and `__close` for
   `<close>` variables, and make `__gc` a safety net that closes only what is still open.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*,
  [section 4, The Application Program Interface](https://www.lua.org/manual/5.4/manual.html#4),
  and [section 5, The Auxiliary Library](https://www.lua.org/manual/5.4/manual.html#5). Every API
  function's entry shows what it pops and pushes, in brackets such as `[-0, +1, e]`.
- Roberto Ierusalimschy, Luiz Henrique de Figueiredo, and Waldemar Celes,
  ["Passing a Language through the Eye of a Needle"](https://dl.acm.org/doi/10.1145/1965724.1965739),
  *Communications of the ACM* 54(7), 2011, on why the API is built around a stack.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on the C
  API cover extending and embedding, userdata, and managing resources, with longer examples.

# Module 13 practice

These exercises practice the [Module 13 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then check it by compiling the code with the commands in
the reading and running it with the standalone `lua`, as [Lab 13](lab13.ipynb) does.

## Worked example: a function that swaps its arguments

Write a C function `swap(a, b)` that returns `b, a`.

1. **Say what is on the stack when the function starts.** The arguments, in order: `a b`. But a
   caller may pass more or fewer than two.
2. **Make the stack exactly what you expect.** `lua_settop(L, 2)` drops extra arguments, and fills
   missing ones with `nil`. The stack is now `a b`, always.
3. **Rearrange it.** `lua_insert(L, 1)` moves the top value, `b`, to the bottom: `b a`.
4. **Return the number of results** on top of the stack: 2.

```c
static int l_swap(lua_State *L) {
  lua_settop(L, 2);   /* a b */
  lua_insert(L, 1);   /* b a */
  return 2;
}
```

Built into a module, `swap(1, 2)` returned `2 1`, `swap(1)` returned `nil 1`, and `swap(1, 2, 3)`
returned `2 1`. The function pushed nothing: it rearranged its arguments and returned the top two.

### Exercise 13.1 (LO-13.1, LO-13.3, ★, about 10 minutes)

A host runs this, where `f` is `function f(n) return n * 10, n * 20, n * 30 end`:

```c
lua_getglobal(L, "f");
lua_pushinteger(L, 1);
lua_pcall(L, 1, 2, 0);
```

What is on the stack afterward? And what if `f` returned only `n`?

<details>
<summary>Answer</summary>

`10 20`. `lua_pcall` pops the function and its argument, and leaves exactly the number of results
its third argument asks for: extra results are dropped, so the 30 is gone. If `f` returned only
`n`, the stack would hold `1 nil`: missing results are filled with `nil`. Pass `LUA_MULTRET` to keep
every result, and count them with `lua_gettop`.
</details>

### Exercise 13.2 (LO-13.2, ★★, about 15 minutes)

This function returns the mean of its arguments. Find two inputs it handles wrongly, say what it
returns for each, and fix it.

```c
static int l_mean(lua_State *L) {
  int n = lua_gettop(L);
  lua_Number total = 0;
  for (int i = 1; i <= n; i++) total += lua_tonumber(L, i);
  lua_pushnumber(L, total / n);
  return 1;
}
```

<details>
<summary>Hint</summary>

What does `lua_tonumber` return for a value that isn't a number? What is `total / n` when no one
passes any argument?
</details>

<details>
<summary>Answer</summary>

`mean(1, "x")` returns 0.5: `lua_tonumber` returns 0 for a value it can't convert, so the string
counts as 0 and no error is raised. `mean()` returns `-nan`, from `0.0 / 0`. Check every argument,
and require at least one:

```c
static int l_mean(lua_State *L) {
  int n = lua_gettop(L);
  luaL_argcheck(L, n > 0, 1, "number expected, got no value");
  lua_Number total = 0;
  for (int i = 1; i <= n; i++) total += luaL_checknumber(L, i);
  lua_pushnumber(L, total / n);
  return 1;
}
```

Now `mean(1, "x")` raises `bad argument #2 to 'mean' (number expected, got string)`. `lua_to…`
functions are for values you have already checked, or for when any value is acceptable.
</details>

### Exercise 13.3 (LO-13.3, ★★, about 15 minutes)

A host loads a plugin like this. What happens when `plugin.lua` has a syntax error, and why?
Rewrite the two lines.

```c
luaL_loadfile(L, "plugin.lua");
lua_call(L, 0, 0);
```

<details>
<summary>Answer</summary>

The host ignores `luaL_loadfile`'s status. When the file doesn't compile, `luaL_loadfile` pushes
the error message instead of a function, so `lua_call` tries to call a string. That error is
outside any protected call, so it reaches the panic function. In a test, the program printed
`PANIC: unprotected error in call to Lua API (attempt to call a string value)` and aborted, with
exit status 134. Check the load, and call in protected mode:

```c
if (luaL_loadfile(L, "plugin.lua") != LUA_OK || lua_pcall(L, 0, 0, 0) != LUA_OK) {
  fprintf(stderr, "plugin: %s\n", lua_tostring(L, -1));
  lua_pop(L, 1);
}
```

Both failures leave one message on the stack, so one branch reports either.
</details>

### Exercise 13.4 (LO-13.4, ★★, about 15 minutes)

A `File` userdata holds a `FILE *fp` from C's `fopen`. Its `close` method calls `fclose(f->fp)`,
and so does its `__gc`. What goes wrong when a program calls `f:close()`, and what should each
function do instead?

<details>
<summary>Answer</summary>

The collector later runs `__gc`, which closes the same `FILE *` a second time. That is undefined
behavior in C, and often a crash. `close` should call `fclose` and set `f->fp = NULL`; `__gc`
should close only if `fp` isn't `NULL`; and every other method should check for `NULL` and raise
an error, as Lua's own files do: after `f:close()`, `f:read()` raises `attempt to use a closed
file`. Add `__close` too, doing what `close` does, so `local f <close> = …` closes the file at the
end of its scope instead of whenever the collector comes.
</details>

### Exercise 13.5 (LO-13.1, LO-13.2, ★★★, about 15 minutes)

`table.unpack(t)` is a C function that pushes every item of `t` onto the stack. Why must it call
`lua_checkstack` first, when `swap` didn't? What do you predict `table.unpack` does with a list of
10 million items?

<details>
<summary>Answer</summary>

Lua guarantees a C function room for 20 values (`LUA_MINSTACK`), which `swap` never exceeds: it
pushes nothing. `table.unpack` pushes as many values as the list has items, so it must ask for the
room first; pushing past the space Lua guaranteed is undefined behavior, not an error. With 10
million items, the request fails, because the stack's limit is a million values, so `table.unpack`
raises an error instead: `pcall(table.unpack, t)` returned `false` and `too many results to
unpack`.
</details>

### Exercise 13.6 (LO-13.2, LO-12.3, ★★, about 15 minutes)

For each task, would you write it in C or in Lua? Give the reason.

1. Reading a settings file once, when the program starts.
2. Calling a C library's function that decodes PNG images.
3. Summing a list of 10 million numbers that is already in a Lua table, which takes 76 ms in Lua.

<details>
<summary>Answer</summary>

1. Lua: it runs once, and Lua code is shorter, safer, and easier to test.
2. C: only C can call the library. Keep the C layer thin, and do the rest in Lua.
3. Measure before you decide (Module 12). A C function still fetches each number through the API,
   with `lua_geti` and `lua_tonumber`, one call each. On an Intel Core i7-11800H under Linux, with
   Lua 5.4.8 and other work on the machine, a C version took 116–134 ms against the Lua loop's
   76–89 ms, over three runs of five; C was slower. C pays off when the work in C is large compared
   with the cost of crossing the API, such as decoding a whole image in one call.
</details>

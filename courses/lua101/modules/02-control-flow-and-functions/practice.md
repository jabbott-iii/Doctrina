# Module 2 practice

These exercises practice the [Module 2 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: tracing adjustment

With `min_max` from the reading, which returns the smaller and then the larger of two numbers,
what does `print(min_max(7, 3), min_max(1, 2))` print?

1. The arguments of `print` are a list of two expressions, both calls.
2. `min_max(7, 3)` is not the last item, so it is adjusted to one value: its first result, `3`.
3. `min_max(1, 2)` is the last item, so it gives all its results: `1` and `2`.
4. `print` receives three values: `3`, `1`, and `2`.

So it prints `3  1  2`, and the `7` that the first call also returned is lost.

### Exercise 2.1 (LO-2.1, ★, about 10 minutes)

Choose a loop for each task and write its first line. The first is done for you.

1. Print 10, 8, 6, 4, 2, 0: a numeric `for`, `for i = 10, 0, -2 do`.
2. Ask for a password until the user types one that is long enough.
3. Print every name in a list called `names`, with its position.
4. Keep doubling a number `x` until it is larger than 1,000.

<details>
<summary>Answer</summary>

2. `repeat`, because the program must ask once before there is anything to check:
   `repeat … until #password >= 8`.
3. The generic `for` with `ipairs`: `for i, name in ipairs(names) do`.
4. `while x <= 1000 do`, because the condition decides whether to double at all. A `repeat`
   would double `x` once even if it already exceeded 1,000.
</details>

### Exercise 2.2 (LO-2.1, ★★, about 10 minutes)

Predict exactly what this prints, including the spacing.

```lua
local i = 100
local n = 2
for i = 1, n do
  n = n + 1
  io.write(i, " ")
end
print(i, n)
```

<details>
<summary>Hint</summary>

How many times does the loop run, given that its bound is computed once? Which `i` does the last
line read?
</details>

<details>
<summary>Answer</summary>

`1 2 100  4` on one line. The loop runs twice, because its bound was 2 when it started; changing
`n` later doesn't matter. `io.write` prints no newline, so `print`'s output continues the line.
The loop's `i` is a new local, so the last line reads the outer `i`, still 100. `n` was
incremented twice, to 4.
</details>

### Exercise 2.3 (LO-2.2, ★★, about 15 minutes)

With `local function f() return "a", "b", "c" end`, give the result of each line. The first is
done for you.

1. `local x, y = f()` sets `x` to `"a"` and `y` to `"b"`; the `"c"` is dropped.
2. `local t = { f(), f() }`: what are the items of `t`, and what is `#t`?
3. `print((f()))`
4. `print(string.rep(f()))`
5. `select("#", f(), nil)`

<details>
<summary>Hint</summary>

For each call, ask whether it is the last item in its list, and whether it has parentheses
around it.
</details>

<details>
<summary>Answer</summary>

2. `{ "a", "a", "b", "c" }`, so `#t` is 4. The first call isn't last and gives one value.
3. `a`. The parentheses keep only the first result.
4. An error: `bad argument #2 to 'rep' (number expected, got string)`. `string.rep` received all
   three results, so its second argument, the repeat count, is `"b"`.
5. `2`. `f()` isn't last, so it gives one value, and `nil` is the second.
</details>

### Exercise 2.4 (LO-2.3, ★★, about 10 minutes)

Which of these `return` statements are proper tail calls?

1. `return helper(n - 1)`
2. `return helper(n - 1) or 0`
3. `return self.next:visit(x)`
4. `return (helper(n))`
5. `return helper(n), n`
6. `return obj.handlers[name](event)`

<details>
<summary>Answer</summary>

1, 3, and 6. Each is `return` followed by exactly one call. The call can be a method call (3) or
a call of a value looked up in a table (6). Statement 2 applies `or` after the call returns, 4
truncates the results, and 5 adds a value, so in each the caller still has work to do.
</details>

### Exercise 2.5 (LO-2.3, ★★★, about 20 minutes)

Write `fib(n)`, which returns the `n`th Fibonacci number (`fib(0)` is 0, `fib(1)` is 1, and each
number after is the sum of the two before it). It must be recursive, it must use only proper tail
calls, and it must work when called with one argument. Then answer: `fib(92)` is
7540113804746346429. What does your function return for `fib(93)`, and why?

<details>
<summary>Hint</summary>

Carry two accumulators, the current Fibonacci number and the next one, and count `n` down to 0.
</details>

<details>
<summary>Answer</summary>

```lua
local function fib(n, a, b)
  a = a or 0
  b = b or 1
  if n == 0 then return a end
  return fib(n - 1, b, a + b)
end
```

`fib(93)` returns -6246583658587674878, a negative number. The true value is larger than
`math.maxinteger`, and integer addition wraps around without an error, as module 1 showed. A
tail call removed the stack's limit, but not the integers' limit.
</details>

### Exercise 2.6 (LO-2.4, ★★, about 15 minutes)

A function is called as `connect(host, port, timeout, retries, secure)`, and callers keep passing
the arguments in the wrong order. Redesign it to take a table of options, where `host` is required
and the others default to 443, 30, 3, and `true`. For each default, say whether `opts.x or
default` is correct, given that `retries = 0` and `secure = false` are both valid.

<details>
<summary>Answer</summary>

Call it as `connect{ host = "example.org", retries = 0 }`. Inside, `local port = opts.port or
443` and `local timeout = opts.timeout or 30` are correct. `local retries = opts.retries or 3` is
correct too, although 0 is a valid value, because 0 is truthy in Lua, so `0 or 3` is `0`.
`secure` is the one that needs `if opts.secure == nil then secure = true end`, because
`false or true` would turn `secure = false` into `true`. `host` has no default; module 6 shows how
to report a missing one as an error.
</details>

# Module 8 practice

These exercises practice the [Module 8 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: tracing a method call through a subclass

With `Account` and `Savings` from the reading, and `s = Savings.new(100, 0.05)`, which functions
run, in order, for `s:add_interest()`?

1. `s:add_interest()` looks up `add_interest`. `s` holds only `balance` and `rate`, so the lookup
   goes to `s`'s metatable, `Savings`, whose `__index` is `Savings`. It holds `add_interest`, so
   `Savings.add_interest(s)` runs.
2. Inside it, `self:deposit(…)` looks up `deposit` in `s`, then in `Savings`, which doesn't have
   it. `Savings`'s own metatable has `__index = Account`, so the lookup continues there, and
   `Account.deposit(s, 5.0)` runs.
3. `Account.deposit` changes `s.balance`: `self` is `s`, not `Account`, because the colon passed
   `s` all the way down.

So the calls are `Savings.add_interest`, then `Account.deposit`, both with `s` as `self`, and the
balance becomes 105.0.

### Exercise 8.1 (LO-8.1, ★, about 10 minutes)

Given `local p = Point.new(1, 2)`, which of these calls work, and what does each failing one do?

1. `p:move(3, 4)`
2. `p.move(3, 4)`
3. `p.move(p, 3, 4)`
4. `Point.move(p, 3, 4)`

<details>
<summary>Answer</summary>

1, 3, and 4 work, and do the same thing. 2 passes 3 as `self` and 4 as the first coordinate, so
the method fails at its first use of `self`, with `attempt to index a number value (local
'self')`.
</details>

### Exercise 8.2 (LO-8.1, ★★, about 20 minutes)

Write a class `Rect` with `Rect.new(w, h)`, `r:area()`, and `r:scale(factor)`, which multiplies
both sides and returns `r` itself, so that calls can be chained: `Rect.new(2, 3):scale(2):area()`
is 24. Add `==`, true when both sides match, and `tostring`, as in `Rect(4x6)`.

<details>
<summary>Answer</summary>

```lua
local Rect = {}
Rect.__index = Rect

function Rect.new(w, h)
  return setmetatable({ w = w, h = h }, Rect)
end

function Rect:area()
  return self.w * self.h
end

function Rect:scale(factor)
  self.w, self.h = self.w * factor, self.h * factor
  return self
end

function Rect.__eq(a, b)
  return a.w == b.w and a.h == b.h
end

function Rect.__tostring(r)
  return "Rect(" .. r.w .. "x" .. r.h .. ")"
end

print(Rect.new(2, 3):scale(2):area(), Rect.new(2, 3):scale(2))   --> 24  Rect(4x6)
```

Returning `self` is what lets `:scale(2):area()` chain: each call works on the object the previous
one returned.
</details>

### Exercise 8.3 (LO-8.2, ★★, about 15 minutes)

A colleague makes `Square` a subclass of `Rect` from Exercise 8.2, with `Square.new(side)`. Then
someone adds `function Rect:set_width(w) self.w = w end`. What goes wrong for squares? Would
composition have avoided it?

<details>
<summary>Answer</summary>

`Square` inherits `set_width`, so `sq:set_width(5)` makes a "square" with different sides, which
breaks the one rule that defines a square. Inheritance promised that a square can do everything a
rectangle can, and that promise became false when `Rect` grew a method. With composition, a
`Square` that holds a `Rect` and forwards only `area`, `scale`, and `tostring` never gets
`set_width`, so the change to `Rect` can't reach it. This is the coupling the reading's table
describes: a subclass depends on everything its parent offers, now and later.
</details>

### Exercise 8.4 (LO-8.2, ★★, about 10 minutes)

This override is meant to add an exclamation mark to the parent's report. What happens when it
runs, and how do you fix it?

```lua
function Savings:report()
  return self:report() .. "!"
end
```

<details>
<summary>Answer</summary>

`self:report()` finds `Savings.report` again, since `self` is a `Savings` object, so the method
calls itself until Lua stops it with `stack overflow`. Call the parent's version through the
parent: `return Account.report(self) .. "!"`.
</details>

### Exercise 8.5 (LO-8.3, ★★, about 15 minutes)

Write `new_wallet(balance)`, a closure-based object with `deposit(amount)`, which raises an error
for an amount that isn't positive, and `balance()`. Show that no code outside it can set the
balance directly.

<details>
<summary>Answer</summary>

```lua
local function new_wallet(balance)
  local self = {}
  function self.deposit(amount)
    if type(amount) ~= "number" or amount <= 0 then
      error("deposit: amount must be positive", 2)
    end
    balance = balance + amount
  end
  function self.balance()
    return balance
  end
  return self
end

local w = new_wallet(10)
w.deposit(5)
w.balance = 1000000      -- replaces the method, but not the balance
print(pcall(w.deposit, -3))
```

The last assignment replaces the field `balance` of the object, which held a function, with a
number; the real balance, the local in `new_wallet`, is still 15, and `w.deposit` still sees it.
The object can be broken this way, but its state can't be changed except through `deposit`.
</details>

### Exercise 8.6 (LO-8.3, ★★, about 10 minutes)

Choose metatable-based or closure-based objects for each, and say why.

1. A logger that plugins receive, which they may call but must not reconfigure.
2. The 50,000 cells of a spreadsheet, each with a value and a formula.
3. A `Vector` type with `+` and `*`.

<details>
<summary>Answer</summary>

1. Closures: there is one logger, its settings must be private, and the memory per object doesn't
   matter.
2. Metatables: closures would add one closure per method to each of 50,000 cells, and the cells
   need no privacy.
3. Metatables: operators need metamethods, which a class provides once for every vector, while a
   closure-based object would need a metatable of its own anyway.
</details>

# Module 8: Objects and classes

**Objectives:** LO-8.1, LO-8.2, LO-8.3\
**Prerequisites:** [Module 7](../07-metatables/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 8](lab08.ipynb), 1.5 for the
[practice](practice.md), and 3 for the midterm exam, which is this week

Lua has no `class` keyword. An object is a table that holds its own data, and a class is a table
of the methods its objects share, connected to them through `__index` from module 7. This module
builds a class, a subclass, and the same design by composition, and then a second kind of object
whose state hides in closures. Each approach costs different amounts of memory and time, and
allows different things, so the module measures them and says when to choose each.

## Methods and the colon

A **method** is a function that works on the object it is called on. Module 4 introduced the
colon for strings; it works for any table. A call written with a colon passes the object as a
hidden first argument, and a function defined with a colon receives it as a parameter named
`self`:

```lua
local counter = { count = 0 }

function counter:increment(by)       -- the same as: function counter.increment(self, by)
  self.count = self.count + (by or 1)
end

counter:increment(5)                 -- the same as: counter.increment(counter, 5)
print(counter.count)                 --> 5
```

The colon is only shorthand, and the two sides must agree. Calling a method with a dot,
`counter.increment(5)`, passes 5 as `self`, and the method stops with
`attempt to index a number value (local 'self')`. That message is the usual sign of a dot where
a colon belongs.

## A class

A class is a table that holds the methods, and serves as the metatable of every object it makes,
with its `__index` pointing at itself:

```lua
local Account = {}
Account.__index = Account

function Account.new(balance)
  return setmetatable({ balance = balance or 0 }, Account)
end

function Account:deposit(amount)
  self.balance = self.balance + amount
end

function Account:report()
  return "balance " .. self.balance
end

function Account.__tostring(account)
  return "Account(" .. account.balance .. ")"
end

local a = Account.new(100)
a:deposit(50)
print(a:report(), a)            --> balance 150  Account(150)
print(rawget(a, "deposit"))     --> nil
```

When `a:deposit(50)` runs, Lua looks for `deposit` in `a`, which holds only `balance`. It misses,
so Lua follows `a`'s metatable, `Account`, to its `__index`, which is `Account` again, and finds
the function there. Each object holds only its own data, and every object shares one copy of each
method. `Account.new` is called with a dot, because it makes an object rather than working on
one; the constructor's name is a convention, and `new` is the most common.

A class can also hold default values for fields. With `Account.balance = 0`, an object without its
own `balance` reads 0 through `__index`, and its first `deposit` creates its own field. Never use
a table as such a default: every object would share that one table, and a change made through one
object would appear in all of them.

## Inheritance

A **subclass** is a class whose own `__index` lookup falls back on a parent class. Objects of
the subclass find their own methods first, then the parent's:

```lua
local Savings = setmetatable({}, { __index = Account })
Savings.__index = Savings

function Savings.new(balance, rate)
  local account = Account.new(balance)      -- build the parent's part
  account.rate = rate
  return setmetatable(account, Savings)     -- then make it a Savings object
end

function Savings:add_interest()
  self:deposit(self.balance * self.rate)    -- inherited from Account
end

function Savings:report()                   -- overrides Account's report
  return Account.report(self) .. " at " .. self.rate
end

local s = Savings.new(100, 0.05)
s:add_interest()
print(s:report())        --> balance 105.0 at 0.05
```

A lookup of `s:deposit` now takes three steps: `s` misses, `Savings` misses, and `Savings`'s own
metatable sends the lookup on to `Account`, which has it. An overriding method that needs the
parent's version calls it through the parent, with an explicit `self`: `Account.report(self)`.
Calling `self:report()` there would call `Savings.report` again, recursing until the stack
overflows.

### Metamethods aren't inherited

`print(s)` prints `table: 0x…`, not `Account(105.0)`. Lua reads a metamethod straight from the
metatable with a raw access, without following `__index`, so `Account.__tostring` is invisible
to objects whose metatable is `Savings`. Copy each metamethod a subclass should keep:

```lua
Savings.__tostring = Account.__tostring
print(s)                 --> Account(105.0)
```

### Is it an instance?

To ask whether an object belongs to a class or to one of its subclasses, walk up the chain of
metatables:

```lua
local function is_instance(object, class)
  local mt = getmetatable(object)
  while mt do
    if mt == class then return true end
    local parent = getmetatable(mt)
    mt = parent and parent.__index
  end
  return false
end

print(is_instance(s, Account), is_instance(a, Savings))     --> true  false
```

## Composition

Inheritance says that a `Savings` object **is an** `Account`, and can go anywhere an account can.
**Composition** says that a `Savings` object **has an** account, which it uses to do part of its
job, and offers only the methods it chooses:

```lua
local Savings2 = {}
Savings2.__index = Savings2

function Savings2.new(balance, rate)
  return setmetatable({ account = Account.new(balance), rate = rate }, Savings2)
end

function Savings2:deposit(amount)           -- forwarded to the account
  self.account:deposit(amount)
end

function Savings2:add_interest()
  self.account:deposit(self.account.balance * self.rate)
end
```

| | Inheritance | Composition |
| :- | :- | :- |
| The relationship | The subclass is a kind of the parent | The object owns a part |
| Methods it gets | All of the parent's, automatically | Only those it forwards, one by one |
| Coupling | The subclass depends on the parent's fields and methods, so changing the parent can break it | The object depends only on the part's public methods |
| Replacing the part | Fixed when the class is written | Any object with the same methods, even at run time |

Prefer composition unless the subclass can truly stand in for its parent everywhere, as a
savings account can stand in for an account. A class that inherits only to reuse a few methods
gets every other method too, including ones that make no sense for it, and breaks when the
parent changes the fields it relied on. Lua programs usually keep inheritance shallow, one or two
levels, because each level adds one more table lookup to every method call that misses.

## Objects from closures

Module 5's counters kept their state in closures. The same idea makes objects with truly private
state: the data lives in locals of the constructor, and the object is a table of closures that
share them.

```lua
local function new_account(balance)
  local self = {}
  function self.deposit(amount) balance = balance + amount end
  function self.balance() return balance end
  return self
end

local b = new_account(100)
b.deposit(50)               -- a dot: there is no self to pass
print(b.balance())          --> 150
```

No code outside `new_account` can read or change `balance` except through the two functions.
With the metatable version, any code can write `a.balance = 1000000`. The price is memory: each
object carries one closure for each method, instead of sharing one copy.

On an Intel Core i7-11800H, with Lua 5.4.8 through lupa 2.8, 10,000 counters with four methods
each took about 106 bytes per counter as tables sharing a metatable, and 378 bytes per counter as
tables of four closures. Both figures include the 26 bytes each counter's slot in a list took.
Calling a closure method is faster, because it reads `count` as an upvalue instead of through
`self`: 5 million calls took 0.17 s with metatables and 0.10 s with closures. Lab 8 repeats both
measurements.

| | Metatable-based objects | Closure-based objects |
| :- | :- | :- |
| Memory per object | The data only; methods are shared | The data, plus one closure per method |
| Calls | `obj:method()`, through `__index` | `obj.method()`, with no lookup beyond the object |
| Privacy | None: every field is visible and writable | Complete: state is reachable only through the methods |
| Inheritance and overriding | Through `__index` chains | By hand: wrap or replace the functions in the table |
| Metamethods | Shared in the class | Each object needs its own metatable to have any |

Choose closures for a few long-lived objects whose state must be protected, such as a connection
or a configuration that plugins can read but not change. Choose metatables for many small
objects, such as the customers of a simulation, and for anything that needs inheritance or
operators.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| `obj.method()` and `obj:method()` are interchangeable | The colon passes `obj` as the first argument | `a.deposit(10)` stops with `attempt to index a number value (local 'self')` |
| Each object holds its own copy of the methods | Methods live once, in the class | `rawget(a, "deposit")` is `nil` |
| A table default in the class is per object | Every object shares that table | `Class.items = {}`, then `obj:add(x)` adds to every object |
| A subclass inherits `__tostring` and the operators | Metamethods are read raw from the metatable | `print(s)` shows `table: 0x…` until `__tostring` is copied |
| `self:report()` inside `Savings.report` calls the parent's | It calls the most specific one, the same function | Call `Account.report(self)` |
| Closure-based objects differ only in style | They trade memory for privacy and speed | 378 bytes per counter instead of 106 |

## Summary

- `obj:m(args)` is `obj.m(obj, args)`, and `function T:m()` is `function T.m(self)`; a dot where a
  colon belongs gives `attempt to index a … value (local 'self')`.
- A class is a table of methods that is also its objects' metatable, with `Class.__index = Class`;
  objects hold only their data.
- A subclass's own metatable has `__index` set to the parent, so lookups fall through; override by
  defining the method again, and call the parent's version as `Parent.method(self, …)`.
- Metamethods aren't inherited, because Lua reads them without following `__index`; copy them.
- Inheritance fits when the subclass can stand in for the parent everywhere; otherwise, compose:
  hold the part in a field and forward what you need.
- Closure-based objects keep state private and call faster, but take a closure per method per
  object.

## Self-check

1. Rewrite `function Shape:area() return self.w * self.h end` and the call `box:area()` without
   colons.

   <details>
   <summary>Answer</summary>

   `function Shape.area(self) return self.w * self.h end`, and `box.area(box)`.
   </details>

2. An object `c` of class `Counter` gives `nil` for `rawget(c, "increment")`, yet `c:increment()`
   works. Trace the lookup.

   <details>
   <summary>Answer</summary>

   `c` has no `increment`, so Lua takes `c`'s metatable, `Counter`, and reads its `__index`,
   which is `Counter`, where `increment` is stored. The method lives once, in the class.
   </details>

3. A class has `Queue.items = {}` as a default, and `function Queue:push(v) self.items[#self.items
   + 1] = v end`. What goes wrong with two queues?

   <details>
   <summary>Answer</summary>

   Neither queue has its own `items`, so both read `Queue.items` through `__index`, and push into
   that one shared table. Give each object its own table in the constructor:
   `setmetatable({ items = {} }, Queue)`.
   </details>

4. `Savings` inherits from `Account`. Why does `s1 + s2` fail for two savings accounts when
   `Account` defines `__add`, and how do you fix it?

   <details>
   <summary>Answer</summary>

   Lua reads `__add` from the operands' metatable, `Savings`, with a raw access, and doesn't
   follow `Savings`'s own `__index` to `Account`. Copy it: `Savings.__add = Account.__add`.
   </details>

5. A game has 200,000 bullets on screen, each with a position, a speed, and three methods. Would
   you build them with metatables or with closures? Why?

   <details>
   <summary>Answer</summary>

   With metatables. The measurement above found closures cost about 270 more bytes per object for
   four methods; even for three, that is tens of megabytes for 200,000 bullets. Bullets don't
   need private state, so the closures would buy nothing.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [3.4.10, Function Calls](https://www.lua.org/manual/5.4/manual.html#3.4.10) and
  [3.4.11, Function Definitions](https://www.lua.org/manual/5.4/manual.html#3.4.11), which define
  the colon as shorthand, and [2.4, Metatables and Metamethods](https://www.lua.org/manual/5.4/manual.html#2.4),
  which says that metamethods are read with a raw access.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapter on
  object-oriented programming covers classes, inheritance, multiple inheritance through an
  `__index` function, and privacy with closures.

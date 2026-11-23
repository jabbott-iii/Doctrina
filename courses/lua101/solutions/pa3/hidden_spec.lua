-- hidden_spec.lua: the hidden tests for PA3. tools/grade_project.py runs them against a
-- submission's iter.lua, and weights each describe block by the points in its name.

local iter = require("iter")

-- Calls fn, which must raise an error, and returns the message.
local function message_of(fn)
  local ok, err = pcall(fn)
  assert(not ok, "expected an error, but the call returned normally")
  return err
end

-- The error must be raised at level 2: its position names this file, the caller, not iter.lua.
local function assert_blames_caller(err)
  assert.is_truthy(tostring(err):find("hidden_spec.lua:%d+:"),
    "the error should name the caller's line, not a line in iter.lua: " .. tostring(err))
end

-- An iterator over 1, 2, 3, … that counts how many times it has been called.
local function counted(limit)
  local source = { calls = 0 }
  function source.next()
    source.calls = source.calls + 1
    if limit == nil or source.calls <= limit then return source.calls end
  end
  return source
end

describe("iter.from_list (5 points)", function()
  it("gives the values in order, then nil", function()
    local it = iter.from_list({ "a", "b" })
    assert.are.equal("a", it())
    assert.are.equal("b", it())
    assert.is_nil(it())
    assert.is_nil(it())
  end)

  it("keeps false values", function()
    assert.are.same({ false, true, false }, iter.to_list(iter.from_list({ false, true, false })))
  end)

  it("gives nothing for an empty list", function()
    assert.is_nil(iter.from_list({})())
  end)

  it("raises an error for a value that isn't a table", function()
    local err = message_of(function() iter.from_list("abc") end)
    assert.is_truthy(err:find("from_list: list must be a table", 1, true))
    assert_blames_caller(err)
  end)
end)

describe("iter.count (5 points)", function()
  it("counts from 1 in steps of 1 by default", function()
    assert.are.same({ 1, 2, 3 }, iter.to_list(iter.take(3, iter.count())))
  end)

  it("uses start and step", function()
    assert.are.same({ 10, 15, 20 }, iter.to_list(iter.take(3, iter.count(10, 5))))
    assert.are.same({ 0, -2, -4 }, iter.to_list(iter.take(3, iter.count(0, -2))))
  end)

  it("raises an error for a step of 0", function()
    local err = message_of(function() iter.count(1, 0) end)
    assert.is_truthy(err:find("count: step must not be 0", 1, true))
    assert_blames_caller(err)
  end)

  it("raises an error for a start or step that isn't a number", function()
    local err = message_of(function() iter.count("1") end)
    assert.is_truthy(err:find("count: start and step must be numbers", 1, true))
    assert.has_error(function() iter.count(1, "2") end, "count: start and step must be numbers")
  end)
end)

describe("iter.map (8 points)", function()
  it("applies fn to each value", function()
    local squares = iter.map(function(x) return x * x end, iter.from_list({ 1, 2, 3 }))
    assert.are.same({ 1, 4, 9 }, iter.to_list(squares))
  end)

  it("is lazy: it calls fn and the source only when asked", function()
    local source = counted()
    local calls = 0
    local doubled = iter.map(function(x) calls = calls + 1; return 2 * x end, source.next)
    assert.are.equal(0, source.calls)
    assert.are.equal(2, doubled())
    assert.are.equal(4, doubled())
    assert.are.equal(2, source.calls)
    assert.are.equal(2, calls)
  end)

  it("works on an infinite iterator", function()
    assert.are.same({ 2, 4, 6 }, iter.to_list(iter.take(3, iter.map(function(x) return 2 * x end,
      iter.count()))))
  end)

  it("keeps a result of false", function()
    local negated = iter.map(function(x) return not x end, iter.from_list({ true, false }))
    assert.are.same({ false, true }, iter.to_list(negated))
  end)

  it("raises an error when fn returns nil", function()
    local broken = iter.map(function() return nil end, iter.from_list({ 1 }))
    local err = message_of(function() return broken() end)
    assert.is_truthy(err:find("map: fn returned nil", 1, true))
  end)

  it("raises an error for an fn or it that isn't a function", function()
    local err = message_of(function() iter.map("upper", iter.from_list({})) end)
    assert.is_truthy(err:find("map: fn must be a function", 1, true))
    assert_blames_caller(err)
    err = message_of(function() iter.map(tostring, { 1, 2 }) end)
    assert.is_truthy(err:find("map: it must be a function", 1, true))
  end)
end)

describe("iter.filter (8 points)", function()
  it("keeps the values for which pred is true", function()
    local evens = iter.filter(function(x) return x % 2 == 0 end, iter.from_list({ 1, 2, 3, 4 }))
    assert.are.same({ 2, 4 }, iter.to_list(evens))
  end)

  it("treats any truthy result as true, and nil as false", function()
    local kept = iter.filter(function(x) if x > 1 then return x end end, iter.from_list({ 1, 2, 3 }))
    assert.are.same({ 2, 3 }, iter.to_list(kept))
  end)

  it("works on an infinite iterator", function()
    local odd = iter.filter(function(x) return x % 2 == 1 end, iter.count())
    assert.are.same({ 1, 3, 5 }, iter.to_list(iter.take(3, odd)))
  end)

  it("ends when its source ends, even if nothing passed", function()
    assert.is_nil(iter.filter(function() return false end, iter.from_list({ 1, 2 }))())
  end)

  it("raises an error for a pred or it that isn't a function", function()
    local err = message_of(function() iter.filter(nil, iter.count()) end)
    assert.is_truthy(err:find("filter: pred must be a function", 1, true))
    assert_blames_caller(err)
    assert.has_error(function() iter.filter(tostring, "x") end, "filter: it must be a function")
  end)
end)

describe("iter.take (10 points)", function()
  it("gives the first n values", function()
    assert.are.same({ "a", "b" }, iter.to_list(iter.take(2, iter.from_list({ "a", "b", "c" }))))
  end)

  it("gives fewer when the source ends first", function()
    assert.are.same({ 1, 2 }, iter.to_list(iter.take(5, iter.from_list({ 1, 2 }))))
  end)

  it("gives nothing for n = 0, without calling the source", function()
    local source = counted()
    assert.is_nil(iter.take(0, source.next)())
    assert.are.equal(0, source.calls)
  end)

  it("never calls the source after the nth value", function()
    local source = counted()
    iter.to_list(iter.take(2, source.next))
    assert.are.equal(2, source.calls)
    assert.are.equal(3, source.next())
  end)

  it("doesn't call the source again once it has ended", function()
    local source = counted(1)
    local it = iter.take(5, source.next)
    it(); it(); it(); it()
    assert.are.equal(2, source.calls)
  end)

  it("raises an error for an n that isn't a non-negative integer", function()
    for _, n in ipairs({ -1, 1.5, "3" }) do
      local err = message_of(function() iter.take(n, iter.count()) end)
      assert.is_truthy(err:find("take: n must be a non-negative integer", 1, true))
    end
    assert_blames_caller(message_of(function() iter.take(-1, iter.count()) end))
    assert.has_error(function() iter.take(nil, iter.count()) end,
      "take: n must be a non-negative integer")
  end)

  it("raises an error for an it that isn't a function", function()
    assert.has_error(function() iter.take(2, { 1, 2, 3 }) end, "take: it must be a function")
  end)
end)

describe("iter.zip (8 points)", function()
  it("gives pairs of values", function()
    local z = iter.zip(iter.from_list({ "a", "b" }), iter.from_list({ 1, 2 }))
    local x, y = z()
    assert.are.equal("a", x)
    assert.are.equal(1, y)
    x, y = z()
    assert.are.equal("b", x)
    assert.are.equal(2, y)
    assert.is_nil(z())
  end)

  it("ends when the shorter iterator ends", function()
    local n = 0
    for _ in iter.zip(iter.count(), iter.from_list({ "x", "y", "z" })) do n = n + 1 end
    assert.are.equal(3, n)
  end)

  it("calls b only when a gave a value", function()
    local b = counted()
    local z = iter.zip(iter.from_list({ "only" }), b.next)
    z(); z()
    assert.are.equal(1, b.calls)
  end)

  it("calls neither iterator once it has ended", function()
    local a, b = counted(), counted(1)
    local z = iter.zip(a.next, b.next)
    z(); z(); z(); z()
    assert.are.equal(2, a.calls)
    assert.are.equal(2, b.calls)
  end)

  it("raises an error for an argument that isn't a function", function()
    local err = message_of(function() iter.zip(iter.count(), {}) end)
    assert.is_truthy(err:find("zip: a and b must be functions", 1, true))
    assert_blames_caller(err)
  end)
end)

describe("iter.split (10 points)", function()
  it("splits at each separator", function()
    assert.are.same({ "a", "b", "c" }, iter.to_list(iter.split("a,b,c", ",")))
  end)

  it("keeps empty fields, at the ends too", function()
    assert.are.same({ "a", "", "b" }, iter.to_list(iter.split("a,,b", ",")))
    assert.are.same({ "", "a", "" }, iter.to_list(iter.split(",a,", ",")))
  end)

  it("gives one empty field for the empty string", function()
    assert.are.same({ "" }, iter.to_list(iter.split("", ",")))
  end)

  it("gives the whole string when the separator is absent", function()
    assert.are.same({ "no separator" }, iter.to_list(iter.split("no separator", ";")))
  end)

  it("treats the separator as plain text, not a pattern", function()
    assert.are.same({ "1", "2", "3" }, iter.to_list(iter.split("1.2.3", ".")))
    assert.are.same({ "50", "25" }, iter.to_list(iter.split("50%25", "%")))
  end)

  it("handles separators longer than one character", function()
    assert.are.same({ "a", "b", "-c" }, iter.to_list(iter.split("a--b---c", "--")))
  end)

  it("raises an error for an empty separator or a non-string", function()
    local err = message_of(function() iter.split("abc", "") end)
    assert.is_truthy(err:find("split: sep must be a non-empty string", 1, true))
    assert_blames_caller(err)
    assert.has_error(function() iter.split(42, ",") end, "split: s must be a string")
  end)
end)

describe("iter.to_list (4 points)", function()
  it("collects every value, false included", function()
    assert.are.same({ 1, false, "x" }, iter.to_list(iter.from_list({ 1, false, "x" })))
  end)

  it("gives an empty list for an empty iterator", function()
    assert.are.same({}, iter.to_list(iter.from_list({})))
  end)

  it("raises an error for a value that isn't a function", function()
    local err = message_of(function() iter.to_list({ 1, 2 }) end)
    assert.is_truthy(err:find("to_list: it must be a function", 1, true))
    assert_blames_caller(err)
  end)
end)

describe("iter.memoize (12 points)", function()
  it("calls fn once for each argument", function()
    local calls = 0
    local square = iter.memoize(function(x) calls = calls + 1; return x * x end)
    assert.are.equal(9, square(3))
    assert.are.equal(9, square(3))
    assert.are.equal(16, square(4))
    assert.are.equal(2, calls)
  end)

  it("caches results of nil and false", function()
    local calls = 0
    local f = iter.memoize(function(x)
      calls = calls + 1
      if x == "no" then return false end
      return nil
    end)
    assert.is_nil(f("nothing"))
    assert.is_nil(f("nothing"))
    assert.are.equal(false, f("no"))
    assert.are.equal(false, f("no"))
    assert.are.equal(2, calls)
  end)

  it("gives each memoized function a cache of its own", function()
    local a = iter.memoize(function(x) return x + 1 end)
    local b = iter.memoize(function(x) return x - 1 end)
    assert.are.equal(6, a(5))
    assert.are.equal(4, b(5))
  end)

  it("works with false and tables as arguments", function()
    local calls = 0
    local f = iter.memoize(function(x) calls = calls + 1; return type(x) end)
    local t = {}
    assert.are.equal("boolean", f(false))
    assert.are.equal("table", f(t))
    f(false); f(t)
    assert.are.equal(2, calls)
  end)

  it("raises an error for a nil or NaN argument", function()
    local f = iter.memoize(tostring)
    local err = message_of(function() f(nil) end)
    assert.is_truthy(err:find("memoize: the argument must not be nil or NaN", 1, true))
    assert_blames_caller(err)
    assert.has_error(function() f(0 / 0) end, "memoize: the argument must not be nil or NaN")
  end)

  it("raises an error for an fn that isn't a function", function()
    assert.has_error(function() iter.memoize(42) end, "memoize: fn must be a function")
  end)
end)

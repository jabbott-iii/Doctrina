-- iter_spec.lua: a model student test suite for PA3, which earns full marks on the rubric's
-- Tests criterion. tools/grade_project.py --self-test runs it against the model and the broken
-- versions.

local iter = require("iter")

-- A source that counts its calls, for testing that functions are lazy.
local function counter(limit)
  local source = { calls = 0 }
  function source.next()
    source.calls = source.calls + 1
    if limit == nil or source.calls <= limit then return source.calls end
  end
  return source
end

describe("iter.from_list", function()
  it("gives the values in order, then nil", function()
    assert.are.same({ "a", "b", "c" }, iter.to_list(iter.from_list({ "a", "b", "c" })))
  end)

  it("keeps false values", function()
    assert.are.same({ true, false, true }, iter.to_list(iter.from_list({ true, false, true })))
  end)

  it("raises an error for a value that isn't a table", function()
    assert.has_error(function() iter.from_list(5) end, "from_list: list must be a table")
  end)
end)

describe("iter.count", function()
  it("counts from 1 by default", function()
    assert.are.same({ 1, 2, 3 }, iter.to_list(iter.take(3, iter.count())))
  end)

  it("uses start and step", function()
    assert.are.same({ 5, 8, 11 }, iter.to_list(iter.take(3, iter.count(5, 3))))
  end)

  it("raises an error for a step of 0", function()
    assert.has_error(function() iter.count(1, 0) end, "count: step must not be 0")
  end)
end)

describe("iter.map", function()
  it("applies fn to every value", function()
    local doubled = iter.map(function(x) return 2 * x end, iter.from_list({ 1, 2, 3 }))
    assert.are.same({ 2, 4, 6 }, iter.to_list(doubled))
  end)

  it("calls its source only when asked", function()
    local source = counter()
    local mapped = iter.map(function(x) return x end, source.next)
    assert.are.equal(0, source.calls)
    mapped()
    assert.are.equal(1, source.calls)
  end)

  it("raises an error when fn returns nil", function()
    local mapped = iter.map(function() end, iter.from_list({ 1 }))
    assert.has_error(function() mapped() end, "map: fn returned nil")
  end)

  it("raises an error when fn isn't a function", function()
    assert.has_error(function() iter.map(1, iter.count()) end, "map: fn must be a function")
  end)
end)

describe("iter.filter", function()
  it("keeps the values that pass", function()
    local small = iter.filter(function(x) return x < 3 end, iter.from_list({ 1, 5, 2, 7 }))
    assert.are.same({ 1, 2 }, iter.to_list(small))
  end)

  it("treats any truthy result as passing", function()
    local named = iter.filter(function(x) return x.name end,
      iter.from_list({ { name = "a" }, {}, { name = "b" } }))
    assert.are.equal(2, #iter.to_list(named))
  end)
end)

describe("iter.take", function()
  it("gives the first n values, or fewer", function()
    assert.are.same({ 1, 2 }, iter.to_list(iter.take(2, iter.count())))
    assert.are.same({ "x" }, iter.to_list(iter.take(4, iter.from_list({ "x" }))))
  end)

  it("never asks its source for more than n values", function()
    local source = counter()
    iter.to_list(iter.take(3, source.next))
    assert.are.equal(3, source.calls)
  end)

  it("raises an error for a negative or fractional n", function()
    assert.has_error(function() iter.take(-1, iter.count()) end,
      "take: n must be a non-negative integer")
    assert.has_error(function() iter.take(0.5, iter.count()) end,
      "take: n must be a non-negative integer")
  end)
end)

describe("iter.zip", function()
  it("pairs values until the shorter ends", function()
    local letters, numbers = {}, {}
    for letter, number in iter.zip(iter.from_list({ "a", "b", "c" }), iter.count()) do
      letters[#letters + 1], numbers[#numbers + 1] = letter, number
    end
    assert.are.same({ "a", "b", "c" }, letters)
    assert.are.same({ 1, 2, 3 }, numbers)
  end)

  it("doesn't call b once a has ended", function()
    local b = counter()
    iter.to_list(iter.zip(iter.from_list({ 1, 2 }), b.next))
    assert.are.equal(2, b.calls)
  end)
end)

describe("iter.split", function()
  it("keeps empty fields", function()
    assert.are.same({ "a", "", "b", "" }, iter.to_list(iter.split("a,,b,", ",")))
  end)

  it("treats the separator as plain text", function()
    assert.are.same({ "x", "y" }, iter.to_list(iter.split("x.y", ".")))
  end)

  it("raises an error for an empty separator", function()
    assert.has_error(function() iter.split("abc", "") end, "split: sep must be a non-empty string")
  end)
end)

describe("iter.memoize", function()
  it("calls fn once per argument, even when it returns nil", function()
    local calls = 0
    local f = iter.memoize(function(x)
      calls = calls + 1
      if x > 0 then return x end
    end)
    f(1); f(1); f(-1); f(-1)
    assert.are.equal(2, calls)
    assert.is_nil(f(-1))
  end)

  it("raises an error for a nil argument", function()
    local f = iter.memoize(tostring)
    assert.has_error(function() f(nil) end, "memoize: the argument must not be nil or NaN")
  end)
end)

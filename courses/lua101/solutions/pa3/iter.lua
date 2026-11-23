-- iter.lua: lazy iterators, the model solution for LUA101's PA3.
--
-- An iterator here is a function that returns the next value each time it is called, and nil
-- once it has no more. Every function that takes an iterator is lazy: it calls its source only
-- when its own caller asks for the next value.

local iter = {}

-- Raises "name: message" at the line that called the public function: level 1 is this
-- function, level 2 the public function, and level 3 its caller.
local function fail(name, message)
  error(name .. ": " .. message, 3)
end

function iter.from_list(list)
  if type(list) ~= "table" then fail("from_list", "list must be a table") end
  local i = 0
  return function()
    i = i + 1
    return list[i]
  end
end

function iter.count(start, step)
  start, step = start or 1, step or 1
  if type(start) ~= "number" or type(step) ~= "number" then
    fail("count", "start and step must be numbers")
  end
  if step == 0 then fail("count", "step must not be 0") end
  local n = 0
  return function()
    n = n + 1
    return start + (n - 1) * step
  end
end

function iter.map(fn, it)
  if type(fn) ~= "function" then fail("map", "fn must be a function") end
  if type(it) ~= "function" then fail("map", "it must be a function") end
  return function()
    local value = it()
    if value == nil then return nil end
    local result = fn(value)
    if result == nil then error("map: fn returned nil", 2) end
    return result
  end
end

function iter.filter(pred, it)
  if type(pred) ~= "function" then fail("filter", "pred must be a function") end
  if type(it) ~= "function" then fail("filter", "it must be a function") end
  return function()
    while true do
      local value = it()
      if value == nil then return nil end
      if pred(value) then return value end
    end
  end
end

function iter.take(n, it)
  if math.type(n) ~= "integer" or n < 0 then
    fail("take", "n must be a non-negative integer")
  end
  if type(it) ~= "function" then fail("take", "it must be a function") end
  local taken, done = 0, false
  return function()
    if done or taken >= n then return nil end
    local value = it()
    if value == nil then
      done = true
      return nil
    end
    taken = taken + 1
    return value
  end
end

function iter.zip(a, b)
  if type(a) ~= "function" or type(b) ~= "function" then
    fail("zip", "a and b must be functions")
  end
  local done = false
  return function()
    if done then return nil end
    local x = a()
    if x == nil then
      done = true
      return nil
    end
    local y = b()
    if y == nil then
      done = true
      return nil
    end
    return x, y
  end
end

function iter.split(s, sep)
  if type(s) ~= "string" then fail("split", "s must be a string") end
  if type(sep) ~= "string" or sep == "" then fail("split", "sep must be a non-empty string") end
  local position, done = 1, false
  return function()
    if done then return nil end
    local first, last = s:find(sep, position, true)
    if first == nil then
      done = true
      return s:sub(position)
    end
    local field = s:sub(position, first - 1)
    position = last + 1
    return field
  end
end

function iter.to_list(it)
  if type(it) ~= "function" then fail("to_list", "it must be a function") end
  local list = {}
  while true do
    local value = it()
    if value == nil then break end
    list[#list + 1] = value
  end
  return list
end

function iter.memoize(fn)
  if type(fn) ~= "function" then fail("memoize", "fn must be a function") end
  local NIL = {}      -- stands for a cached nil, which a table can't store
  local cache = {}
  return function(x)
    if x == nil or x ~= x then
      error("memoize: the argument must not be nil or NaN", 2)
    end
    local result = cache[x]
    if result == nil then
      result = fn(x)
      if result == nil then result = NIL end
      cache[x] = result
    end
    if result == NIL then return nil end
    return result
  end
end

return iter

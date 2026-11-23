-- iter.lua: lazy iterators, for LUA101's PA3.
-- Tools used: write "none", or say which tools you used and how.
-- Discussed with: write "no one", or name everyone you discussed this assignment with.
--
-- An iterator here is a function that returns the next value each time it is called, and nil
-- once it has no more. Every function that takes an iterator is lazy: it calls its source only
-- when its own caller asks for the next value. The handout, README.md, says exactly what each
-- function must do, and which error each one raises.

local iter = {}

-- Returns an iterator over the values of the sequence `list`, in order.
function iter.from_list(list)
  error("not implemented")
end

-- Returns an endless iterator over start, start + step, start + 2 * step, ...
function iter.count(start, step)
  error("not implemented")
end

-- Returns an iterator over fn(v) for each value v of `it`.
function iter.map(fn, it)
  error("not implemented")
end

-- Returns an iterator over the values v of `it` for which pred(v) is truthy.
function iter.filter(pred, it)
  error("not implemented")
end

-- Returns an iterator over the first n values of `it`.
function iter.take(n, it)
  error("not implemented")
end

-- Returns an iterator over pairs of values, one from `a` and one from `b`.
function iter.zip(a, b)
  error("not implemented")
end

-- Returns an iterator over the fields of `s` between occurrences of the plain text `sep`.
function iter.split(s, sep)
  error("not implemented")
end

-- Returns a new sequence of every value of `it`.
function iter.to_list(it)
  error("not implemented")
end

-- Returns a memoized version of the one-argument function `fn`.
function iter.memoize(fn)
  error("not implemented")
end

return iter

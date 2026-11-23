# %% [markdown]
# # Lab 11: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L11.1
#
# Every field the statement names, with the dependency on `textutil` that lets `luarocks make` find
# it in the project's tree. Common mistakes: leaving out `description.license`, which
# `luarocks lint` rejects; writing the version as `0.1` without the revision; and mapping the module
# to `wordfreq.lua`, without the `src/` folder, which fails at build time.

# %% tags=["answer-L11.1"]
# %%writefile scratch/project/wordfreq/wordfreq-0.1-1.rockspec
package = "wordfreq"
version = "0.1-1"
source = { url = "git+https://example.org/wordfreq.git" }
description = {
  summary = "Lists the most frequent words in a text.",
  license = "MIT",
}
dependencies = {
  "lua >= 5.4",
  "textutil >= 0.1",
}
build = {
  type = "builtin",
  modules = {
    wordfreq = "src/wordfreq.lua",
  },
}

# %% [markdown]
# ## Exercise L11.2
#
# Delete the unused `unused_limit` and the unused loop variable `i`; make `total` local; and assign
# to the outer `best` instead of declaring a new local inside the loop. That last finding,
# `shadowing definition of variable 'best'`, was the bug: the inner `best` vanished after each pass,
# so `max` returned the first item. Common mistakes: renaming `i` to `_i`, which also silences the
# warning but keeps a useless name; and adding `-- luacheck: ignore`, which the check rejects.

# %% tags=["answer-L11.2"]
# %%writefile scratch/project/stats/src/stats.lua
local stats = {}

function stats.mean(list)
  local total = 0
  for _, v in ipairs(list) do total = total + v end
  return total / #list
end

function stats.max(list)
  local best = list[1]
  for _, v in ipairs(list) do
    best = math.max(best, v)
  end
  return best
end

return stats

# %% [markdown]
# ## Exercise L11.3
#
# The class names the shape the functions share, and each function documents what it takes and
# returns. With `factor` declared a `number`, the checker rejects the string `"2"`; with `rect`
# declared a `Rect`, it rejects `12`. A common mistake is annotating `rect` as `table`, which `12`
# still fails but which documents much less.

# %% tags=["answer-L11.3"]
# %%writefile scratch/project/shapes/shapes.lua
local shapes = {}

---A rectangle, in any unit of length.
---@class Rect
---@field width number
---@field height number

---Makes a rectangle.
---@param width number
---@param height number
---@return Rect
function shapes.rect(width, height)
  return { width = width, height = height }
end

---Returns a rectangle's area.
---@param rect Rect
---@return number
function shapes.area(rect)
  return rect.width * rect.height
end

---Returns a new rectangle, scaled by a factor.
---@param rect Rect
---@param factor number
---@return Rect
function shapes.scale(rect, factor)
  return shapes.rect(rect.width * factor, rect.height * factor)
end

return shapes

# %% [markdown]
# ## Exercise L11.4
#
# One test per branch of `letter`, at each grade's lowest score, which also checks the boundaries;
# tests of the error for a number out of range and for a value that isn't a number; and a summary
# with every letter. A common mistake is a test that calls `grades.letter(101)` inside `pcall`
# without checking the result, which covers the line but checks nothing.

# %% tags=["answer-L11.4"]
# %%writefile scratch/project/grades/spec/grades_spec.lua
local grades = require("grades")

describe("grades.letter", function()
  it("gives each letter at its lowest score", function()
    assert.are.equal("A", grades.letter(90))
    assert.are.equal("B", grades.letter(80))
    assert.are.equal("C", grades.letter(70))
    assert.are.equal("F", grades.letter(69))
  end)

  it("raises an error for a score out of range", function()
    assert.has_error(function() grades.letter(101) end, "score must be a number from 0 to 100")
    assert.has_error(function() grades.letter("90") end, "score must be a number from 0 to 100")
  end)
end)

describe("grades.summary", function()
  it("counts nothing in an empty list", function()
    assert.are.same({ A = 0, B = 0, C = 0, F = 0 }, grades.summary({}))
  end)

  it("counts each letter", function()
    assert.are.same({ A = 1, B = 0, C = 2, F = 1 }, grades.summary({ 95, 72, 70, 10 }))
  end)
end)

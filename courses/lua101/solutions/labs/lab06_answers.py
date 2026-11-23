# %% [markdown]
# # Lab 6: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L6.1
#
# The four that return `nil` are failures the caller should expect: text that isn't a number
# (`tonumber`), a file that doesn't exist (`io.open`, `os.remove`), and bytes that aren't valid
# UTF-8 (`utf8.len`, which also returns the bad byte's position, 4). The four that raise errors are
# mistakes in the calling code: a string where a number is required (`math.floor`), a missing
# argument (`string.rep`), a float with no integer value for `%d`, and a module that doesn't
# exist, which `require` treats as a broken program rather than a question.
#
# The common mistake is `"nil"` for `require`, by analogy with `io.open`.

# %% tags=["answer-L6.1"]
# %%lua
failure_predictions = {
  { [[tonumber("12abc")]],            "nil" },
  { [[math.floor("12abc")]],          "error" },
  { [[io.open("no/such/file.txt")]],  "nil" },
  { [[string.rep("ab")]],             "error" },
  { [[utf8.len("caf\xe9")]],          "nil" },
  { [[string.format("%d", 2.5)]],     "error" },
  { [[os.remove("no/such/file.txt")]], "nil" },
  { [[require("no_such_module")]],    "error" },
}

# %% [markdown]
# ## Exercise L6.2
#
# `table.pack` keeps the results of `pcall` in order: `results[1]` says whether `fn` raised an
# error, and the rest are `fn`'s results. Common mistakes: `if not results[2]`, which treats a
# result of `false` as a failure; and `local ok, a, b = pcall(fn, ...)`, which works here but
# hides the rule that `classify` looks at only the first two results.

# %% tags=["answer-L6.2"]
# %%lua
function classify(fn, ...)
  local results = table.pack(pcall(fn, ...))
  if not results[1] then
    return "error", results[2]
  end
  if results[2] == nil then
    return "failure", results[3]
  end
  return "ok", results[2]
end

# %% [markdown]
# ## Exercise L6.3
#
# `parse_line` returns `nil` and a message, because a bad line in a data file is an expected
# outcome that `summary` handles by counting it. `mean` raises an error, because an empty list is a
# mistake in the calling code: `summary` itself checks for one before it calls `mean`. Level 2
# makes the message name the caller's line.
#
# Common mistakes: `error(…)` at level 1, which names the module's own line; leaving `values` or
# `bad` global; and calling a local copy of `parse_line` in `summary`, which works but means a fix
# to one doesn't reach the other. `tonumber(text)` without the `name and` guard also works,
# because `tonumber(nil)` returns `nil`; only `tonumber()` with no argument raises an error.

# %% tags=["answer-L6.3"]
# %%writefile scratch/readings.lua
-- readings.lua: parse sensor readings and summarize them.
local readings = {}

function readings.parse_line(line)
  local name, text = line:match("^([%w_]+)=(.+)$")
  local value = name and tonumber(text)
  if not value then
    return nil, "bad line: " .. line
  end
  return name, value
end

function readings.mean(values)
  if type(values) ~= "table" or #values == 0 then
    error("mean: expected a non-empty list", 2)
  end
  local total = 0
  for _, v in ipairs(values) do
    total = total + v
  end
  return total / #values
end

function readings.summary(text)
  local values, bad = {}, 0
  for line in text:gmatch("[^\n]+") do
    local name, value = readings.parse_line(line)
    if name then
      values[#values + 1] = value
    else
      bad = bad + 1
    end
  end
  local mean = nil
  if #values > 0 then
    mean = readings.mean(values)
  end
  return { count = #values, mean = mean, bad = bad }
end

return readings

# %% [markdown]
# ## Exercise L6.4
#
# Each test checks one promise from the statement. The four broken versions change, in turn, what
# `parse_line` returns for a bad line, whether `mean` raises an error for an empty list, the value
# `mean` returns, and the count `summary` returns. The tests below catch all four; a suite missing
# any one of the failure tests, or testing `summary` only on text without bad lines, misses one.

# %% tags=["answer-L6.4"]
# %%writefile scratch/readings_spec.lua
local readings = require("readings")

describe("readings.parse_line", function()
  it("reads a name and a value", function()
    local name, value = readings.parse_line("kitchen=21.5")
    assert.are.equal("kitchen", name)
    assert.are.equal(21.5, value)
  end)

  it("returns nil and a message for a value that isn't a number", function()
    local name, message = readings.parse_line("garage=cold")
    assert.is_nil(name)
    assert.are.equal("bad line: garage=cold", message)
  end)

  it("rejects a line without a name or without a value", function()
    assert.is_nil(readings.parse_line("=5"))
    assert.is_nil(readings.parse_line("x="))
  end)
end)

describe("readings.mean", function()
  it("averages a list", function()
    assert.are.equal(2.5, readings.mean({ 1, 2, 3, 4 }))
  end)

  it("raises an error for an empty list", function()
    assert.has_error(function() readings.mean({}) end, "mean: expected a non-empty list")
  end)

  it("raises an error for a value that isn't a table", function()
    assert.has_error(function() readings.mean("x") end, "mean: expected a non-empty list")
  end)
end)

describe("readings.summary", function()
  it("counts good and bad lines and averages the good ones", function()
    assert.are.same({ count = 2, mean = 2.0, bad = 1 }, readings.summary("a=1\nb=x\nc=3\n"))
  end)

  it("has no mean when no line is good", function()
    local s = readings.summary("a=x\n")
    assert.are.equal(0, s.count)
    assert.are.equal(1, s.bad)
    assert.is_nil(s.mean)
  end)

  it("handles empty text", function()
    assert.are.same({ count = 0, bad = 0 }, readings.summary(""))
  end)
end)

# %% [markdown]
# # Lab 1: answer key
#
# Each tagged cell replaces the lab cell with the same tag. `tools/check_lab.py` runs the lab with
# these answers and fails if any check fails. The untagged Markdown cells explain each answer and
# the mistakes students commonly make; the checker ignores them.

# %% [markdown]
# ## Exercise L1.1
#
# The message is `scratch/average.lua:13: attempt to perform arithmetic on a nil value (global
# 'totl')`. Line 13 misspells `total`, and the misspelled name is a global that was never
# assigned. The sum is 243, and 243 / 3 is the float `81.0`, because `/` always gives a float.
# Students sometimes "fix" the error by adding `totl = 0`, which makes the script print `0.0`
# without an error: the message names the symptom, and the cause is the misspelling.

# %% tags=["answer-L1.1"]
# %%writefile scratch/average.lua
-- average.lua: prints the average of three scores.
local total = 0
local count = 0

local function add(score)
  total = total + score
  count = count + 1
end

add(90)
add(72)
add(81)
print("average:", total / count)

# %% [markdown]
# ## Exercise L1.2
#
# The rules behind the predictions students most often get wrong:
#
# - `6 / 2` is `3.0`: `/` always gives a float.
# - `-7 // 2` is `-4` and `-7 % 3` is `2`: `//` rounds down, and `%` takes the divisor's sign.
# - `7 % -3` is `-2`, for the same reason.
# - `"10" + 5` is the integer `15`: arithmetic converts the string `"10"`, which looks like an
#   integer, to the integer 10.
# - `"10" == 10` is `false`: `==` never converts.
# - `10 // 0` is an error, but `10 / 0` is `math.huge` (infinity): only float division by zero
#   is defined.
# - `0 and "zero"` is `"zero"`: `0` is truthy.
# - `false and nil` is `false`: `and` returns its first operand when that operand is falsy.

# %% tags=["answer-L1.2"]
# %%lua
predictions = {
  { "7 // 2",                            3 },
  { "7 / 2",                             3.5 },
  { "6 / 2",                             3.0 },
  { "-7 // 2",                           -4 },
  { "-7 % 3",                            2 },
  { "7 % -3",                            -2 },
  { "2 ^ 3",                             8.0 },
  { "3 + 4.0",                           7.0 },
  { "\"10\" + 5",                        15 },
  { "\"10\" .. 5",                       "105" },
  { "\"10\" == 10",                      false },
  { "#\"hello\"",                        5 },
  { "10 // 0",                           "error" },
  { "10 / 0",                            math.huge },
  { "math.maxinteger + 1 == math.mininteger", true },
  { "nil or \"default\"",                "default" },
  { "0 and \"zero\"",                    "zero" },
  { "false and nil",                     false },
  { "not nil",                           true },
  { "1 == 1.0",                          true },
}

# %% [markdown]
# ## Exercise L1.3
#
# Adding `local` to `n = 0` makes the counter local to each call. A common wrong fix renames the
# global (`count = 0`), which moves the bug to another name instead of removing it.

# %% tags=["answer-L1.3"]
# %%lua
function count_words(text)
  local n = 0
  for _ in text:gmatch("%S+") do
    n = n + 1
  end
  return n
end

n = 100
print("words:", count_words("one two three"))
print("n:", n)

# %% [markdown] tags=["answer-L1.3-why"]
# The function's own result was right because it set `n` to 0, counted, and returned `n`
# before any other code could change it; the bug only overwrote the global that other code
# relied on.

# %% [markdown]
# ## Exercise L1.4
#
# An `if` statement tests `cond` alone, so the value of `a` can't change which branch runs. The
# answer `return cond and a or b` fails the last two checks, which is the point of the exercise.

# %% tags=["answer-L1.4"]
# %%lua
function choose(cond, a, b)
  if cond then
    return a
  end
  return b
end

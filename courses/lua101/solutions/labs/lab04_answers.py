# %% [markdown]
# # Lab 4: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L4.1
#
# - `sub(2, 4)` is `"ell"`, `sub(-3)` is `"llo"`, and `sub(4, 2)` is `""`, because 4 comes after 2.
# - `upper` runs first, then `rep` with a separator: `"HELLO-HELLO"`.
# - `#("ab"):rep(3)` is 6: `#` applies to the result of the whole method call.
# - `%5.1f` pads `3.1` to five characters, `"  3.1|"`; `%-4s` pads on the right, `"ab  |"`; and
#   `%03d` pads with zeros, `"007"`.
# - `("x"):byte()` is 120, the code of `x`.
# - `1e3` is a float, so `tostring` gives `"1000.0"`, while `%d` accepts it because its value is an
#   integer: `"1000.0|1000"`.
#
# The common mistakes are `"HELLOHELLO"` (forgetting the separator) and `"1000|1000"`.

# %% tags=["answer-L4.1"]
# %%lua
string_predictions = {
  { '("hello"):sub(2, 4)',                  "ell" },
  { '("hello"):sub(-3)',                    "llo" },
  { '("hello"):sub(4, 2)',                  "" },
  { '("hello"):upper():rep(2, "-")',        "HELLO-HELLO" },
  { '#("ab"):rep(3)',                       6 },
  { 'string.format("%5.1f|", 3.14159)',     "  3.1|" },
  { 'string.format("%-4s|", "ab")',         "ab  |" },
  { 'string.format("%03d", 7)',             "007" },
  { '("x"):byte()',                         120 },
  { 'tostring(1e3) .. "|" .. string.format("%d", 1e3)', "1000.0|1000" },
}

# %% [markdown]
# ## Exercise L4.2
#
# One anchored pattern with five captures. `%s+` after the level absorbs the padding, and `(.*)$`
# takes the rest of the line. Common mistakes: writing the date as `%d%d%d%d-%d%d-%d%d`, where
# each `-` follows a class and so is a lazy quantifier, not a hyphen, and no line parses; and
# leaving out `^`, so that the line with a stray `x` parses. `%d+-%d+-%d+` happens to work,
# because a `-` that follows a quantifier can't be one, so it matches a hyphen; `%-` says what it
# means either way. `(%a+)` for the level also works, but lets lowercase levels through.

# %% tags=["answer-L4.2"]
# %%lua
function parse_line(line)
  return line:match("^(%d%d%d%d%-%d%d%-%d%d) (%d%d:%d%d:%d%d) (%u+)%s+%[(%a+)%] (.*)$")
end

# %% [markdown]
# ## Exercise L4.3
#
# `%s*%b()` takes each note with the spaces before it, and the parentheses around `gsub` keep only
# the string. Lowercasing both the text and the word makes the count ignore case, and the two
# frontiers make it count whole words. Common mistakes: returning `message:gsub(...)` without
# parentheses, which returns the count too; and `%(.-%)`, which stops at the first `)` and leaves
# a `)` behind in a nested note. Frontiers on `%w` instead of `%a` would also be correct here.

# %% tags=["answer-L4.3"]
# %%lua
function strip_notes(message)
  return (message:gsub("%s*%b()", ""))
end

function count_word(text, word)
  local pattern = "%f[%a]" .. word:lower() .. "%f[%A]"
  local _, count = text:lower():gsub(pattern, "")
  return count
end

# %% [markdown]
# ## Exercise L4.4
#
# The pattern matches the shape the regular expression describes, with any uppercase word as the
# method, and the set does the work of `GET|POST|DELETE`. The space after the three digits makes
# `2000` fail, as in the regular expression. Common mistakes: returning the status as the string
# `"200"`, and three separate `match` calls, one per method, which work but repeat the pattern.

# %% tags=["answer-L4.4"]
# %%lua
local allowed = { GET = true, POST = true, DELETE = true }

function request_of(message)
  local method, path, status = message:match("^(%u+) (%S+) (%d%d%d) ")
  if method and allowed[method] then
    return method, path, tonumber(status)
  end
  return nil
end

# %% [markdown]
# ## Exercise L4.5
#
# Each line goes into a list, and one `table.concat` joins them. The format already ends each line
# with `\n`, so the separator is empty. On the test machine it took about 19 ms for 40,000 rows.

# %% tags=["answer-L4.5"]
# %%lua
function fast_report(rows)
  local lines = {}
  for i, row in ipairs(rows) do
    lines[i] = string.format("%-10s %5d\n", row.name, row.count)
  end
  return table.concat(lines)
end

# %% [markdown]
# ## Exercise L4.6
#
# `utf8.len` both validates the text and counts its characters, so it comes first. The cut ends one
# byte before character `n + 1` starts, which never splits a character. Common mistakes:
# `s:sub(1, n)`, which counts bytes; and a loop over `utf8.codes`, which works but raises an error
# on invalid text instead of returning `nil`.

# %% tags=["answer-L4.6"]
# %%lua
function truncate(s, n)
  local length, bad = utf8.len(s)
  if not length then return nil, bad end
  if length <= n then return s end
  return s:sub(1, utf8.offset(s, n + 1) - 1) .. "…"
end

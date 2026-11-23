# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: tags,-all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lab 4: Strings and patterns
#
# **Objectives:** LO-4.1, LO-4.2, LO-4.3, LO-4.4\
# **Prerequisites:** the [Module 4 reading](index.md) and [Lab 3](../03-tables/lab03.ipynb)\
# **Time:** about 2 hours
#
# You will predict what string functions return, parse a server log with patterns, remove notes
# and count words with `%b` and `%f`, turn a regular expression with alternation into Lua, measure
# string building with `..` against `table.concat`, and shorten UTF-8 text without breaking a
# character. As in the earlier labs, each exercise ends with a check cell that prints `passed` or
# fails with a message, and the checks fail until you finish their exercise.

# %% [markdown]
# ## Setup
#
# Nothing in this lab is random. Section 4 measures time, so its numbers depend on your machine.
# The second cell prints the Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. The string library
#
# ### Exercise L4.1 (LO-4.1, ★, about 15 minutes)
#
# Predict the value of each expression, and replace its `"?"`: a string in quotes, such as
# `"ell"`, or a number. Make all ten predictions before you run the check.

# %% tags=["answer-L4.1"] language="lua"
# string_predictions = {
#   { '("hello"):sub(2, 4)',                  "?" },
#   { '("hello"):sub(-3)',                    "?" },
#   { '("hello"):sub(4, 2)',                  "?" },
#   { '("hello"):upper():rep(2, "-")',        "?" },
#   { '#("ab"):rep(3)',                       "?" },
#   { 'string.format("%5.1f|", 3.14159)',     "?" },
#   { 'string.format("%-4s|", "ab")',         "?" },
#   { 'string.format("%03d", 7)',             "?" },
#   { '("x"):byte()',                         "?" },
#   { 'tostring(1e3) .. "|" .. string.format("%d", 1e3)', "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local function show(v)    -- strings in quotes, so that spaces at their ends are visible
#   if type(v) == "string" then return string.format("%q", v) end
#   return tostring(v)
# end
#
# local wrong, unanswered = 0, 0
# for n, row in ipairs(string_predictions) do
#   local expression, predicted = row[1], row[2]
#   local actual = load("return " .. expression, "=expression", "t")()
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%2d  %-50s you: %-14s Lua: %-14s %s", n, expression,
#     show(predicted), show(actual), verdict))
# end
# assert(unanswered == 0, unanswered .. " expressions still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ## 2. Parsing a log
#
# The next cell stores a server's log in the global `log`, as a long string. Each line has a date,
# a time, a level padded to five characters, a component in brackets, and a message. One line was
# cut short by a crash.

# %% language="lua"
# log = [[
# 2026-11-02 08:15:02 INFO  [web] GET /index.html 200 5120
# 2026-11-02 08:15:07 WARN  [db] slow query (users, 1532 ms)
# 2026-11-02 08:15:09 INFO  [web] POST /api/login 200 312
# 2026-11-02 08:16:44 ERROR [web] GET /api/users 500 0
# 2026-11-02 08:17:01 INFO  [auth] user ada logged in
# 2026-11-02 08:17:30 INFO  [web] GET /style.css 304 0
# 2026-11-02 08:18:12 ERROR [db] connection lost (retry 1 of 3)
# 2026-11-02 08:18:13 INFO  [db] reconnected
# 2026-11-02 08:19:55 INFO  [web] DELETE /api/session 204 0
# 2026-11-02 08:20:03 WARN  [web] PUT /api/users/7 403 87
# this line was cut off by a cra
# 2026-11-02 08:21:40 INFO  [web] GET /index.html 200 5120
# ]]
#
# local count = 0
# for line in log:gmatch("[^\n]+") do count = count + 1 end
# print(count, "lines")

# %% [markdown]
# `[^\n]+` matches a run of characters that aren't newlines, so `gmatch` with it visits each line.
# Try a pattern of your own in the next cell before the exercise: change it to find every time of
# day in the log, then every component in brackets.

# %% language="lua"
# for match in log:gmatch("%d%d%d%d%-%d%d%-%d%d") do io.write(match, "  ") end
# print()

# %% [markdown]
# ### Exercise L4.2 (LO-4.2, ★★, about 25 minutes)
#
# Write `parse_line(line)`, which returns five strings for a log line: the date, the time, the
# level, the component without its brackets, and the message. For a line that doesn't have that
# shape, it returns `nil`. Use one call to `match` with one pattern.
#
# <details>
# <summary>Hint 1</summary>
#
# `-`, `[`, and `]` are magic characters, so the pattern writes them as `%-`, `%[`, and `%]`.
# </details>
#
# <details>
# <summary>Hint 2</summary>
#
# The level is followed by one space or two, which `%s+` matches. Anchor the pattern with `^` and
# `$`, and capture the message with `(.*)`.
# </details>

# %% tags=["answer-L4.2"] language="lua"
# function parse_line(line)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local date, time, level, component, message =
#   parse_line("2026-11-02 08:15:07 WARN  [db] slow query (users, 1532 ms)")
# assert(date == "2026-11-02" and time == "08:15:07", "the date and time come first")
# assert(level == "WARN", "the level should be \"WARN\", without the padding")
# assert(component == "db", "the component should be \"db\", without the brackets")
# assert(message == "slow query (users, 1532 ms)", "the message is the rest of the line")
# assert(select(4, parse_line("2026-11-02 08:16:44 ERROR [web] GET /api/users 500 0")) == "web",
#   "a five-letter level is followed by one space")
# assert(parse_line("this line was cut off by a cra") == nil, "a malformed line gives nil")
# assert(parse_line("2026-11-02 08:15:02 INFO  web GET / 200 1") == nil, "the brackets are required")
# assert(parse_line("x2026-11-02 08:15:02 INFO  [web] GET / 200 1") == nil, "anchor the start")
# local parsed = 0
# for line in log:gmatch("[^\n]+") do
#   if parse_line(line) then parsed = parsed + 1 end
# end
# assert(parsed == 11, "11 of the log's 12 lines should parse, not " .. parsed)
# print("passed")

# %% [markdown]
# ### Exercise L4.3 (LO-4.2, ★★, about 20 minutes)
#
# Write two functions:
#
# - `strip_notes(message)` removes every note in parentheses, together with the spaces before it,
#   and returns only the new string. `strip_notes("slow query (users, 1532 ms)")` is
#   `"slow query"`, and notes inside notes go with the note around them.
# - `count_word(text, word)` returns how many times `word` appears in `text` as a whole word,
#   ignoring case. Assume `word` holds only ASCII letters. `count_word("Error: error-prone
#   errors", "error")` is 2: `errors` is a different word.
#
# <details>
# <summary>Hint</summary>
#
# `%b()` matches a note with any notes nested inside it. For whole words, put frontiers around the
# word, and compare lowercase text with a lowercase word. `gsub` returns the number of matches as
# its second value.
# </details>

# %% tags=["answer-L4.3"] language="lua"
# function strip_notes(message)
#   -- your code here
# end
#
# function count_word(text, word)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# assert(strip_notes("slow query (users, 1532 ms)") == "slow query", "remove the note and its space")
# assert(strip_notes("connection lost (retry 1 of 3)") == "connection lost", "remove every note")
# assert(strip_notes("a (b (c)) d (e)") == "a d", "a nested note goes with the note around it")
# assert(strip_notes("no notes here") == "no notes here", "text without notes is unchanged")
# assert(select("#", strip_notes("x (y)")) == 1, "strip_notes should return one value, not two")
# assert(count_word("Error: error-prone errors; ERROR.", "error") == 3, "Error, error-, and ERROR")
# assert(count_word("the cat concatenates cats", "cat") == 1, "only the whole word counts")
# assert(count_word("Cat", "CAT") == 1, "ignore case in the word too")
# assert(count_word("", "cat") == 0, "no text, no words")
# assert(math.type(count_word("cat", "cat")) == "integer", "return the count as an integer")
# print("passed")

# %% [markdown]
# ## 3. When a pattern needs alternation
#
# A colleague's Python script finds web requests in the log's messages with this regular
# expression, which captures the method, the path, and the status code:
#
# ```text
# ^(GET|POST|DELETE) (\S+) (\d{3})
# ```
#
# It matches only the methods `GET`, `POST`, and `DELETE`, followed by a space, a path, a space,
# exactly three digits, and a space. Lua patterns have no `|` and no `{3}`.
#
# ### Exercise L4.4 (LO-4.3, ★★, about 20 minutes)
#
# Write `request_of(message)`, which returns the method, the path, and the status as an integer
# for every message the regular expression matches, and `nil` for every other message.
#
# <details>
# <summary>Hint</summary>
#
# Match the general shape, with the method captured as `(%u+)`, and write `\d{3}` as three `%d`s.
# Then test the method against a set of the three allowed methods.
# </details>

# %% tags=["answer-L4.4"] language="lua"
# function request_of(message)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local method, path, status = request_of("GET /index.html 200 5120")
# assert(method == "GET" and path == "/index.html", "GET /index.html should give GET and the path")
# assert(status == 200 and math.type(status) == "integer", "the status should be the integer 200")
# assert(select(3, request_of("DELETE /api/session 204 0")) == 204, "DELETE is allowed")
# assert(request_of("POST /api/login 200 312") == "POST", "POST is allowed")
# assert(request_of("PUT /api/users/7 403 87") == nil, "PUT isn't one of the three methods")
# assert(request_of("GETS /x 200 1") == nil, "GETS isn't GET")
# assert(request_of("get /x 200 1") == nil, "the methods are uppercase")
# assert(request_of("GET /x 20 1") == nil, "the status has exactly three digits, not two")
# assert(request_of("GET /x 2000 1") == nil, "...and not four")
# assert(request_of("user ada logged in") == nil, "a message that isn't a request gives nil")
# print("passed")

# %% [markdown]
# With `parse_line` and `request_of` done, this cell counts the requests in the log by status
# code. It is the whole log analysis in a few lines. It runs only once both exercises pass.

# %% tags=["raises-exception"] language="lua"
# local by_status = {}
# for line in log:gmatch("[^\n]+") do
#   local _, _, _, _, message = parse_line(line)
#   local _, _, status = request_of(message or "")
#   if status then by_status[status] = (by_status[status] or 0) + 1 end
# end
# local codes = {}
# for code in pairs(by_status) do codes[#codes + 1] = code end
# table.sort(codes)
# assert(#codes > 0, "no requests found: finish Exercises L4.2 and L4.4 first")
# for _, code in ipairs(codes) do print(code, by_status[code]) end

# %% [markdown]
# ## 4. Building long strings
#
# `slow_report` builds a text report by appending each line with `..`. The cell after it times the
# function on 2,500 to 20,000 rows, and prints how many times longer each row of the table took
# than the row above. Predict that ratio before you run it, from the reading. The timing cell takes
# about a second.

# %% language="lua"
# function make_rows(n)
#   local rows = {}
#   for i = 1, n do rows[i] = { name = "item" .. i, count = i % 97 } end
#   return rows
# end
#
# function slow_report(rows)
#   local s = ""
#   for _, row in ipairs(rows) do
#     s = s .. string.format("%-10s %5d\n", row.name, row.count)
#   end
#   return s
# end
#
# io.write(slow_report(make_rows(3)))

# %% language="lua"
# print("     n     bytes   seconds   ratio")
# local previous
# for _, n in ipairs({ 2500, 5000, 10000, 20000 }) do
#   local rows = make_rows(n)
#   local start = os.clock()
#   local report = slow_report(rows)
#   local seconds = os.clock() - start
#   local ratio = previous and string.format("%.1f", seconds / previous) or ""
#   print(string.format("%6d   %7d   %7.4f   %s", n, #report, seconds, ratio))
#   previous = seconds
# end

# %% [markdown]
# ### Exercise L4.5 (LO-4.4, ★, about 15 minutes)
#
# Write `fast_report(rows)`, which returns exactly the same string as `slow_report(rows)` but builds
# it with `table.concat`. The check compares the two on 1,000 rows, then times `fast_report` on
# 40,000 rows, which took `slow_report` about 3 seconds when this lab was tested.

# %% tags=["answer-L4.5"] language="lua"
# function fast_report(rows)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local rows = make_rows(1000)
# assert(fast_report(rows) == slow_report(rows), "fast_report must return the same string as slow_report")
# assert(fast_report({}) == "", "no rows give the empty string")
# local big = make_rows(40000)
# local start = os.clock()
# local report = fast_report(big)
# local seconds = os.clock() - start
# print(string.format("fast_report on 40,000 rows: %.4f s, %d bytes", seconds, #report))
# assert(#report == 680000, "the report on 40,000 rows should be 680,000 bytes")
# assert(seconds < 0.25, "fast_report took 0.25 s or more: does it still use .. in a loop?")
# print("passed")

# %% [markdown]
# ## 5. UTF-8 text
#
# Run the next cell, and compare each result with the reading's section on UTF-8. Then change
# `word` to a word of your own with accented letters, or to an emoji, and run it again.

# %% language="lua"
# local word = "naïve café"
# print("bytes:", #word, "characters:", utf8.len(word))
# print("upper:", word:upper())
# print("%a+ finds:", word:match("%a+"))
# print("reversed bytes are valid UTF-8:", utf8.len(word:reverse()) ~= nil)
# for position, code in utf8.codes(word) do
#   io.write(position, ":", utf8.char(code), " ")
# end
# print()

# %% [markdown]
# ### Exercise L4.6 (LO-4.4, ★★, about 20 minutes)
#
# Write `truncate(s, n)`, which shortens UTF-8 text for a preview. If `s` has at most `n`
# characters, it returns `s`. Otherwise it returns the first `n` characters followed by `"…"`
# (one character, U+2026). If `s` isn't valid UTF-8, it returns `nil` and the position of the first
# invalid byte, as `utf8.len` does. It must never cut a character in half.
#
# <details>
# <summary>Hint</summary>
#
# `utf8.offset(s, n + 1)` is the byte where character `n + 1` starts, so the first `n` characters
# end one byte before it.
# </details>

# %% tags=["answer-L4.6"] language="lua"
# function truncate(s, n)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# assert(truncate("héllo wörld", 5) == "héllo…", "keep five characters, then add …")
# assert(truncate("héllo", 5) == "héllo", "text that fits is returned as it is")
# assert(truncate("€€€", 1) == "€…", "one three-byte character, then …")
# assert(truncate("abc", 0) == "…", "zero characters leave only …")
# assert(truncate("", 3) == "", "the empty string fits")
# local result, position = truncate("ab\xffcd", 2)
# assert(result == nil and position == 3, "invalid UTF-8 gives nil and the bad byte's position")
# assert(utf8.len(truncate("naïve café", 3)) == 4, "three characters and … make four")
# print("passed")

# %% [markdown]
# ## Summary
#
# - The string functions return new strings, count positions from 1 or, when negative, from the
#   end, and can be called as methods.
# - One anchored pattern with captures parses a line of a log into its fields, and `nil` from
#   `match` flags the lines that don't fit.
# - `%b()` handles nested parentheses, and `%f` finds whole words, which regular expressions do
#   with other tools.
# - A regular expression with alternation becomes a pattern for the general shape plus a test
#   against a set.
# - `..` in a loop grew about four times slower each time the input doubled; `table.concat`
#   doesn't.
# - `#`, `upper`, `reverse`, and `%a` work on bytes and ASCII; `utf8.len`, `utf8.codes`, and
#   `utf8.offset` work on characters.
#
# Next, do the [Module 4 practice](practice.md), then start PA2.

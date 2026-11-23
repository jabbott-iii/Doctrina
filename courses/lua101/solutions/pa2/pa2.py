# ---
# jupyter:
#   jupytext:
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
# # PA2: Tables and text
#
# **Objectives:** LO-2.2, LO-3.1, LO-3.2, LO-3.3, LO-3.4, LO-4.1, LO-4.2, LO-4.4\
# **Due:** week 5, as the [schedule](../../README.md#schedule) gives it\
# **Weight:** 5% of the course grade; 22 points\
# **Time:** about 3 hours
#
# Write each answer in the cell marked `-- YOUR CODE HERE`, replacing the line
# `error("not implemented")`. Each problem's test cell checks your answer with visible tests,
# which you can run as often as you like. When you submit, the grader also runs hidden tests,
# which check the cases the problem statement describes but the visible tests don't. A problem's
# points go to the hidden and visible tests together, so read each statement closely. Where a
# statement says how fast a function must be, the hidden tests time it on a large input.
#
# - Don't change or delete the test cells.
# - Define each function as a global, as each problem's starter code does, so the test cells can
#   call it. Helper functions you add may be local.
# - Before you submit, restart the kernel and run every cell from the top (**Kernel** > **Restart
#   Kernel and Run All Cells**), and check that every test cell prints `passed`.
# - The course policies apply. In particular, generative AI tools may not write any part of this
#   assignment; say in the last cell which tools you used, and how, or write "none".

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% [markdown]
# ## Problem 1: Word frequencies (LO-3.1, LO-4.2, 4 points)
#
# In this problem, a **word** is a run of one or more ASCII letters, so `"It's"` holds the two
# words `it` and `s`. Words are compared in lowercase.
#
# - `word_counts(text)` returns a table that maps each word in `text`, in lowercase, to the number
#   of times it appears. `word_counts("The cat saw the dog")` is
#   `{ the = 2, cat = 1, saw = 1, dog = 1 }`.
# - `top_words(counts, k)` takes such a table and returns a sequence of the `k` most frequent
#   words, as records `{ word = …, count = … }`, from the most frequent to the least. Words with
#   the same count come in alphabetical order. If there are fewer than `k` words, it returns them
#   all. It must not change `counts`.

# %% nbgrader={"grade": false, "grade_id": "word-counts", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function word_counts(text)
#   -- BEGIN SOLUTION
#   local counts = {}
#   for word in text:lower():gmatch("%a+") do
#     counts[word] = (counts[word] or 0) + 1
#   end
#   return counts
#   -- END SOLUTION
# end
#
# function top_words(counts, k)
#   -- BEGIN SOLUTION
#   local list = {}
#   for word, count in pairs(counts) do
#     list[#list + 1] = { word = word, count = count }
#   end
#   table.sort(list, function(a, b)
#     if a.count ~= b.count then return a.count > b.count end
#     return a.word < b.word
#   end)
#   for i = #list, k + 1, -1 do
#     list[i] = nil
#   end
#   return list
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "word-counts-tests", "locked": true, "points": 4, "schema_version": 3, "solution": false, "task": false} language="lua"
# local counts = word_counts("The cat saw the dog")
# assert(counts.the == 2 and counts.cat == 1 and counts.dog == 1, "count each word in lowercase")
# assert(counts.The == nil, "words are stored in lowercase")
# local top = top_words(counts, 2)
# assert(#top == 2, "top_words(counts, 2) should return two records")
# assert(top[1].word == "the" and top[1].count == 2, "the most frequent word comes first")
# assert(top[2].word == "cat" and top[2].count == 1, "ties come in alphabetical order")
# -- BEGIN HIDDEN TESTS
# local c2 = word_counts("It's the END; the end.")
# assert(c2.it == 1 and c2.s == 1 and c2["end"] == 2 and c2.the == 2,
#   "punctuation separates words, and case doesn't matter")
# local n = 0
# for _ in pairs(c2) do n = n + 1 end
# assert(n == 4, "\"It's the END; the end.\" has four different words")
# assert(next(word_counts("")) == nil and next(word_counts("123 !?")) == nil,
#   "text without letters has no words")
# local t2 = top_words({ b = 2, a = 2, c = 1, d = 3 }, 3)
# assert(#t2 == 3 and t2[1].word == "d" and t2[2].word == "a" and t2[3].word == "b",
#   "top_words should sort by count, then alphabetically")
# assert(#top_words({ x = 1, y = 1 }, 10) == 2, "with fewer than k words, return them all")
# assert(#top_words({ x = 1 }, 0) == 0, "k = 0 gives an empty list")
# local original = { one = 1, two = 2 }
# top_words(original, 1)
# assert(original.one == 1 and original.two == 2, "top_words must not change its argument")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 2: A set type (LO-3.4, LO-3.2, LO-2.2, 5 points)
#
# Write a set type as seven global functions. A set's members can be any values except `nil` and
# NaN, `false` included. Choose the set's representation yourself.
#
# - `set_new(...)` returns a new set whose members are the arguments. Arguments that are `nil` are
#   skipped, wherever they appear: `set_new(1, nil, 2)` has the two members 1 and 2.
# - `set_add(s, v)` makes `v` a member of `s`, and `set_remove(s, v)` makes it not a member.
#   Adding a member twice, or removing a value that isn't a member, changes nothing, and so does
#   adding or removing `nil`.
# - `set_has(s, v)` returns `true` if `v` is a member of `s`, and `false` otherwise.
# - `set_size(s)` returns the number of members. It must take constant time, whatever the size of
#   the set.
# - `set_union(a, b)` and `set_intersection(a, b)` return new sets, and change neither argument.
# - `set_to_list(s)` returns the members as a sequence in increasing order. You may assume that
#   all the members are numbers, or all are strings.

# %% nbgrader={"grade": false, "grade_id": "set", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function set_new(...)
#   -- BEGIN SOLUTION
#   local s = { items = {}, size = 0 }
#   for i = 1, select("#", ...) do
#     set_add(s, (select(i, ...)))
#   end
#   return s
#   -- END SOLUTION
# end
#
# function set_add(s, v)
#   -- BEGIN SOLUTION
#   if v ~= nil and not s.items[v] then
#     s.items[v] = true
#     s.size = s.size + 1
#   end
#   -- END SOLUTION
# end
#
# function set_remove(s, v)
#   -- BEGIN SOLUTION
#   if v ~= nil and s.items[v] then
#     s.items[v] = nil
#     s.size = s.size - 1
#   end
#   -- END SOLUTION
# end
#
# function set_has(s, v)
#   -- BEGIN SOLUTION
#   return v ~= nil and s.items[v] == true
#   -- END SOLUTION
# end
#
# function set_size(s)
#   -- BEGIN SOLUTION
#   return s.size
#   -- END SOLUTION
# end
#
# function set_union(a, b)
#   -- BEGIN SOLUTION
#   local result = set_new()
#   for v in pairs(a.items) do set_add(result, v) end
#   for v in pairs(b.items) do set_add(result, v) end
#   return result
#   -- END SOLUTION
# end
#
# function set_intersection(a, b)
#   -- BEGIN SOLUTION
#   if set_size(a) > set_size(b) then a, b = b, a end   -- walk the smaller set
#   local result = set_new()
#   for v in pairs(a.items) do
#     if b.items[v] then set_add(result, v) end
#   end
#   return result
#   -- END SOLUTION
# end
#
# function set_to_list(s)
#   -- BEGIN SOLUTION
#   local list = {}
#   for v in pairs(s.items) do list[#list + 1] = v end
#   table.sort(list)
#   return list
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "set-tests", "locked": true, "points": 5, "schema_version": 3, "solution": false, "task": false} language="lua"
# local s = set_new(3, 1, 2)
# assert(set_size(s) == 3 and set_has(s, 2) and not set_has(s, 4), "set_new(3, 1, 2) has 1, 2, 3")
# assert(set_has(s, 4) == false, "set_has should return false, not nil, for a non-member")
# set_add(s, 4)
# set_remove(s, 1)
# assert(table.concat(set_to_list(s), ",") == "2,3,4", "after adding 4 and removing 1: 2, 3, 4")
# local u = set_union(set_new(1, 2), set_new(2, 3))
# assert(table.concat(set_to_list(u), ",") == "1,2,3", "the union of {1, 2} and {2, 3} is {1, 2, 3}")
# local i = set_intersection(set_new(1, 2), set_new(2, 3))
# assert(table.concat(set_to_list(i), ",") == "2", "the intersection of {1, 2} and {2, 3} is {2}")
# -- BEGIN HIDDEN TESTS
# local d = set_new("a", "a", "b")
# assert(set_size(d) == 2, "a repeated argument is one member")
# set_add(d, "a")
# set_remove(d, "zzz")
# set_add(d, nil)
# set_remove(d, nil)
# assert(set_size(d) == 2, "adding a member again, or removing a non-member or nil, changes nothing")
# local holes = set_new(nil, 1, nil, 2, nil)
# assert(set_size(holes) == 2 and set_has(holes, 2), "nil arguments are skipped, even at the ends")
# assert(set_size(set_new()) == 0 and #set_to_list(set_new()) == 0, "set_new() is empty")
# local f = set_new(false)
# assert(set_size(f) == 1 and set_has(f, false) == true, "false can be a member")
# set_remove(f, false)
# assert(set_size(f) == 0 and set_has(f, false) == false, "...and can be removed")
# assert(set_has(set_new(1), nil) == false, "nil is never a member")
# local a, b = set_new(1, 2, 3), set_new(3, 4)
# local u2 = set_union(a, b)
# local i2 = set_intersection(a, b)
# assert(set_size(u2) == 4 and set_size(i2) == 1 and set_has(i2, 3), "union and intersection")
# assert(table.concat(set_to_list(a), ",") == "1,2,3" and set_size(b) == 2,
#   "union and intersection must not change their arguments")
# set_add(u2, 99)
# assert(not set_has(a, 99) and not set_has(b, 99), "the union must be a new set")
# assert(set_size(set_intersection(set_new(1), set_new(2))) == 0, "disjoint sets: empty intersection")
# local words = set_to_list(set_new("pear", "fig", "apple"))
# assert(table.concat(words, ",") == "apple,fig,pear", "set_to_list sorts strings too")
# local big = set_new()
# for k = 1, 20000 do set_add(big, k) end
# for k = 1, 20000, 2 do set_remove(big, k) end
# assert(set_size(big) == 10000, "20,000 adds and 10,000 removes leave 10,000 members")
# local start = os.clock()
# for _ = 1, 2000 do set_size(big) end
# assert(os.clock() - start < 0.1, "set_size must take constant time: keep a count of the members")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 3: Run-length encoding (LO-4.1, LO-4.2, LO-4.4, 4 points)
#
# **Run-length encoding** replaces each run of a repeated character with its length and the
# character. Assume the text holds only ASCII characters, and no digits.
#
# - `rle_encode(s)` returns the encoding of `s`: `rle_encode("aaabcc")` is `"3a1b2c"`, and
#   `rle_encode("")` is `""`. It must take time in proportion to the length of `s`, so build the
#   result with `table.concat`.
# - `rle_decode(code)` reverses it: `rle_decode("3a1b2c")` is `"aaabcc"`, and
#   `rle_decode("12x")` is twelve `x`s. If `code` isn't a sequence of runs, each a count of 1 or
#   more followed by one character that isn't a digit, it returns `nil`. So `"3"`, `"a3"`, and
#   `"0a"` all give `nil`.
#
# Lua patterns can't repeat a group, so `(%d+%D)*` isn't a pattern. Find another way to check
# that a code is made only of runs.

# %% nbgrader={"grade": false, "grade_id": "rle", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function rle_encode(s)
#   -- BEGIN SOLUTION
#   local parts = {}
#   local i = 1
#   while i <= #s do
#     local c = s:sub(i, i)
#     local j = i
#     while s:sub(j + 1, j + 1) == c do
#       j = j + 1
#     end
#     parts[#parts + 1] = (j - i + 1) .. c
#     i = j + 1
#   end
#   return table.concat(parts)
#   -- END SOLUTION
# end
#
# function rle_decode(code)
#   -- BEGIN SOLUTION
#   if code:gsub("%d+%D", "") ~= "" then
#     return nil
#   end
#   local parts = {}
#   for count, c in code:gmatch("(%d+)(%D)") do
#     local n = tonumber(count)
#     if n == 0 then
#       return nil
#     end
#     parts[#parts + 1] = c:rep(n)
#   end
#   return table.concat(parts)
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "rle-tests", "locked": true, "points": 4, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(rle_encode("aaabcc") == "3a1b2c", "rle_encode(\"aaabcc\") should be \"3a1b2c\"")
# assert(rle_encode("") == "", "the empty string encodes to the empty string")
# assert(rle_decode("3a1b2c") == "aaabcc", "rle_decode(\"3a1b2c\") should be \"aaabcc\"")
# assert(rle_decode("12x") == ("x"):rep(12), "counts can have more than one digit")
# assert(rle_decode("a3") == nil, "a code must start with a count")
# -- BEGIN HIDDEN TESTS
# assert(rle_encode("abc") == "1a1b1c", "every run gets a count, even a run of one")
# assert(rle_encode(("z"):rep(15)) == "15z", "a long run gets a long count")
# assert(rle_encode("  ..") == "2 2.", "spaces and punctuation are characters too")
# assert(rle_decode("") == "", "the empty code decodes to the empty string")
# assert(rle_decode("3") == nil, "a count without a character is malformed")
# assert(rle_decode("3a2") == nil, "a trailing count is malformed")
# assert(rle_decode("0a") == nil, "a count of 0 is malformed")
# assert(rle_decode("2 2.") == "  ..", "decoding spaces and punctuation")
# assert(select("#", rle_decode("1a")) == 1, "rle_decode should return one value")
# for _, text in ipairs({ "a", "aab", "hello, world", "mississippi" }) do
#   assert(rle_decode(rle_encode(text)) == text, "decoding the encoding should give back " .. text)
# end
# local long = ("ab"):rep(100000)
# local start = os.clock()
# local code = rle_encode(long)
# local seconds = os.clock() - start
# assert(#code == 400000 and code:sub(1, 6) == "1a1b1a", "encoding 200,000 runs")
# assert(seconds < 0.5, string.format("rle_encode took %.2f s on 200,000 runs: use table.concat", seconds))
# assert(rle_decode(code) == long, "decoding 200,000 runs")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 4: Reversing UTF-8 text (LO-4.4, 3 points)
#
# `s:reverse()` reverses bytes, which breaks every character longer than one byte. Write
# `utf8_reverse(s)`, which reverses the characters of the UTF-8 string `s`:
# `utf8_reverse("héllo")` is `"olléh"`. If `s` isn't valid UTF-8, it returns `nil` and the
# position of the first invalid byte, as `utf8.len` does. It must take time in proportion to the
# length of `s`.

# %% nbgrader={"grade": false, "grade_id": "utf8-reverse", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function utf8_reverse(s)
#   -- BEGIN SOLUTION
#   local length, bad = utf8.len(s)
#   if not length then
#     return nil, bad
#   end
#   local reversed = {}
#   local i = length
#   for char in s:gmatch(utf8.charpattern) do
#     reversed[i] = char
#     i = i - 1
#   end
#   return table.concat(reversed)
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "utf8-reverse-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(utf8_reverse("héllo") == "olléh", "utf8_reverse(\"héllo\") should be \"olléh\"")
# assert(utf8_reverse("abc") == "cba", "ASCII text reverses as usual")
# assert(utf8_reverse("") == "", "the empty string reverses to itself")
# -- BEGIN HIDDEN TESTS
# assert(utf8_reverse("a€b") == "b€a", "a three-byte character stays whole")
# assert(utf8_reverse("x\u{1F600}y") == "y\u{1F600}x", "a four-byte character stays whole")
# assert(utf8_reverse("é") == "é", "one character reverses to itself")
# local result, position = utf8_reverse("ab\xffc")
# assert(result == nil and position == 3, "invalid UTF-8 gives nil and the position of the bad byte")
# local text = ("é€x"):rep(20000)
# local start = os.clock()
# local back = utf8_reverse(text)
# assert(os.clock() - start < 0.25, "utf8_reverse took too long on 60,000 characters")
# assert(back == ("x€é"):rep(20000), "reversing 60,000 characters")
# assert(utf8_reverse(back) == text, "reversing twice gives back the original")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 5: Merging settings (LO-3.3, LO-3.1, 3 points)
#
# A program keeps its default settings in a table, and each user's changes in another. Write
# `merge_settings(defaults, overrides)`, which returns a new table with every setting from both:
#
# - A setting in `overrides` replaces the one in `defaults`, whatever its value, `false`
#   included.
# - When a setting is a table in both, the two tables are merged the same way, at every depth.
# - The result shares no table with either argument, so changing the result changes neither
#   argument, and neither argument changes.
#
# For example, with `defaults = { theme = "light", window = { width = 800, height = 600 } }` and
# `overrides = { window = { width = 1024 } }`, the result is
# `{ theme = "light", window = { width = 1024, height = 600 } }`. You may assume that every key is
# a string, and that no table contains itself.

# %% nbgrader={"grade": false, "grade_id": "merge-settings", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function merge_settings(defaults, overrides)
#   -- BEGIN SOLUTION
#   local function copy(value)
#     if type(value) ~= "table" then return value end
#     local result = {}
#     for k, v in pairs(value) do result[k] = copy(v) end
#     return result
#   end
#
#   local result = copy(defaults)
#   for k, v in pairs(overrides) do
#     if type(v) == "table" and type(result[k]) == "table" then
#       result[k] = merge_settings(result[k], v)
#     else
#       result[k] = copy(v)
#     end
#   end
#   return result
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "merge-settings-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false} language="lua"
# local defaults = { theme = "light", window = { width = 800, height = 600 } }
# local overrides = { window = { width = 1024 } }
# local merged = merge_settings(defaults, overrides)
# assert(merged.theme == "light", "a setting only in defaults is kept")
# assert(merged.window.width == 1024 and merged.window.height == 600, "nested tables are merged")
# assert(defaults.window.width == 800, "merge_settings must not change defaults")
# -- BEGIN HIDDEN TESTS
# assert(merged ~= defaults and merged.window ~= defaults.window and merged.window ~= overrides.window,
#   "the result must be made of new tables")
# merged.window.height = 1
# assert(defaults.window.height == 600, "changing the result must not change defaults")
# assert(overrides.window.height == nil, "...nor overrides")
# local m2 = merge_settings({ sound = true, fonts = { size = 12 } }, { sound = false, extra = { a = { 1 } } })
# assert(m2.sound == false, "an override of false replaces the default")
# assert(m2.fonts.size == 12 and m2.extra.a[1] == 1, "settings only in overrides are included")
# local o3 = { list = { 1, 2 } }
# local m3 = merge_settings({}, o3)
# m3.list[1] = 99
# assert(o3.list[1] == 1, "a table taken from overrides must be copied, not shared")
# local m4 = merge_settings({ mode = { fast = true } }, { mode = "slow" })
# assert(m4.mode == "slow", "an override that isn't a table replaces a table")
# local m5 = merge_settings({ mode = "slow" }, { mode = { fast = true } })
# assert(type(m5.mode) == "table" and m5.mode.fast == true, "a table override replaces a non-table")
# local deep = merge_settings({ a = { b = { c = 1, d = 2 } } }, { a = { b = { c = 3 } } })
# assert(deep.a.b.c == 3 and deep.a.b.d == 2, "merging works at every depth")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 6: Lists with holes (LO-3.2, LO-2.2, 3 points)
#
# ### Part A (2 points)
#
# A list of `n` slots may have `nil` in some of them. Write `compact(list, n)`, which returns two
# values: a new sequence of the values in slots 1 to `n` that aren't `nil`, in their order, and
# the number of those values. `compact({ "a", nil, "c", nil }, 4)` returns `{ "a", "c" }` and 2. It
# must not change `list`.

# %% nbgrader={"grade": false, "grade_id": "compact", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function compact(list, n)
#   -- BEGIN SOLUTION
#   local result, count = {}, 0
#   for i = 1, n do
#     if list[i] ~= nil then
#       count = count + 1
#       result[count] = list[i]
#     end
#   end
#   return result, count
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "compact-tests", "locked": true, "points": 2, "schema_version": 3, "solution": false, "task": false} language="lua"
# local values, count = compact({ "a", nil, "c", nil }, 4)
# assert(count == 2 and values[1] == "a" and values[2] == "c", "compact should keep \"a\" and \"c\"")
# assert(select("#", compact({}, 0)) == 2, "compact should return two values")
# -- BEGIN HIDDEN TESTS
# local sparse = {}
# sparse[1], sparse[3], sparse[5] = 1, 3, 5
# local v2, c2 = compact(sparse, 5)
# assert(c2 == 3 and v2[1] == 1 and v2[2] == 3 and v2[3] == 5 and #v2 == 3,
#   "compact must reach slot n even where # stops early")
# local packed = table.pack(nil, false, nil, 0)
# local v3, c3 = compact(packed, packed.n)
# assert(c3 == 2 and v3[1] == false and v3[2] == 0, "false and 0 are values, not holes")
# local v4, c4 = compact({ nil, nil }, 2)
# assert(c4 == 0 and next(v4) == nil, "a list of holes compacts to an empty list")
# assert(math.type(c4) == "integer", "the count should be an integer")
# local list = { 1, nil, 2 }
# local v5 = compact(list, 3)
# assert(list[2] == nil and list[3] == 2 and v5 ~= list, "compact must return a new list")
# local v6, c6 = compact({ 1, 2, 3 }, 2)
# assert(c6 == 2 and v6[3] == nil, "slots after n are ignored")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ### Part B (1 point)
#
# Explain in two or three sentences why `compact` takes the number of slots, `n`, instead of using
# `#list`. Give a table, and the way it is built, for which `compact` would lose a value if it used
# `#list`.

# %% [markdown] nbgrader={"grade": true, "grade_id": "compact-written", "locked": false, "points": 1, "schema_version": 3, "solution": true, "task": false}
# BEGIN SOLUTION
#
# A list with holes isn't a sequence, so `#list` may return any of its borders, not the number of
# slots. For a table built as `local t = {}; t[1] = 1; t[3] = 3`, Lua 5.4 gives `#t == 1`, so
# `compact` would stop at slot 1 and lose the 3. The caller knows how many slots there are, as
# `table.pack` records in `n`, so passing `n` is the only reliable way.
#
# Full credit needs both the reason (`#` returns a border, not a count, when there are holes) and
# a table whose `#` misses a value. Half a point for either alone.
#
# END SOLUTION

# %% [markdown]
# ## Tools you used
#
# Say which tools, if any, you used for this assignment and how, or write "none".
#
# *Your answer here.*

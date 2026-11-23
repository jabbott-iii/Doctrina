# %% [markdown]
# # Lab 10: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L10.1
#
# The handle is declared `<close>` only after `io.open` succeeded, because a failed open returns
# `nil` and a message, and the message must go back to the caller. `return fn(f)` looks like a tail
# call, but Lua doesn't make it one while a `<close>` variable is in scope, so `f` is closed after
# `fn` returns. Common mistakes: `local f <close> = assert(io.open(path, mode))`, which raises an
# error instead of returning `nil` for a missing file; and calling `f:close()` before returning,
# which skips the error path.

# %% tags=["answer-L10.1"]
# %%lua
function with_file(path, mode, fn)
  local file, err = io.open(path, mode)
  if not file then return nil, err end
  local f <close> = file
  return fn(f)
end

# %% [markdown]
# ## Exercise L10.2
#
# One pass over the characters, with a flag for "inside quotes". Inside quotes, `""` is one quote
# and a lone `"` ends the quoted part; outside, a comma ends the field. Collecting characters in a
# list and joining them avoids `..` in the loop. Common mistakes: splitting with
# `gmatch("[^,]*")`, which breaks a quoted comma into two fields; and forgetting the last field
# after the loop, so `"a,b"` gives only `a`.

# %% tags=["answer-L10.2"]
# %%lua
function csv_split(line)
  local fields, field = {}, {}
  local quoted = false
  local i = 1
  while i <= #line do
    local c = line:sub(i, i)
    if quoted then
      if c == '"' then
        if line:sub(i + 1, i + 1) == '"' then
          field[#field + 1] = '"'
          i = i + 1
        else
          quoted = false
        end
      else
        field[#field + 1] = c
      end
    elseif c == '"' then
      quoted = true
    elseif c == "," then
      fields[#fields + 1] = table.concat(field)
      field = {}
    else
      field[#field + 1] = c
    end
    i = i + 1
  end
  fields[#fields + 1] = table.concat(field)
  return fields
end

function csv_join(fields)
  local out = {}
  for i, f in ipairs(fields) do
    if f:find('[,"]') then
      out[i] = '"' .. f:gsub('"', '""') .. '"'
    else
      out[i] = f
    end
  end
  return table.concat(out, ",")
end

# %% [markdown]
# ## Exercise L10.3
#
# The `<close>` handle covers the early `return` for a bad line. The header line is line 1, so the
# counter starts there. Common mistakes: raising an error for a bad line, which the statement says
# is outside data; counting from the first record instead of the header, which reports line 3; and
# `io.lines(path)` without a check, which raises an error for a missing file instead of returning
# `nil`.

# %% tags=["answer-L10.3"]
# %%lua
function read_records(path)
  local file, err = io.open(path)
  if not file then return nil, err end
  local f <close> = file
  local header, records, n = nil, {}, 0
  for line in f:lines() do
    n = n + 1
    local fields = csv_split(line)
    if header == nil then
      header = fields
    elseif #fields ~= #header then
      return nil, string.format("line %d: expected %d fields, got %d", n, #header, #fields)
    else
      local record = {}
      for i, name in ipairs(header) do record[name] = fields[i] end
      records[#records + 1] = record
    end
  end
  return records
end

# %% [markdown]
# ## Exercise L10.4
#
# `%q` writes integers as integers and floats in hexadecimal, so every number reads back with its
# type and value, which the check compares. The comparator orders keys by type name first, and
# `"number" < "string"`, then by value. Common mistakes: `tostring` for numbers, which loses
# precision for floats such as 0.1 and turns `math.mininteger` into a float; `pairs` order, which
# changes between runs; and calling the chunk without `pcall`, so a runtime error escapes
# `deserialize`.

# %% tags=["answer-L10.4"]
# %%lua
local function literal(v)
  if type(v) ~= "table" then
    return string.format("%q", v)
  end
  local keys = {}
  for k in pairs(v) do keys[#keys + 1] = k end
  table.sort(keys, function(a, b)
    if type(a) ~= type(b) then return type(a) < type(b) end
    return a < b
  end)
  local parts = {}
  for i, k in ipairs(keys) do
    parts[i] = "[" .. literal(k) .. "]=" .. literal(v[k])
  end
  return "{" .. table.concat(parts, ",") .. "}"
end

function serialize(value)
  return "return " .. literal(value)
end

function deserialize(text)
  local chunk, err = load(text, "=data", "t", {})
  if not chunk then return nil, err end
  local ok, result = pcall(chunk)
  if not ok then return nil, result end
  return result
end

# %% [markdown]
# ## Exercise L10.5
#
# `gsub` replaces each `'` with `'\''`: close the quotes, an escaped quote, reopen. The dates use
# `hour = 12`, so a change of daylight saving time moves them by an hour, never across midnight,
# and rounding the difference to whole days absorbs that hour. Leaving `hour` out also gives noon
# in Lua 5.4; setting it to 0 doesn't. Common mistakes: dividing with `//`, which loses a day when
# the difference is an hour short; and returning a float.

# %% tags=["answer-L10.5"]
# %%lua
function shell_quote(s)
  return "'" .. s:gsub("'", "'\\''") .. "'"
end

local function noon_of(date)
  local y, m, d = date:match("^(%d%d%d%d)%-(%d%d)%-(%d%d)$")
  if not y then return nil end
  return os.time({ year = tonumber(y), month = tonumber(m), day = tonumber(d), hour = 12 })
end

function days_between(from, to)
  local a = noon_of(from)
  if not a then return nil, "not a date: " .. from end
  local b = noon_of(to)
  if not b then return nil, "not a date: " .. to end
  return math.floor(os.difftime(b, a) / 86400 + 0.5)
end

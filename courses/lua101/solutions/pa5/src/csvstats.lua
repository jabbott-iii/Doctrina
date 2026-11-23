-- csvstats: statistics for each column of a CSV file. The model solution for LUA101's PA5.

local csvstats = {}

---Splits one line of CSV into its fields. A field in double quotes may contain commas, and a
---doubled double quote inside it stands for one double quote.
---@param line string
---@return string[] fields
function csvstats.split_line(line)
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

---Reads a CSV file whose first line names the columns. Empty lines are skipped.
---@param path string
---@return string[]? header the column names, or nil on failure
---@return string[][]|string rows the rows of fields, or the error message
function csvstats.read(path)
  local file, err = io.open(path)
  if not file then
    return nil, err or (path .. ": cannot open")
  end
  local f <close> = file
  local header, rows, number = nil, {}, 0
  for line in f:lines() do
    number = number + 1
    if line ~= "" then
      local fields = csvstats.split_line(line)
      if header == nil then
        header = fields
      elseif #fields ~= #header then
        return nil,
          string.format("%s:%d: expected %d fields, got %d", path, number, #header, #fields)
      else
        rows[#rows + 1] = fields
      end
    end
  end
  if header == nil then
    return nil, path .. ": no header line"
  end
  return header, rows
end

---@class Summary
---@field name string
---@field kind "number"|"text"|"empty"
---@field count integer values that aren't missing
---@field missing integer empty fields
---@field min number?
---@field max number?
---@field mean number?
---@field distinct integer?
---@field top string?

---@class Column
---@field name string
---@field texts string[]
---@field numbers number[]
---@field missing integer
local Column = {}
Column.__index = Column
csvstats.Column = Column

---Makes an empty column.
---@param name string
---@return Column
function Column.new(name)
  return setmetatable({ name = name, texts = {}, numbers = {}, missing = 0 }, Column)
end

---Adds one field's text to the column. An empty field counts as missing.
---@param text string
function Column:add(text)
  if text == "" then
    self.missing = self.missing + 1
    return
  end
  self.texts[#self.texts + 1] = text
  local number = tonumber(text)
  if number then
    self.numbers[#self.numbers + 1] = number
  end
end

---Summarizes the column: numbers if every value is a number, text otherwise.
---@return Summary
function Column:summary()
  local count = #self.texts
  local summary = { name = self.name, count = count, missing = self.missing }
  if count == 0 then
    summary.kind = "empty"
  elseif #self.numbers == count then
    summary.kind = "number"
    local total, low, high = 0, self.numbers[1], self.numbers[1]
    for _, n in ipairs(self.numbers) do
      total = total + n
      low, high = math.min(low, n), math.max(high, n)
    end
    summary.min, summary.max, summary.mean = low, high, total / count
  else
    summary.kind = "text"
    local seen, distinct = {}, 0
    for _, text in ipairs(self.texts) do
      if seen[text] == nil then
        distinct = distinct + 1
      end
      seen[text] = (seen[text] or 0) + 1
    end
    local top
    for text, times in pairs(seen) do
      if top == nil or times > seen[top] or (times == seen[top] and text < top) then
        top = text
      end
    end
    summary.distinct, summary.top = distinct, top
  end
  return summary
end

---Summarizes every column of a table read by `csvstats.read`, in order.
---@param header string[]
---@param rows string[][]
---@return Summary[]
function csvstats.analyze(header, rows)
  local columns = {}
  for i, name in ipairs(header) do
    columns[i] = Column.new(name)
  end
  for _, row in ipairs(rows) do
    for i, column in ipairs(columns) do
      column:add(row[i])
    end
  end
  local summaries = {}
  for i, column in ipairs(columns) do
    summaries[i] = column:summary()
  end
  return summaries
end

---Formats summaries as lines of text, one per column.
---@param summaries Summary[]
---@return string
function csvstats.format(summaries)
  local lines = {}
  for i, s in ipairs(summaries) do
    local line = string.format("%s: %s, %d values, %d missing", s.name, s.kind, s.count, s.missing)
    if s.kind == "number" then
      line = line .. string.format(", min %g, max %g, mean %.2f", s.min, s.max, s.mean)
    elseif s.kind == "text" then
      line = line .. string.format(", %d distinct, most common %s", s.distinct, s.top)
    end
    lines[i] = line
  end
  return table.concat(lines, "\n")
end

return csvstats

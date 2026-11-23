-- csvstats: statistics for each column of a CSV file, for LUA101's PA5.
-- Tools used: write "none", or say which tools you used and how.
-- Discussed with: write "no one", or name everyone you discussed this assignment with.
--
-- The handout, README.md, says exactly what each function must do. Annotate every public function
-- and the Column class with LuaCATS.

local csvstats = {}

function csvstats.split_line(line)
  error("not implemented")
end

function csvstats.read(path)
  error("not implemented")
end

local Column = {}
Column.__index = Column
csvstats.Column = Column

function Column.new(name)
  error("not implemented")
end

-- Your code here: Column:add(text) and Column:summary().

function csvstats.analyze(header, rows)
  error("not implemented")
end

function csvstats.format(summaries)
  error("not implemented")
end

return csvstats

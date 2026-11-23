-- hidden_spec.lua: the hidden tests for PA5. tools/grade_project.py runs them in a copy of the
-- submission's project, with src/ on the module path, and weights each describe block by the
-- points in its name. The command's tests run `lua bin/csvstats` through the shell.

local csvstats = require("csvstats")

local function write_file(text)
  local path = os.tmpname()
  local f <close> = assert(io.open(path, "w"))
  f:write(text)
  return path
end

local function read_file(path)
  local f <close> = assert(io.open(path))
  return f:read("a")
end

local SAMPLE = 'city,temp,note\nOslo,3,"cold, windy"\nLima,19,\nOslo,-2,cold\n\nRome,15.5,"said ""hi"""\n'
local SAMPLE_REPORT = table.concat({
  "city: text, 4 values, 0 missing, 3 distinct, most common Oslo",
  "temp: number, 4 values, 0 missing, min -2, max 19, mean 8.88",
  "note: text, 3 values, 1 missing, 3 distinct, most common cold",
}, "\n")

-- Runs the command with the given arguments; returns its exit status, standard output, and
-- standard error.
local function run_command(args)
  local out, err = os.tmpname(), os.tmpname()
  local _, _, status = os.execute("LUA_PATH='./src/?.lua;;' lua bin/csvstats " .. args .. " > " ..
    out .. " 2> " .. err)
  local stdout, stderr = read_file(out), read_file(err)
  os.remove(out)
  os.remove(err)
  return status, stdout, stderr
end

describe("csvstats.split_line (8 points)", function()
  it("splits plain fields", function()
    assert.are.same({ "a", "b", "c" }, csvstats.split_line("a,b,c"))
  end)

  it("keeps commas inside quotes, and turns doubled quotes into one", function()
    assert.are.same({ "x", "London, UK", 'say "hi"' }, csvstats.split_line('x,"London, UK","say ""hi"""'))
  end)

  it("keeps empty fields", function()
    assert.are.same({ "", "", "" }, csvstats.split_line(",,"))
    assert.are.same({ "" }, csvstats.split_line(""))
    assert.are.same({ "", "z" }, csvstats.split_line('"",z'))
  end)
end)

describe("csvstats.read (14 points)", function()
  it("returns the header and the rows, skipping empty lines", function()
    local path = write_file(SAMPLE)
    local header, rows = csvstats.read(path)
    os.remove(path)
    assert.are.same({ "city", "temp", "note" }, header)
    assert.are.equal(4, #rows)
    assert.are.same({ "Rome", "15.5", 'said "hi"' }, rows[4])
  end)

  it("returns nil and io.open's message for a missing file", function()
    local header, message = csvstats.read("/no/such/file.csv")
    assert.is_nil(header)
    assert.is_truthy(message:find("No such file", 1, true))
  end)

  it("reports the first line with the wrong number of fields, counting every line", function()
    local path = write_file("a,b\n1,2\n\n3\n4,5\n")
    local header, message = csvstats.read(path)
    os.remove(path)
    assert.is_nil(header)
    assert.are.equal(path .. ":4: expected 2 fields, got 1", message)
  end)

  it("reports a file without a header line", function()
    local path = write_file("\n\n")
    local header, message = csvstats.read(path)
    os.remove(path)
    assert.is_nil(header)
    assert.are.equal(path .. ": no header line", message)
  end)

  it("reads a file with a header and no rows", function()
    local path = write_file("a,b\n")
    local header, rows = csvstats.read(path)
    os.remove(path)
    assert.are.same({ "a", "b" }, header)
    assert.are.same({}, rows)
  end)
end)

describe("csvstats.Column (18 points)", function()
  local function column_of(name, values)
    local column = csvstats.Column.new(name)
    for _, v in ipairs(values) do column:add(v) end
    return column
  end

  it("is a class whose methods live in csvstats.Column", function()
    local column = csvstats.Column.new("x")
    assert.are.equal(csvstats.Column, getmetatable(column))
    assert.is_nil(rawget(column, "add"))
    assert.is_nil(rawget(column, "summary"))
  end)

  it("summarizes a column of numbers", function()
    local s = column_of("temp", { "3", "19", "", "-2", "15.5" }):summary()
    assert.are.same({ "temp", "number", 4, 1 }, { s.name, s.kind, s.count, s.missing })
    assert.are.same({ -2, 19, 8.875 }, { s.min, s.max, s.mean })
  end)

  it("treats a column as text unless every value is a number", function()
    local s = column_of("mixed", { "1", "2", "three" }):summary()
    assert.are.equal("text", s.kind)
    assert.are.equal(3, s.distinct)
  end)

  it("counts distinct texts, and picks the most common, alphabetically among ties", function()
    local s = column_of("city", { "Oslo", "Lima", "Oslo", "Lima", "Rome", "" }):summary()
    assert.are.same({ "text", 5, 1, 3, "Lima" }, { s.kind, s.count, s.missing, s.distinct, s.top })
  end)

  it("compares texts as written", function()
    local s = column_of("codes", { "1", "1.0", "x" }):summary()
    assert.are.equal(3, s.distinct)
  end)

  it("reports a column with no values as empty", function()
    local s = column_of("blank", { "", "" }):summary()
    assert.are.same({ "empty", 0, 2 }, { s.kind, s.count, s.missing })
    assert.is_nil(s.mean)
  end)
end)

describe("csvstats.analyze and csvstats.format (14 points)", function()
  it("summarizes each column in order", function()
    local summaries = csvstats.analyze({ "a", "b" }, { { "1", "x" }, { "3", "y" } })
    assert.are.same({ "a", "b" }, { summaries[1].name, summaries[2].name })
    assert.are.same({ "number", "text" }, { summaries[1].kind, summaries[2].kind })
    assert.are.equal(2.0, summaries[1].mean)
  end)

  it("formats the sample's report", function()
    local path = write_file(SAMPLE)
    local header, rows = csvstats.read(path)
    os.remove(path)
    assert.are.equal(SAMPLE_REPORT, csvstats.format(csvstats.analyze(header, rows)))
  end)

  it("formats numbers with %g and the mean with two decimals", function()
    local summaries = csvstats.analyze({ "n" }, { { "0.5" }, { "1e20" } })
    assert.are.equal("n: number, 2 values, 0 missing, min 0.5, max 1e+20, mean 50000000000000000000.00",
      csvstats.format(summaries))
  end)

  it("formats an empty column", function()
    assert.are.equal("blank: empty, 0 values, 3 missing",
      csvstats.format(csvstats.analyze({ "blank" }, { { "" }, { "" }, { "" } })))
  end)
end)

describe("the csvstats command (16 points)", function()
  it("prints the report and exits with status 0", function()
    local path = write_file(SAMPLE)
    local status, stdout, stderr = run_command(path)
    os.remove(path)
    assert.are.equal(0, status)
    assert.are.equal(SAMPLE_REPORT .. "\n", stdout)
    assert.are.equal("", stderr)
  end)

  it("prints a usage message to standard error, and exits with 2, without one argument", function()
    local status, stdout, stderr = run_command("")
    assert.are.equal(2, status)
    assert.are.equal("", stdout)
    assert.are.equal("usage: csvstats FILE.csv\n", stderr)
    assert.are.equal(2, (run_command("a.csv b.csv")))
  end)

  it("reports a missing file on standard error, and exits with 1", function()
    local status, stdout, stderr = run_command("/no/such/file.csv")
    assert.are.equal(1, status)
    assert.are.equal("", stdout)
    assert.is_truthy(stderr:find("^csvstats: /no/such/file%.csv: No such file"))
  end)

  it("reports a malformed file on standard error, and exits with 1", function()
    local path = write_file("a,b\n1\n")
    local status, stdout, stderr = run_command(path)
    os.remove(path)
    assert.are.equal(1, status)
    assert.are.equal("", stdout)
    assert.are.equal("csvstats: " .. path .. ":2: expected 2 fields, got 1\n", stderr)
  end)
end)

-- csvstats_spec.lua: a model student test suite for PA5, which earns full marks on the rubric's
-- Tests criterion. tools/grade_project.py --self-test runs it against the model and the broken
-- versions. Run it from the project's folder with `busted --lpath=./src/?.lua`.

local csvstats = require("csvstats")

local function with_file(text, fn)
  local path = os.tmpname()
  local f <close> = assert(io.open(path, "w"))
  f:write(text)
  f:close()
  local ok, err = pcall(fn, path)
  os.remove(path)
  assert(ok, err)
end

local function slurp(path)
  local f <close> = assert(io.open(path))
  local text = f:read("a")
  os.remove(path)
  return text
end

local function run(args)
  local out, err = os.tmpname(), os.tmpname()
  local _, _, status = os.execute(
    "LUA_PATH='./src/?.lua;;' lua bin/csvstats " .. args .. " > " .. out .. " 2> " .. err
  )
  return status, slurp(out), slurp(err)
end

describe("csvstats.split_line", function()
  it("handles quoted commas and doubled quotes", function()
    assert.are.same({ "a, b", 'x "y"' }, csvstats.split_line('"a, b","x ""y"""'))
  end)
end)

describe("csvstats.read", function()
  it("skips empty lines, and counts them in line numbers", function()
    with_file("a,b\n\n1,2\n3\n", function(path)
      local header, message = csvstats.read(path)
      assert.is_nil(header)
      assert.are.equal(path .. ":4: expected 2 fields, got 1", message)
    end)
    with_file("a\n\n1\n", function(path)
      local _, rows = csvstats.read(path)
      assert.are.equal(1, #rows)
    end)
  end)
end)

describe("csvstats.read's failures", function()
  it("returns nil and a message for a missing file", function()
    local header, message = csvstats.read("/no/such/file.csv")
    assert.is_nil(header)
    assert.is_truthy(message:find("No such file", 1, true))
  end)

  it("returns nil and a message for a file without a header line", function()
    with_file("\n", function(path)
      assert.are.same({ nil, path .. ": no header line" }, { csvstats.read(path) })
    end)
  end)
end)

describe("csvstats.Column", function()
  local function summary_of(values)
    local column = csvstats.Column.new("c")
    for _, v in ipairs(values) do
      column:add(v)
    end
    return column:summary()
  end

  it("counts empty fields as missing", function()
    local s = summary_of({ "1", "", "2" })
    assert.are.same({ 2, 1 }, { s.count, s.missing })
  end)

  it("needs every value to be a number for a number column", function()
    assert.are.equal("text", summary_of({ "1", "x" }).kind)
  end)

  it("computes the mean as a float", function()
    assert.are.equal(1.5, summary_of({ "1", "2" }).mean)
  end)

  it("breaks ties for the most common text alphabetically", function()
    assert.are.equal("a", summary_of({ "b", "a" }).top)
  end)
end)

describe("csvstats.format", function()
  it("formats text and empty columns", function()
    local summaries = csvstats.analyze({ "t", "e" }, { { "x", "" }, { "y", "" }, { "x", "" } })
    assert.are.equal(
      "t: text, 3 values, 0 missing, 2 distinct, most common x\ne: empty, 0 values, 3 missing",
      csvstats.format(summaries)
    )
  end)

  it("prints the mean with two decimals", function()
    local line = csvstats.format(csvstats.analyze({ "n" }, { { "1" }, { "2" }, { "2" } }))
    assert.are.equal("n: number, 3 values, 0 missing, min 1, max 2, mean 1.67", line)
  end)
end)

describe("the csvstats command", function()
  it("reports an error on standard error, with exit status 1", function()
    local status, stdout, stderr = run("/no/such/file.csv")
    assert.are.equal(1, status)
    assert.are.equal("", stdout)
    assert.is_truthy(stderr:find("^csvstats: "))
  end)
end)

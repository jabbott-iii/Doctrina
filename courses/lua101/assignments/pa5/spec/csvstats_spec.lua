-- csvstats_spec.lua: your tests for PA5. Run them from this folder with
-- `busted --lpath=./src/?.lua`. Two examples are here to start from.

local csvstats = require("csvstats")

describe("csvstats.split_line", function()
  it("splits plain fields", function()
    assert.are.same({ "a", "b", "c" }, csvstats.split_line("a,b,c"))
  end)
end)

describe("csvstats.Column", function()
  it("counts an empty field as missing", function()
    local column = csvstats.Column.new("x")
    column:add("")
    assert.are.equal(1, column:summary().missing)
  end)
end)

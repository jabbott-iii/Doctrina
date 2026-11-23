-- iter_spec.lua: your tests for PA3. Run them with `busted` from this assignment's folder.
-- Two examples are here to start from; add tests until every promise in the handout is tested.

local iter = require("iter")

describe("iter.from_list", function()
  it("gives the values in order, then nil", function()
    local it = iter.from_list({ "a", "b" })
    assert.are.equal("a", it())
    assert.are.equal("b", it())
    assert.is_nil(it())
  end)
end)

describe("iter.take", function()
  it("raises an error for a negative n", function()
    assert.has_error(function() iter.take(-1, iter.count()) end,
      "take: n must be a non-negative integer")
  end)
end)

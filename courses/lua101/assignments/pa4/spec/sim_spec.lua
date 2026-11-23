-- sim_spec.lua: your tests for PA4. Run them with `busted` from this assignment's folder.
-- Two examples are here to start from; add tests until every promise in the handout is tested.

local sim = require("sim")

describe("sim.Customer", function()
  it("has a tostring", function()
    assert.are.equal("Customer 2 (arrives 5, needs 3)", tostring(sim.Customer.new(2, 5, 3)))
  end)
end)

describe("sim.Scheduler", function()
  it("runs a task that sleeps, and moves its clock", function()
    local s = sim.Scheduler.new()
    local woke_at
    s:spawn(function() s:sleep(4); woke_at = s:now() end)
    s:run()
    assert.are.equal(4, woke_at)
  end)
end)

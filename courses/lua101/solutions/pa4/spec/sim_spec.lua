-- sim_spec.lua: a model student test suite for PA4, which earns full marks on the rubric's Tests
-- criterion. tools/grade_project.py --self-test runs it against the model and the broken versions.

local sim = require("sim")

describe("sim.arrivals", function()
  it("gives the documented customers for seed 1", function()
    local got = {}
    for c in sim.arrivals({ seed = 1, customers = 3, gap = { 1, 4 }, service = { 2, 6 } }) do
      got[#got + 1] = c.arrival .. "/" .. c.service
    end
    assert.are.same({ "3/5", "4/2", "7/2" }, got)
  end)
end)

describe("sim.Customer", function()
  it("raises an error for the wait of a customer who hasn't started", function()
    assert.has_error(function() sim.Customer.new(4, 0, 1):wait() end, "customer 4 has not started")
  end)

  it("orders by arrival, then by id", function()
    local early, late = sim.Customer.new(1, 5, 1), sim.Customer.new(2, 5, 1)
    assert.is_true(early < late)
    assert.is_false(late < early)
  end)
end)

describe("sim.Scheduler", function()
  local function names_in_order(s, names)
    local log = {}
    for _, name in ipairs(names) do
      s:spawn(function() log[#log + 1] = name end)
    end
    return log
  end

  it("runs tasks due at the same time in the order they were scheduled", function()
    local s = sim.Scheduler.new()
    local log = names_in_order(s, { "first", "second", "third" })
    s:run()
    assert.are.same({ "first", "second", "third" }, log)
  end)

  it("runs tasks due exactly at until_time", function()
    local s, count = sim.Scheduler.new(), 0
    s:spawn(function() count = count + 1 end, 2)
    s:run(2)
    assert.are.equal(1, count)
  end)

  it("wakes every waiting task on a signal", function()
    local s, woken = sim.Scheduler.new(), 0
    for _ = 1, 3 do s:spawn(function() s:wait("bell"); woken = woken + 1 end) end
    s:spawn(function() s:sleep(1); s:signal("bell") end)
    s:run()
    assert.are.equal(3, woken)
  end)
end)

describe("sim.Server", function()
  it("lets a FastServer take half the time, rounded up", function()
    assert.are.equal(3, sim.FastServer.new("F"):service_time(sim.Customer.new(1, 0, 5)))
  end)
end)

describe("sim.run_bank and sim.format_report", function()
  local function bank()
    return sim.run_bank({ seed = 7, customers = 8, gap = { 1, 4 }, service = { 3, 8 },
      servers = { sim.Server.new("A"), sim.FastServer.new("B") } })
  end

  it("serves every customer and counts each server's busy time", function()
    local report = bank()
    assert.are.equal(24, report.finish)
    assert.are.same({ 17, 19 }, { report.servers[1].busy, report.servers[2].busy })
    for _, c in ipairs(report.customers) do assert.is_not_nil(c.finish) end
  end)

  it("reports the mean wait with two decimals", function()
    assert.is_truthy(sim.format_report(bank()):find("mean wait: 0.88", 1, true))
  end)
end)

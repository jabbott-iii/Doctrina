-- hidden_spec.lua: the hidden tests for PA4. tools/grade_project.py runs them against a
-- submission's sim.lua, and weights each describe block by the points in its name.

local sim = require("sim")

local function message_of(fn)
  local ok, err = pcall(fn)
  assert(not ok, "expected an error, but the call returned normally")
  return tostring(err)
end

local function collect(iterator)
  local list = {}
  for value in iterator do list[#list + 1] = value end
  return list
end

local SMALL = { seed = 1, customers = 5, gap = { 1, 4 }, service = { 2, 6 } }

local function two_server_bank()
  return sim.run_bank({ seed = 7, customers = 8, gap = { 1, 4 }, service = { 3, 8 },
    servers = { sim.Server.new("A"), sim.FastServer.new("B") } })
end

describe("sim.arrivals (8 points)", function()
  it("draws each gap, then each service time, from the seed", function()
    local customers = collect(sim.arrivals(SMALL))
    assert.are.equal(5, #customers)
    local arrivals, services = {}, {}
    for i, c in ipairs(customers) do arrivals[i], services[i] = c.arrival, c.service end
    assert.are.same({ 3, 4, 7, 10, 12 }, arrivals)
    assert.are.same({ 5, 2, 2, 4, 3 }, services)
  end)

  it("gives Customer objects numbered from 1", function()
    local customers = collect(sim.arrivals(SMALL))
    for i, c in ipairs(customers) do
      assert.are.equal(sim.Customer, getmetatable(c))
      assert.are.equal(i, c.id)
    end
  end)

  it("gives the same customers for the same seed, and nothing for zero customers", function()
    local a = collect(sim.arrivals(SMALL))
    local b = collect(sim.arrivals(SMALL))
    assert.are.equal(a[5].arrival, b[5].arrival)
    assert.are.same({}, collect(sim.arrivals({ seed = 1, customers = 0, gap = { 1, 2 },
      service = { 1, 2 } })))
  end)

  it("handles ranges of a single value", function()
    local customers = collect(sim.arrivals({ seed = 9, customers = 3, gap = { 2, 2 },
      service = { 3, 3 } }))
    assert.are.same({ 2, 4, 6 }, { customers[1].arrival, customers[2].arrival, customers[3].arrival })
    assert.are.equal(3, customers[3].service)
  end)
end)

describe("sim.Customer (8 points)", function()
  it("stores its fields, and starts with no start time", function()
    local c = sim.Customer.new(3, 10, 4)
    assert.are.same({ 3, 10, 4 }, { c.id, c.arrival, c.service })
    assert.is_nil(c.start)
    assert.is_nil(rawget(c, "wait"))
  end)

  it("reports its wait once it has started", function()
    local c = sim.Customer.new(1, 10, 4)
    c.start = 13
    assert.are.equal(3, c:wait())
  end)

  it("raises an error, at level 2, for the wait of a customer who hasn't started", function()
    local err = message_of(function() sim.Customer.new(7, 0, 1):wait() end)
    assert.is_truthy(err:find("customer 7 has not started", 1, true))
    assert.is_truthy(err:find("hidden_spec.lua:%d+:"))
  end)

  it("has a tostring", function()
    assert.are.equal("Customer 2 (arrives 5, needs 3)", tostring(sim.Customer.new(2, 5, 3)))
  end)

  it("orders customers by arrival, then by id", function()
    local a, b, c = sim.Customer.new(2, 5, 1), sim.Customer.new(1, 5, 9), sim.Customer.new(3, 4, 1)
    assert.is_true(b < a)
    assert.is_true(c < b)
    assert.is_false(a < a)
    assert.is_true(a <= a)
    local list = { a, b, c }
    table.sort(list)
    assert.are.same({ 3, 1, 2 }, { list[1].id, list[2].id, list[3].id })
  end)
end)

describe("sim.Scheduler (20 points)", function()
  it("starts at time 0, and runs tasks in order of their wake times", function()
    local s, log = sim.Scheduler.new(), {}
    assert.are.equal(0, s:now())
    s:spawn(function() for i = 1, 3 do log[#log + 1] = s:now() .. " a" .. i; s:sleep(2) end end)
    s:spawn(function() log[#log + 1] = s:now() .. " b"; s:sleep(3); log[#log + 1] = s:now() .. " b" end)
    s:spawn(function() log[#log + 1] = s:now() .. " c" end, 5)
    assert.are.equal(7, s:run())
    assert.are.equal("0 a1,0 b,2 a2,3 b,4 a3,5 c", table.concat(log, ","))
    assert.are.equal(6, s:now())
  end)

  it("runs tasks due at the same time in the order they were scheduled", function()
    local s, log = sim.Scheduler.new(), {}
    for _, name in ipairs({ "x", "y", "z" }) do
      s:spawn(function() log[#log + 1] = name; s:sleep(1); log[#log + 1] = name end)
    end
    s:run()
    assert.are.equal("xyzxyz", table.concat(log))
  end)

  it("stops at until_time, and continues on the next run", function()
    local s, beats = sim.Scheduler.new(), 0
    s:spawn(function() while true do beats = beats + 1; s:sleep(1) end end)
    assert.are.equal(4, s:run(3.5))
    assert.are.equal(3, s:now())
    assert.are.equal(2, s:run(5))
    assert.are.equal(5, s:now())
    assert.are.equal(6, beats)
  end)

  it("wakes every task waiting for an event when it is signaled, in the order they waited", function()
    local s, log = sim.Scheduler.new(), {}
    for _, name in ipairs({ "p", "q" }) do
      s:spawn(function() s:wait("go"); log[#log + 1] = s:now() .. name end)
    end
    s:spawn(function() s:sleep(4); s:signal("go"); log[#log + 1] = s:now() .. "signal" end)
    s:run()
    assert.are.equal("4signal,4p,4q", table.concat(log, ","))
  end)

  it("ignores a signal with no waiting tasks, and ends while tasks still wait", function()
    local s, reached = sim.Scheduler.new(), false
    s:spawn(function() s:signal("nobody") end)
    s:spawn(function() s:wait("never"); reached = true end)
    s:run()
    assert.is_false(reached)
  end)

  it("raises the error of a failing task", function()
    local s = sim.Scheduler.new()
    s:spawn(function() s:sleep(1); error("broken", 0) end)
    assert.are.equal("broken", message_of(function() s:run() end))
  end)

  it("raises an error when sleep or wait is called outside a task", function()
    local s = sim.Scheduler.new()
    assert.is_truthy(message_of(function() s:sleep(1) end):find("sleep: not inside a task", 1, true))
    assert.is_truthy(message_of(function() s:wait("e") end):find("wait: not inside a task", 1, true))
  end)

  it("keeps two schedulers apart", function()
    local s1, s2 = sim.Scheduler.new(), sim.Scheduler.new()
    s1:spawn(function() s1:sleep(10) end)
    s2:spawn(function() s2:sleep(1) end)
    s2:run()
    assert.are.equal(1, s2:now())
    assert.are.equal(0, s1:now())
  end)
end)

describe("sim.Server (12 points)", function()
  it("starts with nothing served, and serves for the customer's time", function()
    local server = sim.Server.new("A")
    assert.are.same({ "A", 0, 0 }, { server.name, server.served, server.busy })
    assert.are.equal(7, server:service_time(sim.Customer.new(1, 0, 7)))
    assert.are.equal("Server A (served 0, busy 0)", tostring(server))
  end)

  it("has a subclass FastServer that takes half the time, rounded up", function()
    local fast = sim.FastServer.new("F")
    assert.are.equal(3, fast:service_time(sim.Customer.new(1, 0, 5)))
    assert.are.equal(2, fast:service_time(sim.Customer.new(2, 0, 4)))
    assert.are.equal(1, fast:service_time(sim.Customer.new(3, 0, 1)))
  end)

  it("makes FastServer inherit the rest of Server, tostring included", function()
    local fast = sim.FastServer.new("F")
    assert.is_nil(rawget(sim.FastServer, "work"))
    assert.are.equal(sim.Server.work, fast.work)
    assert.are.equal("Server F (served 0, busy 0)", tostring(fast))
  end)

  it("counts what each server served, and for how long", function()
    local report = two_server_bank()
    local a, b = report.servers[1], report.servers[2]
    assert.are.same({ 3, 17 }, { a.served, a.busy })
    assert.are.same({ 5, 19 }, { b.served, b.busy })
  end)
end)

describe("sim.run_bank (16 points)", function()
  it("serves every customer, and logs when each one starts", function()
    local report = two_server_bank()
    assert.are.equal(8, #report.customers)
    assert.are.same({
      "t=3 customer 1 starts at A", "t=5 customer 2 starts at B", "t=9 customer 3 starts at B",
      "t=11 customer 4 starts at A", "t=13 customer 5 starts at B", "t=16 customer 6 starts at A",
      "t=17 customer 7 starts at B", "t=20 customer 8 starts at B",
    }, report.log)
  end)

  it("reports the finish time and the waits", function()
    local report = two_server_bank()
    assert.are.equal(24, report.finish)
    assert.are.equal(0.875, report.mean_wait)
    assert.are.equal(3, report.max_wait)
  end)

  it("serves one line in order of arrival with one server", function()
    local report = sim.run_bank({ seed = 3, customers = 30, gap = { 1, 3 }, service = { 1, 5 },
      servers = { sim.Server.new("Solo") } })
    local previous_finish = 0
    for _, c in ipairs(report.customers) do
      assert.are.equal(math.max(c.arrival, previous_finish), c.start)
      assert.are.equal(c.start + c.service, c.finish)
      previous_finish = c.finish
    end
  end)

  it("gives the same totals for 200 customers whichever identical server is listed first", function()
    local function bank(names)
      return sim.run_bank({ seed = 2026, customers = 200, gap = { 1, 5 }, service = { 2, 9 },
        servers = { sim.Server.new(names[1]), sim.Server.new(names[2]) } })
    end
    local r1, r2 = bank({ "A", "B" }), bank({ "B", "A" })
    assert.are.equal(622, r1.finish)
    assert.are.equal(14, r1.max_wait)
    assert.is_true(math.abs(r1.mean_wait - 504 / 200) < 1e-9)
    assert.are.same({ r1.finish, r1.max_wait, r1.mean_wait }, { r2.finish, r2.max_wait, r2.mean_wait })
  end)

  it("handles a bank with no customers", function()
    local report = sim.run_bank({ seed = 1, customers = 0, gap = { 1, 2 }, service = { 1, 2 },
      servers = { sim.Server.new("A") } })
    assert.are.same({ 0, 0, 0 }, { #report.customers, report.finish, report.max_wait })
    assert.are.equal(0, report.mean_wait)
  end)
end)

describe("sim.format_report (6 points)", function()
  it("formats a report", function()
    assert.are.equal(table.concat({
      "customers: 8", "finish time: 24", "mean wait: 0.88", "max wait: 3",
      "A served 3, busy 17", "B served 5, busy 19",
    }, "\n"), sim.format_report(two_server_bank()))
  end)

  it("formats a report with no customers", function()
    local report = sim.run_bank({ seed = 1, customers = 0, gap = { 1, 2 }, service = { 1, 2 },
      servers = { sim.Server.new("Only") } })
    assert.are.equal("customers: 0\nfinish time: 0\nmean wait: 0.00\nmax wait: 0\nOnly served 0, busy 0",
      sim.format_report(report))
  end)
end)

-- sim.lua: a discrete-event simulation of a bank, the model solution for LUA101's PA4.
--
-- Customers arrive at a bank, wait in one line, and are served by the first free server. Time is
-- simulated: a Scheduler resumes coroutine tasks in order of their wake times, so a run takes no
-- real time and gives the same result every time for the same seed.

local sim = {}

-- PROVIDED: a random-number generator with 64-bit integer arithmetic only, so that the same seed
-- gives the same numbers on every machine.
local Random = {}
Random.__index = Random
sim.Random = Random

function Random.new(seed)
  return setmetatable({ state = seed }, Random)
end

-- Returns an integer from lo to hi, inclusive.
function Random:integer(lo, hi)
  self.state = self.state * 6364136223846793005 + 1442695040888963407
  return lo + (self.state >> 33) % (hi - lo + 1)
end

-- PROVIDED: a first-in, first-out queue whose push and pop take constant time (module 3).
local Queue = {}
Queue.__index = Queue
sim.Queue = Queue

function Queue.new()
  return setmetatable({ first = 1, last = 0, items = {} }, Queue)
end

function Queue:push(value)
  self.last = self.last + 1
  self.items[self.last] = value
end

function Queue:pop()
  if self.first > self.last then return nil end
  local value = self.items[self.first]
  self.items[self.first] = nil
  self.first = self.first + 1
  return value
end

function Queue:size()
  return self.last - self.first + 1
end

Queue.__len = Queue.size

-- Customers --------------------------------------------------------------------------------------

local Customer = {}
Customer.__index = Customer
sim.Customer = Customer

function Customer.new(id, arrival, service)
  return setmetatable({ id = id, arrival = arrival, service = service }, Customer)
end

function Customer:wait()
  if self.start == nil then
    error("customer " .. self.id .. " has not started", 2)
  end
  return self.start - self.arrival
end

function Customer.__tostring(c)
  return "Customer " .. c.id .. " (arrives " .. c.arrival .. ", needs " .. c.service .. ")"
end

function Customer.__lt(a, b)
  if a.arrival ~= b.arrival then return a.arrival < b.arrival end
  return a.id < b.id
end

function Customer.__le(a, b)
  if a.arrival ~= b.arrival then return a.arrival < b.arrival end
  return a.id <= b.id
end

-- Yields n customers in order of arrival. For each customer, it draws the gap since the previous
-- arrival, then the service time, so the first customer arrives at the first gap.
function sim.arrivals(options)
  return coroutine.wrap(function()
    local random = Random.new(options.seed)
    local time = 0
    for id = 1, options.customers do
      time = time + random:integer(options.gap[1], options.gap[2])
      local service = random:integer(options.service[1], options.service[2])
      coroutine.yield(Customer.new(id, time, service))
    end
  end)
end

-- The scheduler ------------------------------------------------------------------------------------

local Scheduler = {}
Scheduler.__index = Scheduler
sim.Scheduler = Scheduler

local WAIT = {}     -- marks a yield that waits for an event rather than for time

function Scheduler.new()
  return setmetatable({ clock = 0, timed = {}, waiting = {}, tasks = {} }, Scheduler)
end

function Scheduler:now()
  return self.clock
end

local function schedule(self, task, wake)
  self.timed[#self.timed + 1] = { wake = wake, task = task }
end

function Scheduler:spawn(fn, delay)
  local task = coroutine.create(fn)
  self.tasks[task] = true
  schedule(self, task, self.clock + (delay or 0))
end

local function current_task(self, name)
  local task = coroutine.running()
  if not self.tasks[task] then
    error(name .. ": not inside a task", 3)
  end
end

function Scheduler:sleep(seconds)
  current_task(self, "sleep")
  coroutine.yield(seconds)
end

function Scheduler:wait(event)
  current_task(self, "wait")
  coroutine.yield(WAIT, event)
end

function Scheduler:signal(event)
  local list = self.waiting[event]
  if list == nil then return end
  self.waiting[event] = nil
  for _, task in ipairs(list) do
    schedule(self, task, self.clock)
  end
end

function Scheduler:run(until_time)
  local resumes = 0
  while #self.timed > 0 do
    local next_index = 1
    for i = 2, #self.timed do
      if self.timed[i].wake < self.timed[next_index].wake then next_index = i end
    end
    if until_time and self.timed[next_index].wake > until_time then break end
    local entry = table.remove(self.timed, next_index)
    self.clock = entry.wake
    local ok, first, second = coroutine.resume(entry.task)
    resumes = resumes + 1
    if not ok then error(first, 0) end
    if coroutine.status(entry.task) == "dead" then
      self.tasks[entry.task] = nil
    elseif first == WAIT then
      local list = self.waiting[second] or {}
      list[#list + 1] = entry.task
      self.waiting[second] = list
    else
      schedule(self, entry.task, self.clock + (first or 0))
    end
  end
  return resumes
end

-- Servers --------------------------------------------------------------------------------------------

local Server = {}
Server.__index = Server
sim.Server = Server

function Server.new(name)
  return setmetatable({ name = name, served = 0, busy = 0 }, Server)
end

function Server:service_time(customer) -- luacheck: ignore 212/self
  return customer.service
end

function Server.__tostring(s)
  return "Server " .. s.name .. " (served " .. s.served .. ", busy " .. s.busy .. ")"
end

-- The server's task: serve customers from the line until it is empty and no more will come.
function Server:work(bank)
  local scheduler = bank.scheduler
  while true do
    local customer = bank.line:pop()
    if customer == nil then
      if bank.closed then return end
      scheduler:wait("arrival")
    else
      customer.start = scheduler:now()
      bank.log[#bank.log + 1] = "t=" .. customer.start .. " customer " .. customer.id ..
        " starts at " .. self.name
      local duration = self:service_time(customer)
      scheduler:sleep(duration)
      customer.finish = scheduler:now()
      self.served = self.served + 1
      self.busy = self.busy + duration
    end
  end
end

local FastServer = setmetatable({}, { __index = Server })
FastServer.__index = FastServer
FastServer.__tostring = Server.__tostring
sim.FastServer = FastServer

function FastServer.new(name)
  return setmetatable(Server.new(name), FastServer)
end

function FastServer:service_time(customer) -- luacheck: ignore 212/self
  return (customer.service + 1) // 2
end

-- The whole bank -------------------------------------------------------------------------------------

function sim.run_bank(options)
  local bank = { scheduler = Scheduler.new(), line = Queue.new(), log = {}, closed = false }
  local customers = {}
  local scheduler = bank.scheduler

  scheduler:spawn(function()
    for customer in sim.arrivals(options) do
      scheduler:sleep(customer.arrival - scheduler:now())
      customers[#customers + 1] = customer
      bank.line:push(customer)
      scheduler:signal("arrival")
    end
    bank.closed = true
    scheduler:signal("arrival")
  end)
  for _, server in ipairs(options.servers) do
    scheduler:spawn(function() server:work(bank) end)
  end
  scheduler:run()

  local total_wait, max_wait, finish = 0, 0, 0
  for _, customer in ipairs(customers) do
    local wait = customer:wait()
    total_wait = total_wait + wait
    if wait > max_wait then max_wait = wait end
    if customer.finish > finish then finish = customer.finish end
  end
  return {
    customers = customers,
    finish = finish,
    mean_wait = #customers > 0 and total_wait / #customers or 0.0,
    max_wait = max_wait,
    servers = options.servers,
    log = bank.log,
  }
end

function sim.format_report(report)
  local lines = {
    "customers: " .. #report.customers,
    "finish time: " .. report.finish,
    string.format("mean wait: %.2f", report.mean_wait),
    "max wait: " .. report.max_wait,
  }
  for _, server in ipairs(report.servers) do
    lines[#lines + 1] = server.name .. " served " .. server.served .. ", busy " .. server.busy
  end
  return table.concat(lines, "\n")
end

return sim

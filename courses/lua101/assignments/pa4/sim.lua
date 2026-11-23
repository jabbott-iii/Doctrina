-- sim.lua: a discrete-event simulation of a bank, for LUA101's PA4.
-- Tools used: write "none", or say which tools you used and how.
-- Discussed with: write "no one", or name everyone you discussed this assignment with.
--
-- Customers arrive at a bank, wait in one line, and are served by the first free server. Time is
-- simulated: a Scheduler resumes coroutine tasks in order of their wake times, so a run takes no
-- real time and gives the same result every time for the same seed. The handout, README.md, says
-- exactly what each part must do.

local sim = {}

-- PROVIDED: a random-number generator with 64-bit integer arithmetic only, so that the same seed
-- gives the same numbers on every machine. Don't change it.
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
  error("not implemented")
end

-- Your code here: Customer:wait(), and the metamethods __tostring, __lt, and __le.

-- Yields the customers of options, in order of arrival.
function sim.arrivals(options)
  error("not implemented")
end

-- The scheduler ------------------------------------------------------------------------------------

local Scheduler = {}
Scheduler.__index = Scheduler
sim.Scheduler = Scheduler

function Scheduler.new()
  error("not implemented")
end

-- Your code here: Scheduler:now(), :spawn(fn, delay), :sleep(seconds), :wait(event),
-- :signal(event), and :run(until_time).

-- Servers --------------------------------------------------------------------------------------------

local Server = {}
Server.__index = Server
sim.Server = Server

function Server.new(name)
  error("not implemented")
end

-- Your code here: Server:service_time(customer), Server:work(bank), and __tostring.

local FastServer = setmetatable({}, { __index = Server })
FastServer.__index = FastServer
sim.FastServer = FastServer

-- Your code here: FastServer.new(name), and FastServer:service_time(customer).

-- The whole bank -------------------------------------------------------------------------------------

function sim.run_bank(options)
  error("not implemented")
end

function sim.format_report(report)
  error("not implemented")
end

return sim

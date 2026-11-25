# PA4: A discrete-event simulation

**Objectives:** LO-7.1, LO-7.2, LO-8.1, LO-8.2, LO-9.2, LO-9.3, and, revisited, LO-5.3 and LO-6.3\
**When:** after Module 10, as the [suggested pace](../../README.md#suggested-pace) places it\
**Checking your work:** the example tests, your own tests, and the rubric below\
**Time:** about 6 hours, spread over modules 9 and 10

You will simulate a bank. Customers arrive, wait in one line, and are served by the first free
server; some servers work twice as fast. The simulation runs on a scheduler of coroutine tasks,
like the one in Lab 9, with a simulated clock, so a day at the bank takes no real time and gives
exactly the same result every run. **Discrete-event simulation**, which jumps the clock from one
event to the next instead of ticking through every moment, is how engineers size checkout lines,
call centers, and network buffers.

## What to hand in

Submit these two files through the learning management system:

- `sim.lua`, the module, with its second line saying which tools you used, and how, or "none",
  and its third line naming everyone you discussed the assignment with, or "no one";
- `spec/sim_spec.lua`, your tests. You may split them across more files in `spec/` whose names
  end in `_spec.lua`.

## Getting started

1. Copy this folder, `assignments/pa4/`, to a folder of your own. It holds the starter module,
   [`sim.lua`](sim.lua), and the starter tests, [`spec/sim_spec.lua`](spec/sim_spec.lua).
2. In a terminal, run `source .venv/lua/bin/activate` from the repository's root, as
   [setting up](../../setup.md) describes, then run `busted` from your copy of the folder. Both
   example tests fail until you write `Customer` and `Scheduler`.

The starter provides two finished pieces. Don't change them: the hidden tests depend on them.

- `sim.Random.new(seed)` makes a random-number generator, and `r:integer(lo, hi)` returns an
  integer from `lo` to `hi`, inclusive. It uses only integer arithmetic, so a seed gives the same
  numbers on every machine.
- `sim.Queue` is module 3's queue, with `Queue.new()`, `q:push(v)`, `q:pop()`, `q:size()`, and
  `#q`.

## The module

Write each part as a class, with its methods in the class table, as module 8 does. Each part below
says exactly what the hidden tests check.

### `sim.Customer`

- `Customer.new(id, arrival, service)` returns a customer with those three fields; its fields
  `start` and `finish` stay `nil` until a server sets them.
- `c:wait()` returns `c.start - c.arrival`. For a customer whose `start` is `nil`, it raises the
  error `customer <id> has not started` at level 2, such as `customer 7 has not started`.
- `tostring(c)` is `Customer <id> (arrives <arrival>, needs <service>)`, such as
  `Customer 2 (arrives 5, needs 3)`.
- `<` and `<=` order customers by arrival time, and customers who arrive at the same time by id.

### `sim.arrivals(options)`

Returns a generator, for the generic `for`, of `options.customers` customers, numbered from 1.
`options.gap` and `options.service` are pairs `{ lo, hi }`. The generator makes one generator
`Random.new(options.seed)`, and for each customer in turn draws two numbers, in this order:

1. the gap since the previous arrival, `r:integer(gap[1], gap[2])`, so the first customer arrives
   at the first gap, counting from time 0;
2. the service time, `r:integer(service[1], service[2])`.

With `{ seed = 1, customers = 5, gap = { 1, 4 }, service = { 2, 6 } }`, the customers arrive at
times 3, 4, 7, 10, and 12, and need 5, 2, 2, 4, and 3.

### `sim.Scheduler`

The scheduler of Lab 9, as a class, with events added:

- `Scheduler.new()` returns a scheduler whose clock is at 0, and `s:now()` returns the clock.
- `s:spawn(fn, delay)` schedules a new task, a coroutine running `fn`, at `now + delay`; `delay`
  defaults to 0.
- `s:sleep(seconds)` makes the current task wait that long.
- `s:wait(event)` makes the current task wait until `event`, any value except `nil`, is signaled.
- `s:signal(event)` schedules every task waiting for `event`, in the order they began waiting, at
  the current time. A task that begins waiting after the signal waits for the next one.
- `s:run(until_time)` runs tasks as Lab 9's `run` does: always the one with the earliest wake time,
  and among tasks with the same wake time, the one that was scheduled first. It stops when no task
  is scheduled for a time, even if some still wait for events, or when the earliest wake time is
  later than `until_time`. It returns the number of resumes. A task that raises an error stops
  `run` with the same error value.
- `sleep` and `wait` called outside a task of that scheduler raise `sleep: not inside a task` and
  `wait: not inside a task`, at level 2.

Two schedulers never share tasks or clocks.

### `sim.Server` and `sim.FastServer`

- `Server.new(name)` returns a server with the fields `name`, `served = 0`, and `busy = 0`.
- `server:service_time(customer)` returns how long the server takes: `customer.service`.
- `tostring(server)` is `Server <name> (served <served>, busy <busy>)`.
- `server:work(bank)` is the body of the server's task. `bank` is a table with the fields
  `scheduler`, `line` (a `Queue` of waiting customers), `log` (a list of strings), and `closed`.
  The server repeats these steps:
  1. Pop the next customer from `bank.line`. If there is none, return if `bank.closed` is `true`;
     otherwise wait for the event `"arrival"`, and start this step again.
  2. Set the customer's `start` to the current time, and append to `bank.log` the line
     `t=<start> customer <id> starts at <name>`.
  3. Sleep for `self:service_time(customer)`, then set the customer's `finish` to the current
     time, add 1 to `served`, and add the service time to `busy`.
- `FastServer` is a subclass of `Server`. `FastServer.new(name)` makes one, and its `service_time`
  is half the customer's, rounded up: 5 becomes 3. Everything else, `tostring` included, works as
  for `Server`.

### `sim.run_bank(options)`

Runs one simulation. `options` has the fields of `sim.arrivals`, and `servers`, a list of `Server`
and `FastServer` objects. It makes a scheduler and a bank, then:

1. Spawns the **arrival task** first. For each customer from `sim.arrivals(options)`, the task
   sleeps until the customer's arrival time, adds the customer to the report's list of customers,
   pushes the customer onto the line, and signals `"arrival"`. After the last customer, it sets
   `bank.closed` to `true` and signals `"arrival"` once more, so idle servers can finish.
2. Spawns one task for each server, in the order of `options.servers`, running `server:work(bank)`.
3. Runs the scheduler until no task is scheduled.

It returns a report: a table with `customers`, the customers in order of arrival; `finish`, the
latest finish time; `mean_wait`, the mean of the customers' waits, as a float; `max_wait`, the
longest wait; `servers`, the list from `options`; and `log`. For a bank with no customers,
`finish`, `mean_wait`, and `max_wait` are 0.

### `sim.format_report(report)`

Returns the report as lines joined by newlines, with no newline at the end: the number of
customers, the finish time, the mean wait with two decimals, the longest wait, and a line for each
server, in order. For two servers, `A` and a `FastServer` `B`, with
`{ seed = 7, customers = 8, gap = { 1, 4 }, service = { 3, 8 } }`:

```text
customers: 8
finish time: 24
mean wait: 0.88
max wait: 3
A served 3, busy 17
B served 5, busy 19
```

## Your tests

Write tests for every promise in this handout: each part's normal results, its edges, and each
error. Test the scheduler with small tasks that log what they do and when, as Lab 9 does. As in
PA3, the grader runs your tests against a correct `sim` module, where they must all pass, and
against 10 versions of it that each break one promise in this handout, where each should make at
least one of your tests fail.

## How it is graded

The course has no grades. This section describes the full check that an instructor or a
mentor who reviews your work can run. The hidden tests aren't published, so when you work
alone, test every promise in this handout yourself, and score your work with the rubric.

### Hidden tests: 70 points

| Part | Points | Part | Points |
| :- | :- | :- | :- |
| `sim.arrivals` | 8 | `sim.Server` and `sim.FastServer` | 12 |
| `sim.Customer` | 8 | `sim.run_bank` | 16 |
| `sim.Scheduler` | 20 | `sim.format_report` | 6 |

Each part's tests earn its points in proportion to how many of them pass. Later parts use earlier
ones, so a broken `Scheduler` costs points in `run_bank` too.

### Rubric: 30 points

| Criterion | Full marks | Partial | Little or none |
| :- | :- | :- | :- |
| **Tests** (10) | Every test passes on a correct module, and the tests catch at least 9 of the 10 broken versions: 10 points | 7–8 caught: 7 points; 4–6: 4 points; 1–3: 1 point | No tests, or none that catch a broken version: 0 points. Each test that fails on a correct module costs 2 points |
| **Design** (10) | Each class keeps its methods in the class table, its state in its objects, and its metamethods where Lua looks for them. `FastServer` overrides only what differs. The scheduler keeps no state outside its objects, and the module creates no globals | The code works, but repeats itself, or keeps state in the module or in globals: 6 points | Methods copied into every object, a subclass that re-implements its parent, or tasks that busy-wait instead of waiting for events: 3 points or fewer |
| **Style** (10) | Consistent two-space indentation, descriptive local names, a comment wherever the reason for the code isn't obvious, no dead or commented-out code, and lines of 100 characters or fewer | Readable, with a few lapses: 6 points | Hard to follow: 3 points or fewer |

## Policies

The course's [policies](../../README.md#policies) apply. Discuss ideas with anyone, but write your
own code and tests, and name everyone you discussed the assignment with on the third line of
`sim.lua`. Generative AI tools may explain concepts and error messages to you, but may not write any
part of the module or its tests; say on the second line of `sim.lua` which tools you used, and how,
or write "none".

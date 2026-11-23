# PA4 answer key and grading notes

Students receive `assignments/pa4/`: the handout, the starter `sim.lua` with `Random` and `Queue`
finished, and two example tests. This folder holds what they don't see:

| File | What it is |
| :- | :- |
| `sim.lua` | The model solution |
| `hidden_spec.lua` | The hidden tests: 28 tests in six blocks, worth 70 points |
| `spec/sim_spec.lua` | A model student test suite, which earns full marks on the Tests criterion |
| `grading.json` | The settings for `tools/grade_project.py`: the module's name and the 10 broken versions |

## Grading a submission

From the repository's root, with the notebook environment active, run the grader on a folder that
holds the submission's `sim.lua` and `spec/`:

```bash
python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa4 path/to/submission
```

It prints the hidden-test points by part, each failed hidden test, how many of the student's tests
pass on the model, and which broken versions they caught. Score **Tests** from that output and the
handout's levels, and **Design** and **Style** by reading `sim.lua`. Check the second and third
lines for the tools used and the people the student talked with.

Before a term's grading, run the self-test, which should give 70.00 of 70 points and catch all 10
broken versions:

```bash
python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa4 --self-test
```

The hidden tests check exact logs and totals, which depend on the order of events at equal times.
The handout fixes that order: ties go to the task scheduled first, the arrival task is spawned
before the servers, and a signal wakes its waiters in the order they began waiting. A submission
that follows the handout gives the model's output exactly; one that differs only in that order
loses points in `run_bank` and `format_report`, and the failed tests' names show where. The test
with 200 customers and two identical servers checks totals that don't depend on which server takes
which customer.

## The broken versions

| Broken version | Caught by a test that… |
| :- | :- |
| Arrivals start the first customer at time 0 | checks the first arrival time for a seed |
| Arrivals draw the service time before the gap | checks the customers for a seed |
| `Customer`'s `<` ignores the id | compares two customers who arrive together |
| `wait` returns `nil` before the customer starts | expects the error for a customer who hasn't started |
| The scheduler breaks ties last in, first out | logs the order of tasks due at the same time |
| `signal` wakes only the first waiting task | counts the tasks a signal wakes |
| `run` stops at `until_time` itself | runs a task due exactly at `until_time` |
| `FastServer` rounds down | checks the service time of an odd one |
| `busy` counts the customer's waiting time too | checks a server's busy time |
| `format_report` rounds the mean wait to one decimal | checks the report's text |

## Design: what to look for

- **Metamethods where Lua looks for them:** `Customer.__tostring`, `__lt`, and `__le` in
  `Customer`, and `Server.__tostring` copied into `FastServer`, which the hidden `tostring` test of
  a `FastServer` checks.
- **An override that changes only what differs:** `FastServer` defines `new` and `service_time`,
  and inherits `work`. A `FastServer` with its own copy of `work` passes the tests, but loses the
  design points the handout names.
- **Waiting, not polling:** a server with nothing to do calls `wait("arrival")`. A server that
  polls instead, looping with `sleep(1)` until the line has a customer, sometimes checks the line
  immediately before a customer arrives at the same time, starts that customer a second late, and
  does many useless resumes. In a trial, the model with a polling server failed 4 of the 28 hidden
  tests, in `run_bank` and `format_report`; the rubric calls it busy-waiting.
- **State in objects:** the scheduler's clock and lists belong to the scheduler object. A module
  with one global clock fails the hidden test that runs two schedulers.

## Reasoning and common mistakes

### `sim.arrivals`

The order of the two draws is the whole point: gap, then service, for each customer. Students who
draw all the gaps first, then all the service times, get different customers for the same seed,
and lose most of the arrivals block and everything that depends on it.

### `sim.Scheduler`

The new parts beyond Lab 9 are `wait` and `signal`. The model's task yields a private marker table
and the event, so `run` can tell a wait from a sleep; a separate table per event holds the waiting
tasks. A task that yields to wait must not be put back in the timed list, or it runs again at once
and busy-waits. `sleep` and `wait` find the current task with `coroutine.running()`, and check that
the scheduler created it, which is also how the test of two schedulers passes.

### `sim.Server` and `sim.FastServer`

`(service + 1) // 2` rounds an integer up. `math.ceil(service / 2)` is equally correct: in Lua
5.4 it returns an integer whenever the result fits in one. `service // 2`, which rounds down, is the
broken version above.

### `sim.run_bank`

The last signal after `closed` is set lets the tasks of idle servers end. Without it they wait
forever; `run` still stops, because tasks waiting for an event don't keep it going, and the report
is the same, so the hidden tests can't tell. In a trial, the model without that signal passed all
28. Read for it under Design: a task left waiting forever is a leak in a longer-running program.
The common failure that the tests do see is computing the mean with `//`, which floors it.

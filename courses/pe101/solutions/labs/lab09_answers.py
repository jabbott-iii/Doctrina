# %% tags=["answer-L9.1"]
def routed(router, workers, ticket):
    route = ask(router, ticket, "Return exactly repair or billing.")
    if route not in workers:
        raise ValueError("Unknown route.")
    return ask(workers[route], ticket, f"Handle the {route} queue.")

# %% tags=["answer-L9.2"]
def parallel(workers, ticket):
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {name: executor.submit(ask, worker, ticket) for name, worker in workers.items()}
        return {name: future.result() for name, future in futures.items()}

# %% tags=["answer-L9.3"]
def orchestrate(planner, workers, ticket):
    plan = json.loads(ask(planner, ticket))
    if (not isinstance(plan, list)
            or any(not isinstance(job, str) or job not in workers for job in plan)
            or len(plan) != len(set(plan))):
        raise ValueError("Invalid worker plan.")
    return {job: ask(workers[job], ticket) for job in plan}

# %% tags=["answer-L9.4"]
def optimize(draft, judge, ticket, max_drafts):
    feedback = ""
    for _ in range(max_drafts):
        proposal = ask(draft, f"{ticket}\n{feedback}")
        feedback = ask(judge, f"{ticket}\n{proposal}")
        if feedback == "pass":
            return proposal
    return None

# %% tags=["answer-L9.5"]
def agent(model, task, max_turns, budget, reserve):
    history = [{"role": "user", "content": task}]
    log = []
    spent = 0
    for turn in range(1, max_turns + 1):
        if spent + reserve > budget:
            return "cost_limit", None, log
        response = model({"messages": history, "tools": TOOLS, "max_tokens": reserve})
        used = response["usage"]["output_tokens"]
        if not 0 <= used <= reserve:
            raise ValueError("Scripted usage must fit the reserve.")
        spent += used
        reason = response["stop_reason"]
        blocks = response["content"]
        calls = [b for b in blocks if b["type"] == "tool_use"]
        log.append({"turn": turn, "used": used, "spent": spent,
                    "stop": reason, "tools": [b["name"] for b in calls]})
        if reason != "tool_use":
            return reason, text_of(response) if reason == "end_turn" else None, log
        if not calls:
            raise ValueError("A tool stop requires a proposal.")
        history.extend([{"role": "assistant", "content": blocks},
                        {"role": "user", "content": [run_tool(b) for b in calls]}])
    return "turn_limit", None, log

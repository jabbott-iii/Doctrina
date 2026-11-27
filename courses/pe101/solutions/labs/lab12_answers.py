# %% tags=["answer-L12.1"]
def decision_positions(turns):
    return [i for i, row in enumerate(turns)
            if row.get("event") == "model" and row.get("origin") == "tool_result"]

# %% tags=["answer-L12.2"]
def task_prompt(task):
    files = ", ".join(task["files"])
    constraints = " ".join(task["constraints"])
    return (f"{task['goal']} Work in {files}. {constraints} "
            f"Verify with {task['verification']}. Report altered files and the test result.")

# %% tags=["answer-L12.3"]
def check_package(path):
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-v"],
                          cwd=path, capture_output=True, text=True, check=False)
    return proc.returncode

# %% tags=["answer-L12.4"]
def reviews():
    return {"A": "accept", "B": "regression", "C": "out_of_scope"}

# %% tags=["answer-L13.1"]
def instructions():
    return {
        "CLAUDE.md": "# Project instructions\n\nUse integer cents. Run python -m unittest discover -v.",
        ".claude/rules/fixtures.md": (
            "---\npaths:\n  - \"data/**\"\n---\n\n# Fixture rules\n\nKeep each fixture ID stable."
        ),
    }

# %% tags=["answer-L13.2"]
def matches(path, pattern):
    path_parts = PurePosixPath(path).parts
    if pattern.endswith("/**"):
        prefix = PurePosixPath(pattern[:-3]).parts
        return len(path_parts) > len(prefix) and path_parts[:len(prefix)] == prefix
    return path_parts == PurePosixPath(pattern).parts

# %% tags=["answer-L13.3"]
def skill():
    return (
        "---\nname: review-labels\ndescription: \"Review bicycle-shop label changes and tests.\"\n"
        "---\n\n# Review labels\n\nInspect the diff. Run regression tests. Summarize evidence."
    )

# %% tags=["answer-L13.4"]
def settings():
    return {
        "permissions": {"allow": ["Bash(python -m unittest discover -v)"]},
        "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": 'python "$CLAUDE_PROJECT_DIR/.claude/hooks/review_command.py"'},
        ]}]},
    }

# %% tags=["answer-L13.5"]
def hook_source():
    return 'import json\nimport sys\n\ntry:\n    event = json.load(sys.stdin)\n    if not isinstance(event, dict):\n        raise ValueError("Expected a JSON object.")\n    tool_input = event.get("tool_input")\n    permitted = (\n        event.get("hook_event_name") == "PreToolUse"\n        and event.get("tool_name") == "Bash"\n        and isinstance(tool_input, dict)\n        and tool_input.get("command") == "python -m unittest discover -v"\n    )\nexcept (ValueError, TypeError):\n    permitted = False\n\nif not permitted:\n    print(json.dumps({"hookSpecificOutput": {\n        "hookEventName": "PreToolUse",\n        "permissionDecision": "deny",\n        "permissionDecisionReason": "Only the reviewed test command fits this lab.",\n    }}))'

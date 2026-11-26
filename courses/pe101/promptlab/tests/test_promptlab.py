"""Tests for promptlab: run them with ``pytest courses/pe101/promptlab``."""

import json

import pytest

import promptlab
from promptlab import data, standins


def test_make_response_has_the_messages_api_shape():
    response = promptlab.make_response("Hello!", input_tokens=12, output_tokens=6)
    assert set(response) == {
        "id", "type", "role", "model", "content", "stop_reason", "stop_sequence", "usage"
    }
    assert response["id"].startswith("msg_standin_")
    assert response["type"] == "message"
    assert response["role"] == "assistant"
    assert response["model"] == "claude-opus-5-5"
    assert response["content"] == [{"type": "text", "text": "Hello!"}]
    assert response["stop_reason"] == "end_turn"
    assert response["stop_sequence"] is None
    assert response["usage"] == {
        "input_tokens": 12,
        "output_tokens": 6,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


def test_each_response_gets_a_new_id():
    first = promptlab.make_response("a")
    second = promptlab.make_response("a")
    assert first["id"] != second["id"]


def test_output_tokens_default_to_the_rough_count_of_the_text():
    response = promptlab.make_response("x" * 10)
    assert response["usage"]["output_tokens"] == 4  # 10 / 2.5


def test_rough_token_count_rounds_up():
    assert promptlab.rough_token_count("") == 0
    assert promptlab.rough_token_count("abc") == 2  # 3 / 2.5 = 1.2


def test_make_response_rejects_an_unknown_stop_reason():
    with pytest.raises(ValueError, match="unknown stop reason"):
        promptlab.make_response("x", stop_reason="done")


def test_a_stop_sequence_needs_its_stop_reason():
    with pytest.raises(ValueError, match="stop_sequence"):
        promptlab.make_response("x", stop_sequence="END")
    response = promptlab.make_response("x", stop_reason="stop_sequence", stop_sequence="END")
    assert response["stop_sequence"] == "END"


def test_a_refusal_carries_its_stop_details():
    details = {"type": "refusal"}
    response = promptlab.make_response("", stop_reason="refusal", stop_details=details)
    assert response["stop_details"] == details
    details["type"] = "changed"
    assert response["stop_details"] == {"type": "refusal"}, "the response keeps its own copy"


def test_make_response_accepts_content_blocks():
    blocks = [{"type": "text", "text": "a"}, {"type": "text", "text": "bcd"}]
    response = promptlab.make_response(blocks)
    assert response["content"] == blocks
    assert response["content"] is not blocks
    assert response["usage"]["output_tokens"] == 2  # "abcd": 4 / 2.5, rounded up


def test_scripted_model_answers_in_order_and_records_requests():
    model = promptlab.ScriptedModel(["first", "second"])
    request = {"model": "claude-haiku-5-5", "max_tokens": 50,
               "messages": [{"role": "user", "content": "Say hi"}]}
    first = model(request)
    request["messages"].append({"role": "assistant", "content": "changed later"})
    second = model({"model": "claude-haiku-5-5", "max_tokens": 50, "messages": []})
    assert first["content"][0]["text"] == "first"
    assert second["content"][0]["text"] == "second"
    assert first["model"] == "claude-haiku-5-5", "a reply names the requested model"
    assert model.calls == 2
    assert len(model.requests[0]["messages"]) == 1, "the model records a copy of each request"


def test_scripted_model_counts_input_tokens_from_the_request():
    model = promptlab.ScriptedModel(["ok"])
    response = model({"system": "x" * 5,
                      "messages": [{"role": "user", "content": [{"type": "text", "text": "y" * 4}]}]})
    # The text is "xxxxx\nyyyy": 10 characters, so 4 tokens at 2.5 characters each.
    assert response["usage"]["input_tokens"] == 4


def test_scripted_model_raises_when_the_script_runs_out():
    model = promptlab.ScriptedModel(["only one"])
    model({"messages": []})
    with pytest.raises(promptlab.ScriptExhausted, match="request 2"):
        model({"messages": []})
    assert model.calls == 2


def test_scripted_model_returns_copies_of_whole_responses():
    whole = promptlab.make_response("cut off", stop_reason="max_tokens")
    model = promptlab.ScriptedModel([whole, whole])
    first = model({"messages": []})
    first["content"][0]["text"] = "edited"
    assert model({"messages": []})["content"][0]["text"] == "cut off"


def test_scripted_model_calls_functions_with_the_request():
    def echo(request):
        return request["messages"][-1]["content"].upper()

    model = promptlab.ScriptedModel([echo])
    response = model({"messages": [{"role": "user", "content": "loud"}]})
    assert response["content"][0]["text"] == "LOUD"


def test_stop_reasons_match_the_documented_list():
    assert standins.STOP_REASONS == (
        "end_turn", "max_tokens", "stop_sequence", "tool_use", "pause_turn", "refusal",
        "model_context_window_exceeded",
    )


@pytest.fixture
def fake_data(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "DATA", tmp_path)
    return tmp_path


def test_load_json_and_jsonl(fake_data):
    (fake_data / "prices.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    (fake_data / "rows.jsonl").write_text('{"n": 1}\n\n{"n": 2}\n', encoding="utf-8")
    assert promptlab.load_json("prices.json") == {"a": 1}
    assert promptlab.load_jsonl("rows.jsonl") == [{"n": 1}, {"n": 2}]


def test_load_jsonl_names_the_bad_line(fake_data):
    (fake_data / "bad.jsonl").write_text('{"n": 1}\n{"n": \n', encoding="utf-8")
    with pytest.raises(ValueError, match="bad.jsonl, line 2"):
        promptlab.load_jsonl("bad.jsonl")


def test_data_path_names_the_folder_when_a_file_is_missing(fake_data):
    with pytest.raises(FileNotFoundError, match="no data file 'missing.json'"):
        promptlab.data_path("missing.json")


def test_the_data_folder_is_the_courses_own():
    assert data.DATA.parts[-3:] == ("courses", "pe101", "data")

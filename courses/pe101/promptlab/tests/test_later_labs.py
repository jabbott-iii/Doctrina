import json
from math import isclose

import pytest

from promptlab.evaluation import paired_bootstrap, wilson
from promptlab.retrieval import bm25
from promptlab.review import GullibleModel, classify
from promptlab.shop_tools import run_tool


def test_wilson_endpoints_and_small_sample():
    low, high = wilson(8, 10)
    assert isclose(low, 0.490, abs_tol=0.001)
    assert isclose(high, 0.943, abs_tol=0.001)
    assert isclose(wilson(0, 8)[0], 0, abs_tol=1e-12)
    assert isclose(wilson(8, 8)[1], 1, abs_tol=1e-12)
    with pytest.raises(ValueError):
        wilson(2, 1)


def test_both_versions_move_together_in_paired_bootstrap():
    a = [0.3, 0.7, 0.2, 0.4]
    assert paired_bootstrap(a, a) == (0, 0, 0)
    result = paired_bootstrap(a, [1, 0.9, 0, 0], repeats=500, seed=17)
    assert result[1] < result[0] < result[2]
    assert result == paired_bootstrap(a, [1, 0.9, 0, 0], repeats=500, seed=17)
    with pytest.raises(ValueError):
        paired_bootstrap(a, [0])


def test_bm25_id_order_and_repeated_query_terms():
    docs = [{"id": "C", "text": "cable"},
            {"id": "A", "text": "chain"},
            {"id": "B", "text": "cable"}]
    ranked = bm25("cable", docs)
    assert [ident for ident, _ in ranked] == ["B", "C", "A"]
    assert ranked[0][1] == ranked[1][1] > ranked[2][1] == 0
    assert bm25("cable CABLE", docs) == ranked
    assert bm25("cable", []) == []


def test_local_tool_uses_schema_and_domain_checks():
    block = {"id": "bench", "name": "estimate_minutes", "input": {"service": "flat"}}
    result = run_tool(block)
    assert result["tool_use_id"] == "bench"
    assert json.loads(result["content"]) == {"value": 25}
    for proposal in (dict(block, name="unknown"),
                     dict(block, input={"service": "unknown"}),
                     dict(block, input={"service": "flat", "question": "?"})):
        result = run_tool(proposal)
        assert result["tool_use_id"] == "bench"
        assert result["is_error"] is True


def test_inert_proposal_fixture_preserves_source_and_replays_a_copy():
    model = GullibleModel()
    case = {"origin": "document", "proposed": {"name": "change_label", "label": "sample"}}
    assert classify(case) == "indirect"
    assert classify(dict(case, origin="user")) == "direct"
    proposal = model(case)
    assert proposal == case["proposed"]
    proposal["name"] = "read_label"
    assert model(case)["name"] == "change_label"

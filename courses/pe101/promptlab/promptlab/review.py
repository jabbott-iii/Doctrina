"""Inert proposals for checking a fictitious action policy.

No real command, file edit, external message, or tool dispatch is available here.
"""

class GullibleModel:
    """Replay a pre-written proposal from a case, regardless of its origin."""

    def __call__(self, case):
        return dict(case["proposed"])


def classify(case):
    """Return the abstract trust-boundary category of a fixture."""
    return "direct" if case["origin"] == "user" else "indirect"

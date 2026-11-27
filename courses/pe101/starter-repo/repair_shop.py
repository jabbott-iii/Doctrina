"""Small bicycle-shop functions for PE101's coding-agent exercises."""


def repair_total(labor_cents, part_cents):
    """Return the invoice total in integer cents."""
    return labor_cents + sum(part_cents)


def estimate_minutes(services):
    """Return posted bench-time estimates for service names."""
    rates = {"flat": 25, "brakes": 40, "inspection": 15}
    return sum(rates[name] for name in services)


def service_label(name):
    """Return the customer-facing service label."""
    return name.replace("_", " ").title()

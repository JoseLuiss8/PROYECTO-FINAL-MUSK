from typing import Any, cast

from src.analyze import generate_report


def test_calculations_values() -> None:
    report: dict[str, object] = generate_report()
    summary: dict[str, Any] = cast(dict[str, Any], report["summary"])
    assert summary["total_clients"] == 3
    assert summary["total_sales"] == 7
    assert summary["total_revenue"] > 0
from src.sale import Sale


def test_sale_creation() -> None:
    s: Sale = Sale(1, 1, "Laptop", "Electronics", 999.99, "2023-01-01")
    assert s.client_id == 1
    assert s.amount == 999.99
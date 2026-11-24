from src.client import Client
from src.client_collection import ClientCollection
from src.sale import Sale
from src.sales_collection import SalesCollection


def test_collections() -> None:
    c: ClientCollection = ClientCollection([Client(1, "Alice", "Spain", "2022-01-01")])
    s: SalesCollection = SalesCollection([Sale(1, 1, "Laptop", "Electronics", 100, "2023-01-01")])

    client: Client | None = c.get_client_by_id(1)
    assert client is not None
    assert client.name == "Alice"
    assert len(s.sales_by_client(1)) == 1
    assert s.total_amount_by_client(1) == 100

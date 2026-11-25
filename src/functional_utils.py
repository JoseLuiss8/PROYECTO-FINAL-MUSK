from functools import reduce
from typing import Any


def filter_by_key(
    records: list[dict[str, Any]], key: str, value: Any
) -> list[dict[str, Any]]:
    """Devuelve una nueva lista con los registros donde records[key] == value."""
    filtered: filter[dict[str, Any]] = filter(
        lambda r: r.get(key) == value, records
    )
    return list(filtered)


def filter_by_date_range(
    records: list[dict[str, Any]], date_key: str, start_date: Any, end_date: Any
) -> list[dict[str, Any]]:
    """Filtra registros con fecha dentro de [start_date, end_date]."""
    filtered: filter[dict[str, Any]] = filter(
        lambda r: r.get(date_key) is not None
        and start_date <= r.get(date_key) <= end_date,
        records,
    )
    return list(filtered)


def extract_field(records: list[dict[str, Any]], field: str) -> list[Any]:
    """Devuelve una nueva lista con el valor de `field` para cada registro."""
    mapped: map[Any] = map(lambda r: r.get(field), records)
    return list(mapped)


def _apply_discount(
    record: dict[str, Any], price_key: str, factor: float
) -> dict[str, Any]:
    raw_price: Any = record.get(price_key, 0.0)
    numeric_price: float = float(raw_price) if raw_price is not None else 0.0
    discounted: float = round(numeric_price * factor, 2)
    updated: dict[str, Any] = {**record, "discounted_price": discounted}
    return updated


def add_discounted_price(
    records: list[dict[str, Any]],
    price_key: str = "price",
    discount: float = 0.1,
) -> list[dict[str, Any]]:
    """Devuelve una nueva lista de diccionarios con `discounted_price` sin mutar el original."""
    factor: float = max(0.0, 1.0 - float(discount))
    mapped: map[dict[str, Any]] = map(
        lambda r: _apply_discount(r, price_key, factor),
        records,
    )
    return list(mapped)


def sum_numeric_field(
    records: list[dict[str, Any]], field: str, initial: float = 0.0
) -> float:
    """Acumula un campo numérico usando reduce sin modificar `records`."""
    def _add(acc: float, r: dict[str, Any]) -> float:
        raw_val: Any = r.get(field, 0.0)
        val: float = float(raw_val) if raw_val is not None else 0.0
        return acc + val

    return reduce(_add, records, float(initial))


def group_counts_by_key(
    records: list[dict[str, Any]], key: str
) -> dict[Any, int]:
    """Devuelve un nuevo diccionario con el recuento de apariciones de cada valor de `key`."""
    def _step(acc: dict[Any, int], r: dict[str, Any]) -> dict[Any, int]:
        k: Any = r.get(key)
        current_count: int = acc.get(k, 0)
        return {**acc, k: current_count + 1}

    return reduce(_step, records, {})
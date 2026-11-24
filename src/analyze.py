import json
import os
from typing import Any, cast

import pandas as pd

from src.client import Client
from src.client_collection import ClientCollection
from src.sale import Sale
from src.sales_collection import SalesCollection


class SalesAnalyzer:
    def __init__(self, clients_path: str = "data/clients.json", sales_path: str = "data/sales.csv") -> None:
        self.clients_collection: ClientCollection = self._load_clients(clients_path)
        self.sales_collection: SalesCollection = self._load_sales(sales_path)

    def _load_clients(self, path: str) -> ClientCollection:
        """Carga los clientes desde el JSON y devuelve una ClientCollection."""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                raw_data: Any = json.load(f)
            data: list[dict[str, Any]] = cast(list[dict[str, Any]], raw_data)
            clients_list: list[Client] = [
                Client(
                    client_id=int(item["client_id"]),
                    name=str(item["name"]),
                    country=str(item["country"]),
                    signup_date=str(item["signup_date"]),
                )
                for item in data
            ]
            return ClientCollection(clients_list)
        return ClientCollection([])

    def _load_sales(self, path: str) -> SalesCollection:
        """Carga las ventas desde el CSV usando Pandas y devuelve una SalesCollection."""
        if os.path.exists(path):
            df: pd.DataFrame = pd.read_csv(path)
            sales_list: list[Sale] = [
                Sale(
                    sale_id=str(row["sale_id"]),
                    client_id=int(row["client_id"]),
                    product=str(row["product"]),
                    category=str(row["category"]),
                    amount=float(row["amount"]),
                    date=str(row["date"]),
                )
                for _, row in df.iterrows()
            ]
            return SalesCollection(sales_list)
        return SalesCollection([])

    # --- CÁLCULOS 1 AL 5 ---

    def total_clients_count(self) -> int:
        """1. Número total de clientes: Cuenta cuántos clientes hay en el JSON."""
        return len(self.clients_collection.clients)

    def total_sales_count(self) -> int:
        """2. Número total de ventas: Tamaño del CSV de ventas."""
        return len(self.sales_collection.sales)

    def total_income_by_client(self) -> dict[int, float]:
        """3. Total de ingresos por cliente: Filtra ventas por client_id y suma amounts."""
        result: dict[int, float] = {}
        for client in self.clients_collection.clients:
            total: float = self.sales_collection.total_amount_by_client(client.client_id)
            result[client.client_id] = total
        return result

    def sales_count_by_client(self) -> dict[int, int]:
        """4. Número de ventas por cliente: Longitud de sales_by_client(id)."""
        result: dict[int, int] = {}
        for client in self.clients_collection.clients:
            sales_list: list[Sale] = self.sales_collection.sales_by_client(client.client_id)
            result[client.client_id] = len(sales_list)
        return result

    def average_sale_by_client(self) -> dict[int, float]:
        """5. Ingreso promedio por venta de cada cliente."""
        result: dict[int, float] = {}
        for client in self.clients_collection.clients:
            avg: float = self.sales_collection.average_sale_by_client(client.client_id)
            result[client.client_id] = avg
        return result

    # --- CÁLCULOS 6 AL 10 ---

    def top_client_by_country(self, country: str) -> Client | None:
        """6. Cliente con mayor gasto por país: Cruza clientes y ventas filtrando por país."""
        country_clients: list[Client] = self.clients_collection.clients_by_country(country)
        if not country_clients:
            return None

        top_client: Client | None = None
        max_spent: float = -1.0
        for client in country_clients:
            spent: float = self.sales_collection.total_amount_by_client(client.client_id)
            if spent > max_spent:
                max_spent = spent
                top_client = client
        return top_client

    def total_sales_by_category(self) -> dict[str, float]:
        """7. Total de ventas por categoría usando Pandas."""
        if self.sales_collection.sales:
            df: pd.DataFrame = pd.DataFrame([s.to_dict() for s in self.sales_collection.sales])
            grouped: dict[Any, Any] = df.groupby("category")["amount"].sum().to_dict()
            return {str(k): float(v) for k, v in grouped.items()}
        return {}

    def top_client_by_category(self, category: str) -> Client | None:
        """8. Cliente con más ventas (número de transacciones) en una categoría específica."""
        category_sales: list[Sale] = [
            s for s in self.sales_collection.sales if s.category.lower() == category.lower()
        ]
        if not category_sales:
            return None

        client_counts: dict[int, int] = {}
        for sale in category_sales:
            client_counts[sale.client_id] = client_counts.get(sale.client_id, 0) + 1

        if not client_counts:
            return None

        top_client_id: int = max(client_counts, key=lambda cid: client_counts[cid])
        return self.clients_collection.get_client_by_id(top_client_id)

    def clients_above_minimum_spend(self, min_spend: float) -> int:
        """9. Número de clientes que superan un gasto mínimo."""
        count: int = 0
        for client in self.clients_collection.clients:
            total: float = self.sales_collection.total_amount_by_client(client.client_id)
            if total >= min_spend:
                count += 1
        return count

    def monthly_accumulated_sales(self) -> dict[str, float]:
        """10. Ventas acumuladas mes a mes usando Pandas."""
        if self.sales_collection.sales:
            df: pd.DataFrame = pd.DataFrame([s.to_dict() for s in self.sales_collection.sales])
            df["date"] = pd.to_datetime(df["date"])
            df["year_month"] = df["date"].dt.to_period("M")
            monthly = df.groupby("year_month")["amount"].sum()
            return {str(k): float(v) for k, v in monthly.items()}
        return {}


def generate_report() -> dict[str, object]:
    """Función global requerida por los tests para generar y estructurar todo el informe."""
    analyzer: SalesAnalyzer = SalesAnalyzer()

    clients_data: list[dict[str, object]] = []
    for client in analyzer.clients_collection.clients:
        total_spent: float = analyzer.sales_collection.total_amount_by_client(client.client_id)
        sale_count: int = len(analyzer.sales_collection.sales_by_client(client.client_id))
        average_sale: float = round(total_spent / sale_count, 2) if sale_count > 0 else 0.0

        clients_data.append({
            "client_id": client.client_id,
            "name": client.name,
            "country": client.country,
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale,
        })

    countries: set[str] = {c.country for c in analyzer.clients_collection.clients}
    top_by_country: dict[str, str] = {}
    for country in countries:
        top_client: Client | None = analyzer.top_client_by_country(country)
        if top_client:
            top_by_country[country] = top_client.name

    high_spenders: list[str] = []
    for client in analyzer.clients_collection.clients:
        total: float = analyzer.sales_collection.total_amount_by_client(client.client_id)
        if total > 500:
            high_spenders.append(client.name)

    total_revenue: float = sum(
        analyzer.sales_collection.total_amount_by_client(c.client_id)
        for c in analyzer.clients_collection.clients
    )

    report: dict[str, object] = {
        "summary": {
            "total_clients": analyzer.total_clients_count(),
            "total_sales": analyzer.total_sales_count(),
            "total_revenue": total_revenue,
        },
        "clients": clients_data,
        "top_client_by_country": top_by_country,
        "sales_by_category": analyzer.total_sales_by_category(),
        "high_spending_clients": high_spenders,
        "monthly_sales": analyzer.monthly_accumulated_sales(),
    }

    return report


if __name__ == "__main__":
    analyzer = SalesAnalyzer()
    print("¡Analizador inicializado con éxito y los 10 cálculos listos!")
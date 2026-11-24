
from src.sale import Sale

class SalesCollection:
    def __init__(self, sales: list[Sale] | None = None):
        # Inicializa la colección con una lista de objetos Sale
        self.sales = sales if sales is not None else []

    def get_sale_by_id(self, sale_id: int) -> Sale | None:
        """Devuelve un objeto Sale concreto buscando por su identificador único."""
        for sale in self.sales:
            if sale.sale_id == sale_id:
                return sale
        return None

    def sales_by_client(self, client_id: int) -> list[Sale]:
        """Devuelve todas las ventas de un cliente específico."""
        return [sale for sale in self.sales if sale.client_id == client_id]

    def total_amount_by_client(self, client_id: int) -> float:
        """Calcula la suma de importes de las ventas de un cliente."""
        client_sales = self.sales_by_client(client_id)
        return sum(sale.amount for sale in client_sales)

    def total_amount_by_category(self, category: str) -> float:
        """Calcula la suma total de ventas de una categoría."""
        return sum(sale.amount for sale in self.sales if sale.category.lower() == category.lower())

    def average_sale_by_client(self, client_id: int) -> float:
        """Calcula la media de gasto por venta para un cliente."""
        client_sales = self.sales_by_client(client_id)
        if not client_sales:
            return 0.0
        return self.total_amount_by_client(client_id) / len(client_sales)
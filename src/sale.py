class Sale:
    def __init__(
        self,
        sale_id: int | str,
        client_id: int,
        product: str,
        category: str,
        amount: float,
        date: str,
    ) -> None:
        self.sale_id: int | str = sale_id
        self.client_id: int = client_id
        self.product: str = product
        self.category: str = category
        self.amount: float = amount
        self.date: str = date

    def to_dict(self) -> dict[str, int | float | str]:
        """Convierte el objeto venta a un diccionario de Python para facilitar su serialización."""
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
        }

    def __str__(self) -> str:
        return f"Venta {self.sale_id} - {self.product} ({self.amount}€)"
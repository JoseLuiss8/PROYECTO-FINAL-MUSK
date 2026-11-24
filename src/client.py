
class Client:
    def __init__(self, client_id: int, name: str, country: str, signup_date: str):
        self.client_id = client_id
        self.name = name
        self.country = country
        self.signup_date = signup_date

    def to_dict(self) -> dict[str, int | str]:
        """Convierte el objeto cliente a un diccionario de Python para exportarlo como JSON."""
        return {
            "client_id": self.client_id,
            "name": self.name,
            "country": self.country,
            "signup_date": self.signup_date
        }

    def __str__(self):
        return f"Cliente {self.client_id} - {self.name} ({self.country})"
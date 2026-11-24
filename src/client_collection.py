
from src.client import Client

class ClientCollection:
    def __init__(self, clients: list[Client] | None = None):
        # Guardamos la lista de clientes (si no se pasa nada, arrancamos con una lista vacía)
        self.clients = clients if clients is not None else []

    def get_client_by_id(self, client_id: int) -> Client | None:
        """Devuelve un objeto Client concreto buscando por su identificador único."""
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def clients_by_country(self, country: str) -> list[Client]:
        """Devuelve una lista con todos los clientes que pertenecen a un país determinado."""
        return [client for client in self.clients if client.country.lower() == country.lower()]
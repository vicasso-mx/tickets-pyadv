"""Repositorio de tickets respaldado por un diccionario en memoria."""


class RepositorioMemoria:
    def __init__(self):
        self._tickets = {}

    def agregar(self, ticket):
        if ticket.folio in self._tickets:
            raise ValueError(f"Ya existe un ticket con folio {ticket.folio}.")
        self._tickets[ticket.folio] = ticket
        return ticket

    def buscar(self, folio):
        return self._tickets.get(folio)

    def listar(self):
        return tuple(self._tickets.values())

    def __len__(self):
        return len(self._tickets)

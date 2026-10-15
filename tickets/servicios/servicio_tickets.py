"""Coordinación de los casos de uso para tickets."""

from tickets.dominio.ticket import Ticket, TicketDesarrollo, TicketInfraestructura, TicketSoporte
from tickets.dominio.validaciones import folio_valido
from tickets.almacenamiento.repositorio_memoria import RepositorioMemoria


class ServicioTickets:
    """Aplica reglas de uso y coordina modelo y repositorio."""

    _clases_por_tipo = {
        "soporte": TicketSoporte,
        "desarrollo": TicketDesarrollo,
        "infraestructura": TicketInfraestructura,
    }

    def __init__(self, repositorio=None):
        self._repositorio = repositorio or RepositorioMemoria()

    def crear_ticket(self, folio, titulo, descripcion, tipo="soporte"):
        if not folio_valido(folio):
            raise ValueError(f"Folio no válido: {folio}. Formato esperado: TK-001 o TK001.")
        if self._repositorio.buscar(folio) is not None:
            raise ValueError(f"Ya existe un ticket con folio {folio}.")
        clase = self._clases_por_tipo.get(tipo)
        if clase is None:
            raise ValueError(f"Tipo no válido: {tipo}.")
        ticket = clase(folio, titulo, descripcion)
        self._repositorio.agregar(ticket)
        return ticket

    def consultar_ticket(self, folio):
        ticket = self._repositorio.buscar(folio)
        if ticket is None:
            raise LookupError(f"No existe un ticket con folio {folio}.")
        return ticket

    def listar_tickets(self, estado=None, tipo=None):
        tickets = self._repositorio.listar()
        if estado is not None:
            tickets = [ticket for ticket in tickets if ticket.estado == estado]
        if tipo is not None:
            tickets = [ticket for ticket in tickets if ticket.tipo == tipo]
        return tickets

    def atender_ticket(self, folio):
        return self.consultar_ticket(folio).atender()

    def actualizar_estado(self, folio, nuevo_estado):
        return self.consultar_ticket(folio).cambiar_estado(nuevo_estado)

    def ordenar_por_folio(self):
        return sorted(self._repositorio.listar(), key=lambda ticket: ticket.folio)

    @staticmethod
    def total_tickets_creados():
        return Ticket.total_tickets_creados()

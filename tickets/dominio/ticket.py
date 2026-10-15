"""Entidades de ticket y operaciones permitidas sobre ellas."""

from datetime import datetime

from tickets.dominio.estados import ESTADOS_VALIDOS, TRANSICIONES_PERMITIDAS, TIPOS_VALIDOS
from tickets.dominio.validaciones import texto_requerido_valido
from tickets.utilidades.decoradores import validar_folio


class Ticket:
    """Ticket encapsulado, con historial de cambios de estado."""

    ESTADOS_VALIDOS = ESTADOS_VALIDOS
    _contador_global = 0

    @validar_folio
    def __init__(self, folio, titulo, descripcion, tipo="soporte"):
        if not texto_requerido_valido(titulo):
            raise ValueError("El título no puede estar vacío.")
        if not texto_requerido_valido(descripcion):
            raise ValueError("La descripción no puede estar vacía.")
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo no válido: {tipo}.")

        self._folio = folio
        self._titulo = titulo.strip()
        self._descripcion = descripcion.strip()
        self._tipo = tipo
        self._estado = "Abierto"
        self._historial = []
        Ticket._contador_global += 1
        self._registrar_evento("crear", None, self._estado)

    @property
    def folio(self):
        return self._folio

    @property
    def titulo(self):
        return self._titulo

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def tipo(self):
        return self._tipo

    @property
    def estado(self):
        return self._estado

    @property
    def historial(self):
        return tuple(dict(evento) for evento in self._historial)

    def _registrar_evento(self, accion, anterior, nuevo):
        self._historial.append({
            "fecha_hora": datetime.now().isoformat(timespec="seconds"),
            "folio": self._folio,
            "accion": accion,
            "estado_anterior": anterior,
            "estado_nuevo": nuevo,
        })

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado no válido: {nuevo_estado}.")
        if nuevo_estado == self._estado:
            return False
        if nuevo_estado not in TRANSICIONES_PERMITIDAS[self._estado]:
            raise ValueError(f"No se permite cambiar de {self._estado} a {nuevo_estado}.")
        anterior = self._estado
        self._estado = nuevo_estado
        self._registrar_evento("cambiar_estado", anterior, nuevo_estado)
        return True

    def atender(self):
        if self._estado == "Cerrado":
            raise ValueError("No se puede atender un ticket cerrado.")
        cambio = self.cambiar_estado("En proceso")
        return cambio

    @classmethod
    def total_tickets_creados(cls):
        return Ticket._contador_global

    def __str__(self):
        return f"{self.__class__.__name__} | Folio: {self.folio} | Título: {self.titulo} | Estado: {self.estado}"


class TicketSoporte(Ticket):
    def __init__(self, folio, titulo, descripcion):
        super().__init__(folio, titulo, descripcion, "soporte")


class TicketDesarrollo(Ticket):
    def __init__(self, folio, titulo, descripcion):
        super().__init__(folio, titulo, descripcion, "desarrollo")


class TicketInfraestructura(Ticket):
    def __init__(self, folio, titulo, descripcion):
        super().__init__(folio, titulo, descripcion, "infraestructura")

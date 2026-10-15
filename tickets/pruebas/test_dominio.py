import unittest

from tickets.dominio.ticket import Ticket, TicketSoporte
from tickets.dominio.validaciones import folio_valido


class PruebasDominio(unittest.TestCase):
    def test_folios_validos_e_invalidos(self):
        self.assertTrue(folio_valido("TK-123"))
        self.assertTrue(folio_valido("TK123"))
        self.assertFalse(folio_valido("TK-12"))
        self.assertFalse(folio_valido("ABC-123"))

    def test_creacion_y_encapsulamiento(self):
        ticket = TicketSoporte("TK-101", "Acceso", "No inicia sesión")
        self.assertEqual(ticket.estado, "Abierto")
        self.assertEqual(len(ticket.historial), 1)
        with self.assertRaises(AttributeError):
            ticket.estado = "Cerrado"

    def test_transiciones_y_cierre(self):
        ticket = Ticket("TK-102", "Error", "Falla reportada")
        self.assertTrue(ticket.atender())
        self.assertEqual(ticket.estado, "En proceso")
        self.assertTrue(ticket.cambiar_estado("Cerrado"))
        with self.assertRaises(ValueError):
            ticket.atender()

    def test_rechaza_datos_invalidos(self):
        with self.assertRaises(ValueError):
            Ticket("TK-1", "Título", "Descripción")
        with self.assertRaises(ValueError):
            Ticket("TK-103", " ", "Descripción")


if __name__ == "__main__":
    unittest.main()

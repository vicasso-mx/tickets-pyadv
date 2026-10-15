import unittest

from tickets.servicios.servicio_tickets import ServicioTickets


class PruebasServicio(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioTickets()

    def test_crear_consultar_y_filtrar(self):
        ticket = self.servicio.crear_ticket("TK-201", "Red", "Sin conexión", "infraestructura")
        self.assertIs(self.servicio.consultar_ticket("TK-201"), ticket)
        self.assertEqual(self.servicio.listar_tickets(tipo="infraestructura"), [ticket])

    def test_folio_duplicado_e_inexistente(self):
        self.servicio.crear_ticket("TK-202", "Uno", "Detalle")
        with self.assertRaises(ValueError):
            self.servicio.crear_ticket("TK-202", "Dos", "Detalle")
        with self.assertRaises(LookupError):
            self.servicio.consultar_ticket("TK-999")

    def test_atender_y_actualizar(self):
        self.servicio.crear_ticket("TK-203", "Uno", "Detalle")
        self.servicio.atender_ticket("TK-203")
        self.servicio.actualizar_estado("TK-203", "Cerrado")
        self.assertEqual(self.servicio.consultar_ticket("TK-203").estado, "Cerrado")


if __name__ == "__main__":
    unittest.main()

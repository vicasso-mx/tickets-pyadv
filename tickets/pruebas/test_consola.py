import unittest

from tickets.consola.menu import ejecutar_menu
from tickets.servicios.servicio_tickets import ServicioTickets


class PruebasConsola(unittest.TestCase):
    def test_opcion_incorrecta_no_termina_el_menu(self):
        entradas = iter(["x", "0"])
        mensajes = []
        ejecutar_menu(ServicioTickets(), entrada=lambda _: next(entradas), salida=mensajes.append)
        self.assertTrue(any("Opción incorrecta" in mensaje for mensaje in mensajes))


if __name__ == "__main__":
    unittest.main()

"""Punto de entrada: python -m tickets."""

from tickets.consola.menu import ejecutar_menu
from tickets.servicios.servicio_tickets import ServicioTickets


def main():
    ejecutar_menu(ServicioTickets())


if __name__ == "__main__":
    main()

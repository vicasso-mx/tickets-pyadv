"""Menú de consola para operaciones básicas de tickets."""


def ejecutar_menu(servicio, entrada=input, salida=print):
    while True:
        salida("\n=== GESTIÓN DE TICKETS ===")
        salida("1. Crear ticket")
        salida("2. Consultar ticket")
        salida("3. Listar tickets")
        salida("4. Atender ticket")
        salida("5. Actualizar estado")
        salida("0. Salir")
        opcion = entrada("Opción: ").strip()

        try:
            if opcion == "0":
                salida("Hasta luego.")
                return
            if opcion == "1":
                folio = entrada("Folio (TK-001 o TK001): ").strip()
                titulo = entrada("Título: ")
                descripcion = entrada("Descripción: ")
                tipo = entrada("Tipo (soporte/desarrollo/infraestructura): ").strip().lower()
                salida(f"Creado: {servicio.crear_ticket(folio, titulo, descripcion, tipo)}")
            elif opcion == "2":
                salida(str(servicio.consultar_ticket(entrada("Folio: ").strip())))
            elif opcion == "3":
                tickets = servicio.ordenar_por_folio()
                if not tickets:
                    salida("No hay tickets registrados.")
                for ticket in tickets:
                    salida(str(ticket))
            elif opcion == "4":
                folio = entrada("Folio: ").strip()
                servicio.atender_ticket(folio)
                salida(f"Ticket {folio} atendido y marcado En proceso.")
            elif opcion == "5":
                folio = entrada("Folio: ").strip()
                estado = entrada("Nuevo estado (Abierto/En proceso/Cerrado): ").strip()
                cambio = servicio.actualizar_estado(folio, estado)
                salida("Estado actualizado." if cambio else "El ticket ya tenía ese estado.")
            else:
                salida("Opción incorrecta. Intenta de nuevo.")
        except (ValueError, LookupError) as error:
            salida(f"Error: {error}")

"""Decoradores aplicados a operaciones del dominio."""

from functools import wraps

from tickets.dominio.validaciones import folio_valido


def validar_folio(funcion):
    """Valida el primer argumento llamado folio mediante la regla regex."""
    @wraps(funcion)
    def envoltura(self, folio, *args, **kwargs):
        if not folio_valido(folio):
            raise ValueError(f"Folio no válido: {folio}. Formato esperado: TK-001 o TK001.")
        return funcion(self, folio, *args, **kwargs)
    return envoltura

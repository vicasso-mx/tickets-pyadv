"""Validaciones puras del dominio."""

import re

PATRON_FOLIO = r"TK-?\d{3}"


def folio_valido(folio):
    """Indica si el folio cumple el formato TK-999 o TK999."""
    return isinstance(folio, str) and re.fullmatch(PATRON_FOLIO, folio) is not None


def texto_requerido_valido(valor):
    """Indica si el valor es texto no vacío después de quitar espacios."""
    return isinstance(valor, str) and bool(valor.strip())

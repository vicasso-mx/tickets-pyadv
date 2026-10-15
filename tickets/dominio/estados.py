"""Estados y transiciones admitidas para un ticket."""

ESTADOS_VALIDOS = ("Abierto", "En proceso", "Cerrado")
TRANSICIONES_PERMITIDAS = {
    "Abierto": ("En proceso", "Cerrado"),
    "En proceso": ("Cerrado",),
    "Cerrado": (),
}
TIPOS_VALIDOS = ("soporte", "desarrollo", "infraestructura")

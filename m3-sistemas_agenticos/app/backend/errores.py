"""Utilidad compartida para convertir errores de Pydantic en mensajes en español."""
from typing import Protocol

_PREFIJO_ERROR_VALOR = "Value error, "


class _ErrorConLista(Protocol):
    def errors(self) -> list[dict]: ...


def primer_mensaje(error: _ErrorConLista) -> str:
    mensaje = error.errors()[0]["msg"]
    if mensaje.startswith(_PREFIJO_ERROR_VALOR):
        mensaje = mensaje[len(_PREFIJO_ERROR_VALOR):]
    return mensaje

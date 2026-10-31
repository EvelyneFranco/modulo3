"""Fixtures compartidas para las pruebas de la aplicación."""
import os
import sqlite3
from collections.abc import Callable

import pytest

URL_API_POR_DEFECTO = "http://localhost:8000"
URL_WEB_POR_DEFECTO = "http://localhost:8080"
RUTA_BD = os.path.join(os.path.dirname(__file__), "..", "backend", "datos", "empleados.db")


@pytest.fixture
def url_api() -> str:
    return os.environ.get("URL_API", URL_API_POR_DEFECTO)


@pytest.fixture
def url_web() -> str:
    return os.environ.get("URL_WEB", URL_WEB_POR_DEFECTO)


@pytest.fixture
def marcar_baja() -> Callable[[str, str], None]:
    """Da de baja a un empleado escribiendo directo en la base de datos.

    HU-02 todavía no expone un endpoint para dar de baja a un empleado
    (esa acción corresponde a una historia futura), así que los casos que
    necesitan un empleado con estado "baja" como precondición preparan
    ese estado aquí en lugar de a través de la API.
    """

    def _marcar(correo: str, fecha_baja: str) -> None:
        conexion = sqlite3.connect(RUTA_BD)
        try:
            conexion.execute(
                "UPDATE empleados SET estado = 'baja', fecha_baja = ? "
                "WHERE lower(correo) = lower(?)",
                (fecha_baja, correo),
            )
            conexion.commit()
        finally:
            conexion.close()

    return _marcar

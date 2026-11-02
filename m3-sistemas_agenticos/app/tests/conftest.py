"""Fixtures compartidas para las pruebas de la aplicación."""
import os
from collections.abc import Callable

import httpx
import pytest

URL_API_POR_DEFECTO = "http://localhost:8000"
URL_WEB_POR_DEFECTO = "http://localhost:8080"


@pytest.fixture
def url_api() -> str:
    return os.environ.get("URL_API", URL_API_POR_DEFECTO)


@pytest.fixture
def url_web() -> str:
    return os.environ.get("URL_WEB", URL_WEB_POR_DEFECTO)


@pytest.fixture
def marcar_baja(url_api: str) -> Callable[[int, str], httpx.Response]:
    """Da de baja a un empleado usando el endpoint de la API.

    HU-03 ya expone POST /api/empleados/{id}/baja, así que las historias
    que necesitan un empleado con estado "baja" como precondición lo logran
    a través de la API en lugar de tocar la base de datos directamente.
    """

    def _marcar(id: int, fecha_baja: str) -> httpx.Response:
        return httpx.post(f"{url_api}/api/empleados/{id}/baja", json={"fecha_baja": fecha_baja})

    return _marcar

"""Pruebas de API para HU-01: registro de empleados."""
import re
import uuid
from datetime import date, timedelta

import httpx


def _correo_unico(base: str) -> str:
    return f"{base}.{uuid.uuid4().hex[:8]}@empresa.com"


def _crear_empleado(url_api: str, **sobrescrituras) -> dict:
    datos = {
        "nombre": "Empleado de Prueba",
        "correo": _correo_unico("empleado.prueba"),
        "puesto": "Analista",
        "departamento": "Tecnología",
        "fecha_ingreso": "2023-01-15",
    }
    datos.update(sobrescrituras)
    respuesta = httpx.post(f"{url_api}/api/empleados", json=datos)
    assert respuesta.status_code == 201
    return respuesta.json()


def _buscar(url_api: str, correo: str) -> list[dict]:
    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": correo})
    assert respuesta.status_code == 200
    return respuesta.json()


def test_cp01_registro_exitoso_con_datos_validos(url_api):
    """CP-01: registro exitoso de un empleado con datos válidos."""
    correo_enviado = f"Ana.Lopez.{uuid.uuid4().hex[:8]}@empresa.com"

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Ana López",
            "correo": correo_enviado,
            "puesto": "Analista de Datos",
            "departamento": "Tecnología",
            "fecha_ingreso": "2024-03-01",
        },
    )

    assert respuesta.status_code == 201
    creado = respuesta.json()
    assert re.fullmatch(r"EMP-\d{4}", creado["numero_empleado"])
    assert creado["correo"] == correo_enviado.lower()
    assert creado["estado"] == "activo"


def test_cp03_no_registra_correo_existente_sin_importar_mayusculas(url_api):
    """CP-03: no se puede registrar un empleado con un correo ya existente (sin importar mayúsculas)."""
    correo = _correo_unico("carlos.ruiz")
    _crear_empleado(
        url_api,
        nombre="Carlos Ruiz",
        correo=correo,
        puesto="Vendedor",
        departamento="Ventas",
        fecha_ingreso="2024-01-15",
    )

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Carlos Ruiz",
            "correo": correo.upper(),
            "puesto": "Vendedor",
            "departamento": "Ventas",
            "fecha_ingreso": "2024-01-15",
        },
    )

    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == "El correo ya está registrado"
    assert len(_buscar(url_api, correo)) == 1


def test_cp05_no_registra_correo_no_corporativo(url_api):
    """CP-05: no se puede registrar un empleado con un correo que no es corporativo."""
    correo = f"maria.gomez.{uuid.uuid4().hex[:8]}@gmail.com"

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "María Gómez",
            "correo": correo,
            "puesto": "Contadora",
            "departamento": "Finanzas",
            "fecha_ingreso": "2024-02-10",
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == "Usa el correo corporativo @empresa.com"
    assert _buscar(url_api, correo) == []


def test_cp07_no_registra_nombre_invalido(url_api):
    """CP-07: no se puede registrar un empleado con otros datos inválidos (nombre)."""
    correo = _correo_unico("luis.diaz")

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "A",
            "correo": correo,
            "puesto": "Diseñador",
            "departamento": "Tecnología",
            "fecha_ingreso": "2024-01-01",
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == "El nombre debe tener entre 2 y 80 caracteres"
    assert _buscar(url_api, correo) == []


def test_cp09_no_registra_puesto_invalido(url_api):
    """CP-09: no se puede registrar un empleado con otros datos inválidos (puesto)."""
    correo = _correo_unico("laura.sote")

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Luis Díaz",
            "correo": correo,
            "puesto": "D",
            "departamento": "Ventas",
            "fecha_ingreso": "2024-01-01",
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == "El puesto debe tener entre 2 y 60 caracteres"
    assert _buscar(url_api, correo) == []


def test_cp11_no_registra_departamento_invalido(url_api):
    """CP-11: no se puede registrar un empleado con otros datos inválidos (departamento)."""
    correo = _correo_unico("jorge.paz")

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Jorge Paz",
            "correo": correo,
            "puesto": "Supervisor",
            "departamento": "Marketing",
            "fecha_ingreso": "2024-01-01",
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == "El departamento debe ser uno del catálogo válido"
    assert _buscar(url_api, correo) == []


def test_cp13_no_registra_fecha_ingreso_futura(url_api):
    """CP-13: no se puede registrar un empleado con fecha de ingreso futura."""
    correo = _correo_unico("pedro.sanz")
    fecha_futura = (date.today() + timedelta(days=30)).isoformat()

    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Pedro Sanz",
            "correo": correo,
            "puesto": "Técnico",
            "departamento": "Operaciones",
            "fecha_ingreso": fecha_futura,
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == "La fecha de ingreso no puede ser futura"
    assert _buscar(url_api, correo) == []

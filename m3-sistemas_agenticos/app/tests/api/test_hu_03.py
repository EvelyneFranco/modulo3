"""Pruebas de API para HU-03: edición y baja de empleados."""
import uuid

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


def test_cp01_editar_puesto_y_departamento_empleado_activo(url_api):
    """CP-01: editar puesto y departamento de un empleado activo."""
    creado = _crear_empleado(url_api, puesto="Analista Jr.", departamento="Ventas")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}",
        json={"puesto": "Analista Sr.", "departamento": "Finanzas"},
    )
    assert respuesta.status_code == 200

    obtenido = httpx.get(f"{url_api}/api/empleados/{creado['id']}")
    assert obtenido.status_code == 200
    cuerpo = obtenido.json()
    assert cuerpo["puesto"] == "Analista Sr."
    assert cuerpo["departamento"] == "Finanzas"


def test_cp03_no_se_puede_editar_numero_empleado_ni_correo(url_api):
    """CP-03: no se puede editar el número de empleado ni el correo."""
    correo_original = _correo_unico("ana.lopez")
    creado = _crear_empleado(url_api, correo=correo_original)

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}",
        json={"numero_empleado": "EMP-0099", "correo": "ana.nueva@empresa.com"},
    )
    assert respuesta.status_code == 422
    detalle = respuesta.json()["detail"]
    assert "numero_empleado" in detalle
    assert "correo" in detalle

    obtenido = httpx.get(f"{url_api}/api/empleados/{creado['id']}")
    cuerpo = obtenido.json()
    assert cuerpo["numero_empleado"] == creado["numero_empleado"]
    assert cuerpo["correo"] == correo_original


def test_cp05_departamento_fuera_del_catalogo(url_api):
    """CP-05: editar con un departamento que no está en la lista permitida."""
    creado = _crear_empleado(url_api, puesto="Soporte", departamento="Operaciones")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}",
        json={"departamento": "Mercadotecnia"},
    )
    assert respuesta.status_code == 422
    assert "departamento" in respuesta.json()["detail"]


def test_cp07_dar_de_baja_empleado_activo(url_api):
    """CP-07: dar de baja a un empleado activo."""
    creado = _crear_empleado(url_api, fecha_ingreso="2022-03-01")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{creado['id']}/baja",
        json={"fecha_baja": "2024-05-10"},
    )
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "baja"
    assert cuerpo["fecha_baja"] == "2024-05-10"

    obtenido = httpx.get(f"{url_api}/api/empleados/{creado['id']}")
    assert obtenido.json()["estado"] == "baja"

    listado = httpx.get(f"{url_api}/api/empleados")
    numeros = [e["numero_empleado"] for e in listado.json()]
    assert creado["numero_empleado"] in numeros


def test_cp09_fecha_baja_anterior_a_fecha_ingreso(url_api):
    """CP-09: dar de baja con una fecha de baja anterior a la fecha de ingreso."""
    creado = _crear_empleado(url_api, fecha_ingreso="2023-01-15")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{creado['id']}/baja",
        json={"fecha_baja": "2022-12-01"},
    )
    assert respuesta.status_code == 422
    assert "fecha de baja" in respuesta.json()["detail"]

    obtenido = httpx.get(f"{url_api}/api/empleados/{creado['id']}")
    assert obtenido.json()["estado"] == "activo"


def test_cp11_no_se_puede_editar_empleado_dado_de_baja(url_api, marcar_baja):
    """CP-11: no se puede editar a un empleado ya dado de baja."""
    creado = _crear_empleado(url_api, puesto="Puesto Original")
    baja = marcar_baja(creado["id"], "2024-01-20")
    assert baja.status_code == 200

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}",
        json={"puesto": "Coordinador"},
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == "No se puede editar a un empleado dado de baja"

    obtenido = httpx.get(f"{url_api}/api/empleados/{creado['id']}")
    assert obtenido.json()["puesto"] == "Puesto Original"

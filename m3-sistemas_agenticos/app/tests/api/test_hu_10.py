"""Pruebas de API para HU-10: solicitud y saldo de vacaciones."""
import uuid

import httpx


def _correo_unico(base: str) -> str:
    return f"{base}.{uuid.uuid4().hex[:8]}@empresa.com"


def _crear_empleado(url_api: str, **sobrescrituras) -> dict:
    datos = {
        "nombre": "Empleado de Prueba",
        "correo": _correo_unico("empleado.vacaciones"),
        "puesto": "Analista",
        "departamento": "Tecnología",
        "fecha_ingreso": "2024-03-10",
    }
    datos.update(sobrescrituras)
    respuesta = httpx.post(f"{url_api}/api/empleados", json=datos)
    assert respuesta.status_code == 201
    return respuesta.json()


def _solicitar(url_api: str, empleado_id: int, fecha_inicio: str, fecha_fin: str) -> httpx.Response:
    return httpx.post(
        f"{url_api}/api/empleados/{empleado_id}/vacaciones",
        json={"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin},
    )


def test_cp01_solicitud_valida_registra_y_descuenta_del_saldo(url_api):
    """CP-01: solicitud válida que se registra y descuenta del saldo del año."""
    creado = _crear_empleado(url_api)

    respuesta = _solicitar(url_api, creado["id"], "2026-07-06", "2026-07-10")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["dias_habiles"] == 5
    assert cuerpo["dias_restantes"] == 7


def test_cp03_sabados_domingos_y_festivos_no_se_descuentan(url_api):
    """CP-03: los sábados, domingos y festivos dentro del periodo no se descuentan."""
    creado = _crear_empleado(url_api)

    respuesta = _solicitar(url_api, creado["id"], "2026-12-21", "2026-12-31")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["dias_habiles"] == 8
    assert cuerpo["dias_restantes"] == 4


def test_cp05_empleado_que_no_existe_no_puede_solicitar_vacaciones(url_api):
    """CP-05: un empleado que no existe no puede solicitar vacaciones."""
    respuesta = _solicitar(url_api, 9999, "2026-07-06", "2026-07-10")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Empleado no encontrado"


def test_cp06_empleado_dado_de_baja_no_puede_solicitar_vacaciones(url_api, marcar_baja):
    """CP-06: un empleado dado de baja no puede solicitar vacaciones."""
    creado = _crear_empleado(url_api, fecha_ingreso="2020-01-15")
    baja = marcar_baja(creado["id"], "2025-01-01")
    assert baja.status_code == 200

    respuesta = _solicitar(url_api, creado["id"], "2026-07-06", "2026-07-10")

    assert respuesta.status_code == 409
    assert (
        respuesta.json()["detail"]
        == "No se pueden solicitar vacaciones para un empleado dado de baja"
    )


def test_cp07_fecha_fin_anterior_a_fecha_inicio(url_api):
    """CP-07: la fecha de fin no puede ser anterior a la fecha de inicio."""
    creado = _crear_empleado(url_api)

    respuesta = _solicitar(url_api, creado["id"], "2026-07-10", "2026-07-05")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "La fecha de fin no puede ser anterior a la fecha de inicio"
    )


def test_cp09_periodo_no_puede_cruzar_de_un_anio_a_otro(url_api):
    """CP-09: un periodo no puede cruzar de un año a otro."""
    creado = _crear_empleado(url_api)

    respuesta = _solicitar(url_api, creado["id"], "2026-12-28", "2027-01-08")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "Las vacaciones deben estar dentro de un mismo año calendario"
    )


def test_cp11_anio_fuera_de_la_tabla_de_festivos_se_rechaza(url_api):
    """CP-11: un año fuera de la tabla de festivos se rechaza."""
    creado = _crear_empleado(url_api)

    respuesta = _solicitar(url_api, creado["id"], "2028-07-06", "2028-07-10")

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "Solo se pueden solicitar vacaciones en 2026 y 2027"


def test_cp13_menos_de_un_anio_de_antiguedad_no_puede_solicitar(url_api):
    """CP-13: un empleado con menos de un año de antigüedad no puede solicitar vacaciones."""
    creado = _crear_empleado(url_api, fecha_ingreso="2026-01-10")

    respuesta = _solicitar(url_api, creado["id"], "2026-06-01", "2026-06-05")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp14_justo_un_anio_cumplido_puede_solicitar(url_api):
    """CP-14: un empleado que cumple justo un año de antigüedad el día de inicio puede solicitar."""
    creado = _crear_empleado(url_api, fecha_ingreso="2025-12-21")

    respuesta = _solicitar(url_api, creado["id"], "2026-12-21", "2026-12-21")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["dias_habiles"] == 1
    assert cuerpo["dias_restantes"] == 11


def test_cp15_un_dia_antes_de_cumplir_el_anio_no_puede_solicitar(url_api):
    """CP-15: un empleado al que le falta un día para cumplir el año no puede solicitar."""
    creado = _crear_empleado(url_api, fecha_ingreso="2025-12-21")

    respuesta = _solicitar(url_api, creado["id"], "2026-12-20", "2026-12-20")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp17_periodo_sin_ningun_dia_habil_se_rechaza(url_api):
    """CP-17: un periodo sin ningún día hábil se rechaza."""
    creado = _crear_empleado(url_api)

    respuesta = _solicitar(url_api, creado["id"], "2026-07-11", "2026-07-12")

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El periodo no incluye días hábiles"


def test_cp19_solicitud_que_rebasa_los_dias_disponibles_se_rechaza(url_api):
    """CP-19: una solicitud que rebasa los días disponibles del año se rechaza indicando cuántos quedan."""
    creado = _crear_empleado(url_api)
    previa = _solicitar(url_api, creado["id"], "2026-09-14", "2026-09-18")
    assert previa.status_code == 201
    assert previa.json()["dias_habiles"] == 4

    respuesta = _solicitar(url_api, creado["id"], "2026-11-02", "2026-11-12")

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "La solicitud excede los días disponibles: quedan 8 días hábiles"
    )


def test_cp20_solicitud_con_exactamente_los_dias_que_quedan(url_api):
    """CP-20: una solicitud con exactamente los días que quedan se registra y agota el saldo."""
    creado = _crear_empleado(url_api)
    previa = _solicitar(url_api, creado["id"], "2026-09-14", "2026-09-18")
    assert previa.status_code == 201
    assert previa.json()["dias_habiles"] == 4

    respuesta = _solicitar(url_api, creado["id"], "2026-11-02", "2026-11-11")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["dias_habiles"] == 8
    assert cuerpo["dias_restantes"] == 0

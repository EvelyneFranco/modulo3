"""Pruebas E2E para HU-10: solicitud y saldo de vacaciones."""
import uuid

import httpx
from playwright.sync_api import expect


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


def _solicitar_vacaciones(page, empleado_id: int, fecha_inicio: str, fecha_fin: str) -> None:
    page.get_by_test_id(f"vacaciones-abrir-{empleado_id}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill(fecha_inicio)
    page.get_by_test_id("vacaciones-fecha-fin").fill(fecha_fin)
    page.get_by_test_id("vacaciones-enviar").click()


def test_cp02_solicitud_valida_registra_y_descuenta_del_saldo(page, url_api, url_web):
    """CP-02: solicitud válida que se registra y descuenta del saldo del año."""
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-07-06", "2026-07-10")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."
    )


def test_cp04_sabados_domingos_y_festivos_no_se_descuentan(page, url_api, url_web):
    """CP-04: los sábados, domingos y festivos dentro del periodo no se descuentan."""
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-12-21", "2026-12-31")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 8 días hábiles. Te quedan 4 días hábiles en 2026."
    )


def test_cp08_fecha_fin_anterior_a_fecha_inicio(page, url_api, url_web):
    """CP-08: la fecha de fin no puede ser anterior a la fecha de inicio."""
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-07-10", "2026-07-05")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "La fecha de fin no puede ser anterior a la fecha de inicio"
    )


def test_cp10_periodo_no_puede_cruzar_de_un_anio_a_otro(page, url_api, url_web):
    """CP-10: un periodo no puede cruzar de un año a otro."""
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-12-28", "2027-01-08")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Las vacaciones deben estar dentro de un mismo año calendario"
    )


def test_cp12_anio_fuera_de_la_tabla_de_festivos_se_rechaza(page, url_api, url_web):
    """CP-12: un año fuera de la tabla de festivos se rechaza."""
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2028-07-06", "2028-07-10")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solo se pueden solicitar vacaciones en 2026 y 2027"
    )


def test_cp16_menos_de_un_anio_de_antiguedad_no_puede_solicitar(page, url_api, url_web):
    """CP-16: un empleado con menos de un año de antigüedad no puede solicitar vacaciones."""
    creado = _crear_empleado(url_api, fecha_ingreso="2026-01-10")

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-06-01", "2026-06-05")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp18_periodo_sin_ningun_dia_habil_se_rechaza(page, url_api, url_web):
    """CP-18: un periodo sin ningún día hábil se rechaza."""
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-07-11", "2026-07-12")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "El periodo no incluye días hábiles"
    )


def test_cp21_solicitud_que_rebasa_los_dias_disponibles_se_rechaza(page, url_api, url_web):
    """CP-21: una solicitud que rebasa los días disponibles del año se rechaza indicando cuántos quedan."""
    creado = _crear_empleado(url_api)
    previa = httpx.post(
        f"{url_api}/api/empleados/{creado['id']}/vacaciones",
        json={"fecha_inicio": "2026-09-14", "fecha_fin": "2026-09-18"},
    )
    assert previa.status_code == 201

    page.goto(url_web)
    _solicitar_vacaciones(page, creado["id"], "2026-11-02", "2026-11-12")

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "La solicitud excede los días disponibles: quedan 8 días hábiles"
    )

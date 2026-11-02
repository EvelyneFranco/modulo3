"""Pruebas E2E para HU-01: registro de empleados."""
import re
import uuid
from datetime import date, timedelta

import httpx
from playwright.sync_api import expect


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


def _llenar_formulario(page, *, nombre, correo, puesto, departamento, fecha_ingreso):
    page.get_by_test_id("empleado-nombre").fill(nombre)
    page.get_by_test_id("empleado-correo").fill(correo)
    page.get_by_test_id("empleado-puesto").fill(puesto)
    page.get_by_test_id("empleado-departamento").select_option(departamento)
    page.get_by_test_id("empleado-fecha-ingreso").fill(fecha_ingreso)
    page.get_by_test_id("empleado-guardar").click()


def test_cp02_registro_exitoso_con_datos_validos(page, url_web):
    """CP-02: registro exitoso de un empleado con datos válidos."""
    correo = f"Ana.Lopez.{uuid.uuid4().hex[:8]}@empresa.com"

    page.goto(url_web)
    _llenar_formulario(
        page,
        nombre="Ana López",
        correo=correo,
        puesto="Analista de Datos",
        departamento="Tecnología",
        fecha_ingreso="2024-03-01",
    )

    mensaje = page.get_by_test_id("mensaje-exito")
    expect(mensaje).to_have_text(re.compile(r"^Empleado EMP-\d{4} registrado con éxito$"))


def test_cp04_no_registra_correo_existente_sin_importar_mayusculas(page, url_api, url_web):
    """CP-04: no se puede registrar un empleado con un correo ya existente (sin importar mayúsculas)."""
    correo = _correo_unico("carlos.ruiz")
    _crear_empleado(
        url_api,
        nombre="Carlos Ruiz",
        correo=correo,
        puesto="Vendedor",
        departamento="Ventas",
        fecha_ingreso="2024-01-15",
    )

    page.goto(url_web)
    _llenar_formulario(
        page,
        nombre="Carlos Ruiz",
        correo=correo.upper(),
        puesto="Vendedor",
        departamento="Ventas",
        fecha_ingreso="2024-01-15",
    )

    expect(page.get_by_test_id("mensaje-error")).to_have_text("El correo ya está registrado")


def test_cp06_no_registra_correo_no_corporativo(page, url_web):
    """CP-06: no se puede registrar un empleado con un correo que no es corporativo."""
    correo = f"maria.gomez.{uuid.uuid4().hex[:8]}@gmail.com"

    page.goto(url_web)
    _llenar_formulario(
        page,
        nombre="María Gómez",
        correo=correo,
        puesto="Contadora",
        departamento="Finanzas",
        fecha_ingreso="2024-02-10",
    )

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "Usa el correo corporativo @empresa.com"
    )


def test_cp08_no_registra_nombre_invalido(page, url_web):
    """CP-08: no se puede registrar un empleado con otros datos inválidos (nombre)."""
    correo = _correo_unico("luis.diaz")

    page.goto(url_web)
    _llenar_formulario(
        page,
        nombre="A",
        correo=correo,
        puesto="Diseñador",
        departamento="Tecnología",
        fecha_ingreso="2024-01-01",
    )

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "El nombre debe tener entre 2 y 80 caracteres"
    )


def test_cp10_no_registra_puesto_invalido(page, url_web):
    """CP-10: no se puede registrar un empleado con otros datos inválidos (puesto)."""
    correo = _correo_unico("laura.sote")

    page.goto(url_web)
    _llenar_formulario(
        page,
        nombre="Luis Díaz",
        correo=correo,
        puesto="D",
        departamento="Ventas",
        fecha_ingreso="2024-01-01",
    )

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "El puesto debe tener entre 2 y 60 caracteres"
    )


def test_cp12_departamento_invalido_no_disponible_en_el_catalogo(page, url_web):
    """CP-12: no se puede registrar un empleado con otros datos inválidos (departamento).

    'Marketing' no está en el catálogo, así que la pantalla no permite capturarlo
    en el select; la validación del backend para este caso ya se prueba en CP-11 (api).
    """
    page.goto(url_web)

    opcion_no_disponible = page.get_by_test_id("empleado-departamento").get_by_role(
        "option", name="Marketing"
    )
    expect(opcion_no_disponible).to_have_count(0)


def test_cp14_no_registra_fecha_ingreso_futura(page, url_web):
    """CP-14: no se puede registrar un empleado con fecha de ingreso futura."""
    correo = _correo_unico("pedro.sanz")
    fecha_futura = (date.today() + timedelta(days=30)).isoformat()

    page.goto(url_web)
    _llenar_formulario(
        page,
        nombre="Pedro Sanz",
        correo=correo,
        puesto="Técnico",
        departamento="Operaciones",
        fecha_ingreso=fecha_futura,
    )

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "La fecha de ingreso no puede ser futura"
    )

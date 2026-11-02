"""Pruebas E2E para HU-03: edición y baja de empleados."""
import uuid

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


def test_cp02_editar_puesto_y_departamento_empleado_activo(page, url_api, url_web):
    """CP-02: editar puesto y departamento de un empleado activo."""
    creado = _crear_empleado(url_api, puesto="Analista Jr.", departamento="Ventas")

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("Analista Sr.")
    page.get_by_test_id("empleado-departamento").select_option("Finanzas")
    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    fila = page.get_by_test_id(f"fila-empleado-{creado['id']}")
    expect(fila).to_contain_text("Analista Sr.")
    expect(fila).to_contain_text("Finanzas")


def test_cp04_correo_deshabilitado_al_editar(page, url_api, url_web):
    """CP-04: no se puede editar el número de empleado ni el correo."""
    correo_original = _correo_unico("ana.lopez")
    creado = _crear_empleado(url_api, correo=correo_original)

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{creado['id']}").click()

    campo_correo = page.get_by_test_id("empleado-correo")
    expect(campo_correo).to_be_disabled()
    expect(campo_correo).to_have_value(correo_original)

    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id(f"numero-empleado-{creado['id']}")).to_have_text(
        creado["numero_empleado"]
    )


def test_cp06_departamento_fuera_del_catalogo(page, url_api, url_web):
    """CP-06: editar con un departamento que no está en la lista permitida.

    'Mercadotecnia' no está en el catálogo, así que el select ni siquiera ofrece
    esa opción; el intento de editar con ese departamento se cubre en la API (CP-05).
    """
    creado = _crear_empleado(url_api)

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{creado['id']}").click()

    opcion_mercadotecnia = page.get_by_test_id("empleado-departamento").locator(
        "option", has_text="Mercadotecnia"
    )
    expect(opcion_mercadotecnia).to_have_count(0)


def test_cp08_dar_de_baja_empleado_activo(page, url_api, url_web):
    """CP-08: dar de baja a un empleado activo."""
    creado = _crear_empleado(url_api, fecha_ingreso="2022-03-01")

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2024-05-10")
    page.get_by_test_id("confirmar-baja").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{creado['id']}")).to_have_text("Baja")
    expect(page.get_by_test_id(f"fila-empleado-{creado['id']}")).to_be_visible()


def test_cp10_fecha_baja_anterior_a_fecha_ingreso(page, url_api, url_web):
    """CP-10: dar de baja con una fecha de baja anterior a la fecha de ingreso."""
    creado = _crear_empleado(url_api, fecha_ingreso="2023-01-15")

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2022-12-01")
    page.get_by_test_id("confirmar-baja").click()

    expect(page.get_by_test_id("mensaje-error")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{creado['id']}")).to_have_text("Activo")


def test_cp12_no_se_puede_editar_empleado_dado_de_baja(page, url_api, url_web, marcar_baja):
    """CP-12: no se puede editar a un empleado ya dado de baja."""
    creado = _crear_empleado(url_api, puesto="Puesto Original")
    baja = marcar_baja(creado["id"], "2024-01-20")
    assert baja.status_code == 200

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("Coordinador")
    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "No se puede editar a un empleado dado de baja"
    )
    fila = page.get_by_test_id(f"fila-empleado-{creado['id']}")
    expect(fila).to_contain_text("Puesto Original")

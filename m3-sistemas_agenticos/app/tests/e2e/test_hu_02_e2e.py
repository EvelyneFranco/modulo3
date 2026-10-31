"""Pruebas E2E para HU-02: directorio de empleados."""
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


def test_cp02_fila_muestra_datos_principales(page, url_api, url_web):
    """CP-02: ver el directorio con los datos principales de cada empleado."""
    creado = _crear_empleado(
        url_api,
        nombre="Laura Gómez",
        correo=_correo_unico("laura.gomez"),
        puesto="Analista de Nómina",
        departamento="Recursos Humanos",
    )

    page.goto(url_web)
    expect(page.get_by_test_id("tabla-empleados")).to_be_visible()

    fila = page.get_by_test_id(f"fila-empleado-{creado['id']}")
    expect(fila).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{creado['id']}")).to_have_text(
        creado["numero_empleado"]
    )
    expect(fila).to_contain_text("Laura Gómez")
    expect(fila).to_contain_text("Analista de Nómina")
    expect(fila).to_contain_text("Recursos Humanos")
    expect(page.get_by_test_id(f"estado-empleado-{creado['id']}")).to_have_text("Activo")


def test_cp04_buscar_nombre_minusculas_sin_importar_mayusculas(page, url_api, url_web):
    """CP-04: buscar por nombre en minúsculas encuentra coincidencias sin importar mayúsculas."""
    creado = _crear_empleado(
        url_api,
        nombre="Carlos Ramírez",
        correo=_correo_unico("carlos.ramirez"),
        departamento="Ventas",
    )

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill("carlos ramirez")

    expect(page.get_by_test_id(f"fila-empleado-{creado['id']}")).to_be_visible()


def test_cp06_buscar_correo_mayusculas_sin_importar_mayusculas(page, url_api, url_web):
    """CP-06: buscar por correo en mayúsculas encuentra coincidencias sin importar mayúsculas."""
    correo = _correo_unico("ana.torres")
    creado = _crear_empleado(url_api, nombre="Ana Torres", correo=correo)

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(correo.upper())

    expect(page.get_by_test_id(f"fila-empleado-{creado['id']}")).to_be_visible()


def test_cp08_filtrar_por_departamento(page, url_api, url_web):
    """CP-08: filtrar por departamento muestra solo a los empleados de ese departamento."""
    incluido = _crear_empleado(
        url_api,
        nombre="Pedro Salinas",
        correo=_correo_unico("pedro.salinas"),
        departamento="Ventas",
    )
    excluido = _crear_empleado(
        url_api,
        nombre="Mónica Lira",
        correo=_correo_unico("monica.lira"),
        departamento="Tecnología",
    )

    page.goto(url_web)
    page.get_by_test_id("filtro-departamento").select_option("Ventas")

    expect(page.get_by_test_id(f"fila-empleado-{incluido['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"fila-empleado-{excluido['id']}")).to_have_count(0)


def test_cp10_buscar_sin_coincidencias_muestra_sin_resultados(page, url_api, url_web):
    """CP-10: buscar un texto sin coincidencias muestra un mensaje de sin resultados."""
    _crear_empleado(
        url_api,
        nombre="Sofía Mendoza",
        correo=_correo_unico("sofia.mendoza"),
    )

    page.goto(url_web)
    texto_sin_coincidencias = f"zzz-inexistente-{uuid.uuid4().hex[:8]}"
    page.get_by_test_id("buscar-empleados").fill(texto_sin_coincidencias)

    sin_resultados = page.get_by_test_id("sin-resultados")
    expect(sin_resultados).to_be_visible()
    expect(sin_resultados).to_have_text("No se encontraron resultados")


def test_cp12_empleado_dado_de_baja_sigue_en_el_directorio(page, url_api, url_web, marcar_baja):
    """CP-12: un empleado dado de baja sigue apareciendo en el directorio."""
    correo = _correo_unico("jorge.nieto")
    creado = _crear_empleado(url_api, nombre="Jorge Nieto", correo=correo)
    marcar_baja(correo, "2024-03-10")

    page.goto(url_web)

    fila = page.get_by_test_id(f"fila-empleado-{creado['id']}")
    expect(fila).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{creado['id']}")).to_have_text("Baja")


def test_cp14_combinar_busqueda_y_departamento_sin_coincidencias(page, url_api, url_web):
    """CP-14: combinar búsqueda y filtro de departamento sin coincidencias muestra un mensaje de sin resultados."""
    _crear_empleado(
        url_api,
        nombre="Luis Peña",
        correo=_correo_unico("luis.pena"),
        departamento="Finanzas",
    )

    page.goto(url_web)
    page.get_by_test_id("filtro-departamento").select_option("Operaciones")
    page.get_by_test_id("buscar-empleados").fill("Luis Peña")

    sin_resultados = page.get_by_test_id("sin-resultados")
    expect(sin_resultados).to_be_visible()
    expect(sin_resultados).to_have_text("No se encontraron resultados")

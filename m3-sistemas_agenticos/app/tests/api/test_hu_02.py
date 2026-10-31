"""Pruebas de API para HU-02: directorio de empleados."""
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


def test_cp01_directorio_muestra_datos_principales(url_api):
    """CP-01: ver el directorio con los datos principales de cada empleado."""
    creado = _crear_empleado(
        url_api,
        nombre="Laura Gómez",
        correo=_correo_unico("laura.gomez"),
        puesto="Analista de Nómina",
        departamento="Recursos Humanos",
    )

    respuesta = httpx.get(f"{url_api}/api/empleados")
    assert respuesta.status_code == 200
    empleados = respuesta.json()
    encontrado = next(
        (e for e in empleados if e["numero_empleado"] == creado["numero_empleado"]), None
    )
    assert encontrado is not None
    assert encontrado["nombre"] == "Laura Gómez"
    assert encontrado["puesto"] == "Analista de Nómina"
    assert encontrado["departamento"] == "Recursos Humanos"
    assert encontrado["estado"] == "activo"


def test_cp03_buscar_nombre_minusculas_sin_importar_mayusculas(url_api):
    """CP-03: buscar por nombre en minúsculas encuentra coincidencias sin importar mayúsculas."""
    creado = _crear_empleado(
        url_api,
        nombre="Carlos Ramírez",
        correo=_correo_unico("carlos.ramirez"),
        departamento="Ventas",
    )

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": "carlos ramirez"})
    assert respuesta.status_code == 200
    numeros = [e["numero_empleado"] for e in respuesta.json()]
    assert creado["numero_empleado"] in numeros


def test_cp05_buscar_correo_mayusculas_sin_importar_mayusculas(url_api):
    """CP-05: buscar por correo en mayúsculas encuentra coincidencias sin importar mayúsculas."""
    correo = _correo_unico("ana.torres")
    creado = _crear_empleado(url_api, nombre="Ana Torres", correo=correo)

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": correo.upper()})
    assert respuesta.status_code == 200
    numeros = [e["numero_empleado"] for e in respuesta.json()]
    assert creado["numero_empleado"] in numeros


def test_cp07_filtrar_por_departamento(url_api):
    """CP-07: filtrar por departamento muestra solo a los empleados de ese departamento."""
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

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"departamento": "Ventas"})
    assert respuesta.status_code == 200
    numeros = [e["numero_empleado"] for e in respuesta.json()]
    assert incluido["numero_empleado"] in numeros
    assert excluido["numero_empleado"] not in numeros


def test_cp09_buscar_sin_coincidencias_devuelve_arreglo_vacio(url_api):
    """CP-09: buscar un texto sin coincidencias muestra un mensaje de sin resultados."""
    _crear_empleado(
        url_api,
        nombre="Sofía Mendoza",
        correo=_correo_unico("sofia.mendoza"),
    )

    texto_sin_coincidencias = f"zzz-inexistente-{uuid.uuid4().hex[:8]}"
    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": texto_sin_coincidencias})
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_cp11_empleado_dado_de_baja_sigue_en_el_directorio(url_api, marcar_baja):
    """CP-11: un empleado dado de baja sigue apareciendo en el directorio."""
    correo = _correo_unico("jorge.nieto")
    creado = _crear_empleado(url_api, nombre="Jorge Nieto", correo=correo)
    marcar_baja(correo, "2024-03-10")

    respuesta = httpx.get(f"{url_api}/api/empleados")
    assert respuesta.status_code == 200
    encontrado = next(
        (e for e in respuesta.json() if e["numero_empleado"] == creado["numero_empleado"]), None
    )
    assert encontrado is not None
    assert encontrado["estado"] == "baja"
    assert encontrado["fecha_baja"] == "2024-03-10"


def test_cp13_combinar_busqueda_y_departamento_sin_coincidencias(url_api):
    """CP-13: combinar búsqueda y filtro de departamento sin coincidencias muestra un mensaje de sin resultados."""
    _crear_empleado(
        url_api,
        nombre="Luis Peña",
        correo=_correo_unico("luis.pena"),
        departamento="Finanzas",
    )

    respuesta = httpx.get(
        f"{url_api}/api/empleados",
        params={"departamento": "Operaciones", "buscar": "Luis Peña"},
    )
    assert respuesta.status_code == 200
    assert respuesta.json() == []

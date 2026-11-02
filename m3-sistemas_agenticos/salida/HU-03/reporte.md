# Reporte · HU-03

**Estado:** ESCALAR A UNA PERSONA
**Costo de agentes:** 4.24 USD
**Ciclos de corrección:** 2

## Bitácora
- Filtro de historia: OK
- Criterios escritos en criterios.feature
- Preguntas abiertas: la persona respondió 'si'
- Casos de prueba escritos en casos_prueba.json
- Plan rechazado:  No apruebo el cambio de id a numero_empleado. Mantén {id} en rutas y data-testid como dice la convención (fila-empleado-{id}, editar-empleado-{id}, baja-empleado-{id}) y en PUT /api/empleados/{id} y POST /api/empleados/{id}/baja. No modifiques el comportamiento de HU-01 y HU-02. El 409 debe responder con el mensaje «No se puede editar a un empleado dado de baja». El resto del plan está bien.
- Plan aprobado por una persona
- Construcción 1
- Verificación: OK
- Pruebas automatizadas: OK (12 casos)
- Despliegue: OK
- Despliegue y pruebas listos
- Pruebas E2E: 7 failed, 19 passed in 34.40s
- Triage → desarrollador: En la API, dar de baja a un empleado no persiste el estado: GET posterior devuelve 'activo' en vez de 'baja' (test_cp11_empleado_dado_de_baja_sigue_en_el_directorio), y la búsqueda por nombre en minúsculas no encuentra al empleado existente (test_cp03_buscar_nombre_minusculas), incumpliendo el criterio de HU-03 de que el empleado dado de baja sigue apareciendo correctamente en el directorio y HU-02 de búsqueda case-insensitive.
- Código corregido; redespliegue OK
- Pruebas E2E: 6 failed, 20 passed in 26.31s
- Triage → desarrollador: En test_cp11_empleado_dado_de_baja_sigue_en_el_directorio el empleado EMP-0004 debería quedar con estado 'baja' tras la operación de baja, pero la API devuelve 'activo'. El criterio de aceptación "Dar de baja a un empleado activo" indica que el sistema debe responder 200 y el empleado debe quedar con estado 'baja' y fecha_baja establecida. La app no está persistiendo/aplicando el cambio de estado correctamente.
- Código corregido; redespliegue OK
- Pruebas E2E: 5 failed, 21 passed in 21.41s

## Última ejecución de pruebas
```
5 failed, 21 passed in 21.41s
- tests.api.test_hu_02::test_cp03_buscar_nombre_minusculas_sin_importar_mayusculas
  AssertionError: assert 'EMP-0097' in ['EMP-0095']
- tests.api.test_hu_02::test_cp11_empleado_dado_de_baja_sigue_en_el_directorio
  AssertionError: assert 'activo' == 'baja'
  
  - baja
  + activo
- tests.e2e.test_hu_02_e2e::test_cp04_buscar_nombre_minusculas_sin_importar_mayusculas[chromium]
  AssertionError: Locator expected to be visible
Actual value: None
Error: element(s) not found 
Call log:
  - Expect "to_be_visible" get_by_test_id("fila-empleado-111") with timeout 5000ms
  - waiting for get_by_test_id("fila-empleado-111")

Aria snapshot:
- main:
  - heading "Gestión de empleados" [level=1]
  - heading "Registrar empleado" [level=2]
  - text: Nombre
  - textbox "Nombre"
  - text: 
- tests.e2e.test_hu_03_e2e::test_cp04_no_se_puede_editar_el_correo[chromium]
  playwright._impl._errors.TimeoutError: Locator.fill: Timeout 3000ms exceeded.
Call log:
  - waiting for get_by_test_id("empleado-correo")
    - locator resolved to <input value="" disabled id="correo" required="" type="email" name="correo" data-testid="empleado-correo"/>
    - fill("ana.nueva.ae401d57@empresa.com")
  - attempting fill action
    2 × waiting for element to be visible, enabled and e
- tests.e2e.test_hu_03_e2e::test_cp06_editar_con_departamento_fuera_del_catalogo[chromium]
  playwright._impl._errors.TimeoutError: Locator.select_option: Timeout 3000ms exceeded.
Call log:
  - waiting for get_by_test_id("empleado-departamento")
    - locator resolved to <select required="" id="departamento" name="departamento" data-testid="empleado-departamento">…</select>
  - attempting select option action
    2 × waiting for element to be visible and enabled
      - did not find some 
```
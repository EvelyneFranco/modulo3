# Changelog

Cambios a la fábrica de agentes, del más reciente al más antiguo. Cada versión indica el commit donde quedó.

## [1.4.1] · 2026-11-04 · Documentación (`95689c4`)

### Agregado
- Docstrings en las funciones clave: la función principal de cada agente, los nodos con persona en el bucle (`pedir_aclaracion`, `aprobar_plan`), `verificar`, `filtrar_historia`, `pruebas_e2e`, `triage`, `reporte` y `construir_grafo`.
- `README.md`, `CHANGELOG.md`, `salida/HU-10/decisiones.md` y la carpeta `evidencias/` (`1b9b17e`).

## [1.4.0] · 2026-11-04 · Reto HU-10 Solicitar vacaciones (`4f57ec3`)

### Resultado
- La fábrica construyó HU-10 con estado **LISTA**: 0 ciclos de triage, 61 pruebas pasan (21 de HU-10 y 40 de HU-01 a HU-03) y 1.56 USD en agentes de Claude Code.
- `auditoria.jsonl` de la ejecución final: 83 acciones y ninguna fuera de rol.

### Cambiado
- `agentes/disenador_pruebas.py`: pide pasos breves y casos `e2e` solo cuando la pantalla puede producir el resultado. La primera ejecución se cortó por `max_tokens` al escribir 21 casos; se reanudó desde el checkpoint sin repetir al analista.

## [1.3.0] · 2026-11-03 · Fábrica preparada para HU-10 (`899141e`)

### Agregado
- `flujos/flujo_s4.py`: checkpoint persistente con `PostgresSaver` cuando existe `POSTGRES_URI`. Al iniciar, si la historia quedó a medias, pregunta si se reanuda; si no, borra el hilo anterior y empieza de cero.
- `agentes/analista.py`: `mensajes_obligatorios()` extrae de `contexto/convenciones_app.md` los mensajes de error de la sección de la historia; `validar_gherkin()` rechaza los criterios si falta alguno (una `N` suelta acepta cualquier número).

### Cambiado
- `agentes/analista.py`: el analista también lee `contexto/convenciones_app.md` y copia los mensajes de error textuales.
- `agentes/disenador_pruebas.py`: en reglas con fechas o límites, prueba el valor en el borde y el primero que queda fuera.
- `.env`: `PRESUPUESTO_USD` de 2 a 6 por sesión de Claude Code (en HU-03 el desarrollador gastó 1.93 de 2).

## [1.2.0] · 2026-11-03 · Seguridad (`3a205e3`)

### Agregado
- `salida/seguridad.md`: demostración de HU-99 (historia envenenada), comparación de prompt ingenuo (3 de 3 ataques) contra endurecido (0 de 3), capas de defensa, riesgos OWASP agénticos y checklist de producción.
- `salida/bloqueada/reporte.md`: HU-99 bloqueada por `filtrar_historia` con 0.00 USD.

## [1.1.0] · 2026-11-02 · Fábrica corregida y HU-03 (`fb3cb05`)

### Cambiado
- `agentes/automatizador.py`: reescribe pruebas existentes si los casos cambiaron, usa la API de Playwright para Python (`has_text`), crea datos únicos con uuid, prepara datos solo por la API y prueba campos deshabilitados con `to_be_disabled()`.
- `agentes/disenador_pruebas.py`: no inventa requisitos y usa los identificadores de `convenciones_app.md`.
- `agentes/triage.py`: lee los criterios de todas las historias, porque las pruebas de todas corren juntas. Antes culpaba al desarrollador por pruebas de otra historia.
- `agentes/desarrollador.py`: prueba el backend en el puerto 8001 y lo detiene con `kill`. Un `uvicorn` huérfano había bloqueado el flujo.

### Agregado
- HU-03 Editar y dar de baja construida con `flujo_s4`; el primer plan se rechazó porque cambiaba el identificador que usaba HU-02.
- `historias/HU-10-solicitar-vacaciones.md` y las reglas y convenciones de vacaciones al final de `contexto/`.

## [1.0.0] · 2026-10-31 · Labs 1 a 3

- Lab 3 (`4ea5553`): agentes de despliegue y automatización; HU-02 desplegada con Docker Compose y probada con pytest y Playwright.
- Lab 2 (`7ed3ace`): agente desarrollador con Claude Code, aprobación humana del plan y verificación determinista.
- Lab 1 (`01dbe45`, `8bb6c2d`): analista y diseñador de pruebas para HU-01, con validadores y reflexión guiada.

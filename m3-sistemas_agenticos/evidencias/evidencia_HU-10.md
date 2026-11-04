# Evidencia del proceso · Reto HU-10 Solicitar vacaciones

**Alumna:** Evelyne Franco · **Repositorio:** https://github.com/EvelyneFranco/modulo3 · **Fecha de ejecución:** 2026-11-03

## 1. Resumen

| Dato | Valor |
| --- | --- |
| Estado final | **LISTA** (`salida/HU-10/reporte.md`) |
| Escenarios de aceptación | 10, con los 8 mensajes de error textuales |
| Casos de prueba | 21 (13 de API y 8 e2e) |
| Pruebas al final | **61 pasan**: 21 de HU-10 y 40 de HU-01 a HU-03, que no se rompieron |
| Ciclos de triage | 0 |
| Costo de agentes de Claude Code | 1.56 USD |
| Intervenciones humanas | 3: preguntas abiertas, plan rechazado con 4 comentarios y aprobación del segundo plan |
| Acciones auditadas | 83, ninguna fuera de rol |

## 2. Arquitectura

Seis agentes con roles y permisos separados, orquestados por un grafo de LangGraph de flujo fijo. La tabla de roles, el diagrama del grafo y las funciones de LangGraph que se usan (estado tipado con reductores, `interrupt`, paralelización, checkpoint en Postgres) están en el [README](../README.md). El grafo generado está en `flujos/salidas/grafo_flujo_s4.html`.

## 3. Prompts y contexto

| Qué | Dónde |
| --- | --- |
| Prompt de cada agente | `SISTEMA`, `INSTRUCCIONES` y `TAREA` en `agentes/analista.py`, `disenador_pruebas.py`, `desarrollador.py`, `despliegue.py`, `automatizador.py` y `triage.py` |
| Prompt endurecido del filtro | `filtrar_historia` en `flujos/flujo_s4.py` (historia entre `<historia_no_confiable>`) |
| Reglas del repositorio | `CLAUDE.md` |
| Contexto de la app para Claude Code | `app/CLAUDE.md`, copiado de `contexto/convenciones_app.md` antes de construir |
| Reglas y convenciones de vacaciones | Al final de `contexto/reglas_negocio.md` y de `contexto/convenciones_app.md` |

Cambios de prompt hechos para el reto, cada uno con su motivo, en el [CHANGELOG](../CHANGELOG.md) (versiones 1.3.0 y 1.4.0). Los principales:

- **Analista:** «Lee la historia, `contexto/reglas_negocio.md` y `contexto/convenciones_app.md`. Cuando las convenciones fijan un mensaje de error para esta historia, cópialo textual en el escenario.»
- **Diseñador:** «En reglas con fechas o límites, prueba el valor justo en el borde y el primero que queda fuera.» y «Sé breve: […] escribe casos e2e solo cuando la pantalla puede producir el resultado.»

## 4. Recorrido de la fábrica, en orden

| # | Etapa | Evidencia | Captura |
| --- | --- | --- | --- |
| 1 | Filtro de seguridad | Bitácora: «Filtro de historia: OK» | — |
| 2 | Criterios | `salida/HU-10/criterios.feature`; `validar_gherkin` lo aceptó al intento 1 | — |
| 3 | Preguntas abiertas (humano) | Bitácora: «la persona respondió 'si'» | `capturas/pregunta-analista.png` |
| 4 | Casos de prueba | `salida/HU-10/casos_prueba.json`; se cortó por `max_tokens`, se corrigió el agente y se **reanudó desde el checkpoint** | `capturas/reanudar.png` |
| 5 | Plan (humano) | Bitácora: «Plan rechazado: Agrega al plan: 1) …» y luego «Plan aprobado por una persona» | `capturas/plancorregido.png` |
| 6 | Código | 9 archivos de `app/backend` y `app/frontend`; verificación OK en la construcción 1 | — |
| 7 | Despliegue y pruebas, en paralelo | «Despliegue: OK» y «Pruebas automatizadas: OK (21 casos)» | — |
| 8 | Pruebas E2E | «61 passed in 20.46s» | — |
| 9 | Reporte | `salida/HU-10/reporte.md` | — |

La salida completa de la terminal está en [`log_HU-10.txt`](log_HU-10.txt).

**El checkpoint guardó también la bitácora.** El reporte final conserva la línea de las preguntas abiertas, que se respondieron en la primera ejecución, aunque el reporte se escribió en la segunda. El estado se recuperó de Postgres, no se volvió a generar.

## 5. Humano en el bucle

- **Preguntas abiertas:** periodos superpuestos y fechas con formato inválido. Continué porque ninguna regla limita la superposición y las convenciones piden el 422 automático de FastAPI.
- **Primer plan, rechazado:** no mencionaba el mensaje de éxito exacto, no actualizaba el saldo en pantalla tras enviar, no cubría el aniversario exacto ni el 29 de febrero, y no aclaraba que se aceptan exactamente los días que quedan. Cada omisión haría fallar pruebas ocultas.
- **Segundo plan, aprobado:** incluía los 4 puntos (ver el log).

## 6. Triage

En HU-10 no hubo fallas, así que el triage no se activó (0 ciclos). Su funcionamiento quedó demostrado al construir HU-03 (`salida/HU-03/reporte.md`):

- Se enrutó dos veces al desarrollador y el flujo escaló a una persona al llegar a `MAX_CICLOS = 2`.
- **Problema:** el triage solo leía los criterios de la historia actual y culpaba al desarrollador por pruebas de HU-02.
- **Corrección en el agente:** `agentes/triage.py` ahora lee los criterios de todas las historias.

## 7. Integridad: auditoría

`auditoria.jsonl` contiene solo la ejecución final de HU-10. La de los labs se guardó aparte, fuera del commit.

| Agente | Acciones | Archivos que escribió |
| --- | --- | --- |
| desarrollador-plan | 18 (Read, Glob, Bash) | Ninguno: solo lee |
| desarrollador | 35 | `backend/esquemas.py`, `main.py`, `modelos.py`, `rutas_vacaciones.py`, `vacaciones.py`; `frontend/src/App.jsx`, `api/empleados.js`, `components/DirectorioEmpleados.jsx`, `components/FormularioVacaciones.jsx` |
| despliegue | 14 (Read, Bash) | Ninguno: la configuración de Docker ya servía |
| automatizador | 16 | `tests/api/test_hu_10.py`, `tests/e2e/test_hu_10_e2e.py` |

**Esa lista coincide exactamente con los archivos de `app/` del commit de la Fase C.** El único otro cambio en `app/` es `app/CLAUDE.md`, que copia el código de la fábrica (`preparar_app`) desde `contexto/convenciones_app.md`. Nada se escribió a mano. `buscar_denegados.py` reporta 0 intentos fuera de rol. La demostración de las defensas con la historia envenenada HU-99 está en [`salida/seguridad.md`](../salida/seguridad.md).

## 8. Verificación independiente

Además de las pruebas que escribió la fábrica, revisé la app desplegada por mi cuenta.

**API: 23 solicitudes directas.** Todas dieron el resultado de las reglas:
- los ejemplos de las tablas (5, 8 y 4 días hábiles);
- usar justo los días que quedan (queda 0) y el rechazo con «quedan 0 días hábiles»;
- el saldo de 2027 empieza en 12, porque los días no pasan de un año al siguiente;
- antigüedad del aniversario exacto (aceptada) y la del día anterior (rechazada);
- el orden de validación cuando aplican dos errores a la vez;
- el 422 con fecha inválida y el 409 con un empleado dado de baja.

**Contenedores:** `docker compose ps` muestra `backend` (healthy, puerto 8000) y `frontend` (puerto 8080). En Docker Desktop se ve además el contenedor `hitl-postgres`, que guarda el checkpoint del flujo. Ver `capturas/docker-terminal.png` y `capturas/docker-desktop.png`.

**Pantalla, en http://localhost:8080:**

| Captura | Qué muestra |
| --- | --- |
| `solicitudRegistrada.png` | 5 días hábiles, quedan 7, y el saldo se actualiza a 7 |
| `sucessDiasRestantes.png` | Se usa el último día disponible y el saldo queda en 0 |
| `masde12dias.png` | Del 4 al 25 de diciembre son 15 días hábiles: «quedan 12 días hábiles» |
| `segundoDiaRestanteExcede.png` | «quedan 1 días hábiles»: las convenciones piden siempre «días hábiles» |
| `noAntiguedad.png` | Mensaje de antigüedad |
| `fechaFinAntesInicio.png` | Mensaje de fecha de fin anterior |

## 9. Reflexión

1. **Preparar la fábrica rindió más que corregir después.** Antes de correr HU-10 hice que el analista leyera las convenciones y que un validador exigiera los 8 mensajes, y que el diseñador probara los bordes. La construcción salió bien a la primera y sin ciclos de triage. En HU-03, sin esa preparación, costó 4.24 USD y terminó escalada.
2. **Revisar el plan es el punto de control más barato.** Rechazarlo costó 0.12 USD y evitó cuatro fallas que las pruebas ocultas habrían encontrado. Rehacer el código después habría costado varias veces más.
3. **Un checkpoint persistente cambia cómo se trabaja con fallas.** Cuando el diseñador se cortó, la ejecución no se perdió: corregí el agente y el flujo siguió en el mismo paso, con la bitácora intacta.
4. **Las defensas deterministas son las que se pueden demostrar.** Que el modelo «se porte bien» varía entre ejecuciones. Los hooks y la auditoría permiten afirmar con datos que cada archivo lo escribió el agente que debía.

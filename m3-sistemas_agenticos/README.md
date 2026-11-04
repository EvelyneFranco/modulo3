# Fábrica de software con agentes · Módulo 3

Una cadena de seis agentes orquestada con LangGraph que convierte una historia de usuario en una funcionalidad de la aplicación de gestión de empleados: escribe criterios de aceptación, casos de prueba y código; lo despliega con Docker y lo prueba de punta a punta. Una persona aprueba el plan antes de que se escriba código.

Historias construidas por la fábrica: HU-01 Registrar empleado, HU-02 Consultar directorio, HU-03 Editar y dar de baja y **HU-10 Solicitar vacaciones** (reto).

## Agentes y roles

| # | Agente | Rol en el formato de entrega | Entrada | Salida | Puede escribir en |
| --- | --- | --- | --- | --- | --- |
| 1 | Analista | Especificación | Historia + `contexto/` | `salida/HU-xx/criterios.feature` | `salida/HU-xx/` |
| 2 | Diseñador de pruebas | Especificación | Criterios + convenciones | `salida/HU-xx/casos_prueba.json` | `salida/HU-xx/` (solo con `guardar_casos`) |
| 3 | Desarrollador (Claude Code) | Planificador y Codificador | Criterios, casos y reglas | Plan; `app/backend`, `app/frontend` | `backend/*`, `frontend/*` |
| 4 | Despliegue (Claude Code) | Infraestructura | Código | Contenedores con Docker Compose | `docker-compose.yml`, Dockerfiles |
| 5 | Automatizador (Claude Code) | Tester | Casos de prueba | `app/tests` (pytest + Playwright) | `tests/*` |
| 6 | Triage | Reviewer | Pruebas fallidas + criterios | Quién corrige y qué | No escribe: solo enruta |

El rol de **Reviewer** lo cumplen juntos las verificaciones deterministas de `flujos/verificacion.py` (salud de la API, build, pruebas) y el triage, que decide qué agente corrige una falla usando los criterios como referencia.

## Flujo (`flujos/flujo_s4.py`)

```mermaid
graph TD
  A([inicio]) --> F[filtrar_historia]
  F -->|sospechosa| Z[fin · reporte]
  F --> AN[analizar]
  AN -->|preguntas abiertas| PA{{pedir_aclaracion · humano}}
  AN --> DC[disenar_casos]
  PA --> DC
  DC --> PL[planificar]
  PL --> AP{{aprobar_plan · humano}}
  AP -->|comentarios| PL
  AP -->|si| CO[construir]
  CO --> VE[verificar]
  VE -->|falla| CO
  VE --> DE[desplegar]
  VE --> AU[automatizar]
  DE --> LI[listo]
  AU --> LI
  LI --> E2E[pruebas_e2e]
  E2E -->|pasan| Z
  E2E -->|fallan| TR[triage]
  TR --> CC[corregir_codigo] --> E2E
  TR --> CP[corregir_pruebas] --> E2E
  TR --> CD[corregir_despliegue] --> E2E
```

- **Estado tipado:** `Estado` es un `TypedDict` que hereda de los flujos de las sesiones 2 y 3, con reductores para la bitácora y el costo.
- **Humano en el bucle:** `interrupt()` en `pedir_aclaracion` y `aprobar_plan`; se responde con `Command(resume=...)`.
- **Paralelización:** `desplegar` y `automatizar` corren a la vez y se unen en `listo`.
- **Checkpoint persistente:** con `POSTGRES_URI` el estado se guarda en Postgres (`PostgresSaver`) con `thread_id` = nombre de la historia. Si la ejecución se corta, al volver a correr el comando pregunta si se reanuda desde el último paso. Sin `POSTGRES_URI` usa `InMemorySaver`.
- **Límites:** `MAX_INTENTOS = 2` de construcción, `MAX_CICLOS = 2` de triage, `max_turns = 80` y `PRESUPUESTO_USD` por sesión de Claude Code.

El grafo generado se guarda en `flujos/salidas/grafo_flujo_s4.html`.

## Seguridad

Defensa en capas, documentada con la demostración de HU-99 en [`salida/seguridad.md`](salida/seguridad.md):

1. `filtrar_historia`: un LLM revisa la historia entre `<historia_no_confiable>` y la bloquea si trae órdenes ocultas.
2. Lectura limitada del analista y el diseñador (`herramientas_archivos` en `agentes/base.py`).
3. Hooks de Claude Code en `seguridad/hooks.py`: `confinar_escritura`, `confinar_lectura` (bloquea `.env` y `secretos`), `comandos_permitidos` y `auditar`, que registra cada acción en `auditoria.jsonl`.
4. Sin internet: `WebFetch` y `WebSearch` están deshabilitados.

## Requisitos

Python 3.12, Node 20 o superior, Docker Desktop, Claude Code y una clave de API de Anthropic con créditos.

## Instalación

### macOS y Linux

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

### Windows (PowerShell)

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env
```

### Configurar `.env`

```
ANTHROPIC_API_KEY=tu-clave
MODEL=el-modelo-que-indique-el-curso
PRESUPUESTO_USD=6
POSTGRES_URI=postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable
```

`POSTGRES_URI` es opcional. Para tener el checkpoint persistente, levanta Postgres con Docker (mismo comando en los tres sistemas):

```bash
docker run -d --name hitl-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16
```

`.env` nunca se sube al repositorio.

## Uso

Todo se ejecuta desde la raíz del repositorio, como módulo.

```bash
# La fábrica completa con una historia
python -m flujos.flujo_s4 historias/HU-10-solicitar-vacaciones.md

# Agentes por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature
python -m agentes.automatizador HU-01

# Pruebas de todas las historias contra la app desplegada
cd app && pytest tests -q
```

### Ejemplo de una ejecución (HU-10)

1. El filtro revisa la historia y la deja pasar.
2. El analista escribe `criterios.feature`. Si hay preguntas abiertas, el flujo se detiene: responde `si` para continuar o cualquier otra cosa para detenerlo.
3. El diseñador escribe `casos_prueba.json` y el desarrollador propone un plan. Responde `si` para aprobarlo o escribe tus comentarios en una línea para que lo rehaga.
4. El desarrollador construye, el código se verifica, y despliegue y automatizador trabajan en paralelo.
5. Corren las pruebas de todas las historias. Si fallan, el triage elige quién corrige (hasta dos ciclos).
6. El resultado queda en `salida/HU-10/reporte.md`: **LISTA**, **ESCALAR A UNA PERSONA** o **BLOQUEADA POR SEGURIDAD**.

Si la ejecución se corta, vuelve a correr el mismo comando y responde `si` a «¿Reanudar?».

La aplicación queda en http://localhost:8080 y la documentación de la API en http://localhost:8000/docs.

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `historias/` | Historias de entrada (HU-99 es la historia envenenada de la demostración de seguridad) |
| `contexto/` | Reglas de negocio y convenciones de la app que leen los agentes |
| `agentes/` | Un archivo por agente, más `base.py` (bucle de agente) y `claude_code.py` (Agent SDK) |
| `flujos/` | Orquestadores de LangGraph por sesión y verificaciones deterministas |
| `seguridad/` | Hooks de rol y de seguridad |
| `app/` | Aplicación generada por los agentes (no se edita a mano) |
| `salida/` | Artefactos por historia: criterios, casos, reporte y decisiones |
| `evidencias/` | Evidencia del proceso del reto HU-10 |
| `ejemplos/` | Un programa corto por patrón visto en clase |

Cambios por versión en [`CHANGELOG.md`](CHANGELOG.md).

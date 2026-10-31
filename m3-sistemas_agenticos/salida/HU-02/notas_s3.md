# Notas · Sesión 3 · HU-02

## Ejecución

- `python -m flujos.flujo_s3 historias/HU-02-consultar-directorio.md`: app LISTA · 1.19 USD · 14 casos automatizados.
- El analista necesitó 2 intentos: el validador determinista rechazó el primero.
- El analista dejó 3 preguntas abiertas (búsqueda parcial, departamento inexistente, combinar búsqueda y filtro). Respondí «si» porque sus supuestos eran razonables.
- Aprobé el plan del desarrollador porque extendía HU-01 sin romperlo: parámetros opcionales en `listar_empleados`, sin cambios en esquemas ni modelos, y conservaba los `data-testid` existentes.
- Despliegue y automatizador arrancaron al mismo tiempo (paralelo). En la bitácora, «Pruebas automatizadas: OK» llegó antes que «Despliegue: OK», porque el automatizador no construye imágenes de Docker.

## docker compose ps

```text
NAME             IMAGE          COMMAND                  SERVICE    CREATED         STATUS                   PORTS
app-backend-1    app-backend    "uvicorn main:app --…"   backend    3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
app-frontend-1   app-frontend   "/docker-entrypoint.…"   frontend   3 minutes ago   Up 3 minutes             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
```

## Resultado de las pruebas

- API (`pytest tests/api -q`): 5 pasaron, 2 fallaron.
- E2E (`pytest tests/e2e -q --headed`): 6 pasaron, 1 falló.

| Prueba | Causa | Agente a corregir |
|---|---|---|
| CP-03 (API) | El caso busca «carlos ramirez» sin tilde y el empleado es «Ramírez». La historia solo pide ignorar mayúsculas, no acentos: el diseñador de pruebas agregó un requisito que nadie pidió. | Diseñador de pruebas |
| CP-04 (E2E) | El mismo problema de la tilde, visto desde el navegador: la app muestra «No se encontraron resultados». | Diseñador de pruebas |
| CP-11 (API) | La prueba da de baja al empleado escribiendo directo en SQLite desde la Mac y consulta la API de inmediato. Docker Desktop tarda en sincronizar el archivo compartido con el contenedor; minutos después la API sí mostraba «baja». | Automatizador |

Ninguna falla es un error de la app. El snapshot de Playwright muestra que el formulario «Registrar empleado» de HU-01 sigue en pantalla.

Pregunta abierta para una historia futura: en español, ¿la búsqueda debería ignorar acentos?

## Intento fuera de rol (buscar_denegados.py)

Ninguno: los agentes respetaron sus carpetas en esta ejecución.

## Auditoría

`desarrollador` 88 · `automatizador` 26 · `despliegue` 18 · `desarrollador-plan` 14 (acumulado con el Lab 2; cuenta intentos, no si se permitieron).

## 3A · ¿Por qué el automatizador puede ir en paralelo con el despliegue?

Porque para **escribir** las pruebas solo necesita `casos_prueba.json` y los `data-testid` de `app/CLAUDE.md`, y los dos existen antes del despliegue. No necesita la app corriendo: solo revisa la sintaxis con `--collect-only`. **Ejecutar** las pruebas sí requiere la app desplegada, y eso pasa después de que las dos ramas se juntan.

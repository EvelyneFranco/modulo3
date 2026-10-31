# Notas · Sesión 2 · Lab 2 (HU-01)

## Rechazo del primer plan

- **Comentario con que lo rechacé:** «no guarda el correo en minúsculas y valida el formato en el backend».
- **¿El segundo plan lo incorporó?** Sí, en las dos partes:
  - Minúsculas: en `backend/esquemas.py` un `field_validator` normaliza el correo con `correo.strip().lower()`, y la búsqueda de duplicados compara con `func.lower(correo)`.
  - Validación en el backend: el mismo validador revisa que termine en `@empresa.com` y responde 422; la validación del frontend queda solo como ayuda visual.
- **Lección:** mi comentario empezaba con «no», así que leído al pie de la letra podía entenderse al revés («no lo guardes en minúsculas»). El agente interpretó bien la intención, pero los comentarios a un agente deben ser instrucciones claras e imperativas.

## Criterios de aceptación (prueba manual en http://localhost:5173)

| Escenario | Resultado en la API | ¿Cumplido? |
| --- | --- | --- |
| Registro exitoso de un empleado con datos válidos | 201 Created y mensaje con el número de empleado | Cumplido |
| Correo ya existente, sin importar mayúsculas (`ANA.LOPEZ@empresa.com`) | 409 Conflict «El correo ya está registrado» | Cumplido |
| Correo que no es corporativo (`@gmail.com`) | 422 Unprocessable Entity | Cumplido |
| Otros datos inválidos · nombre de 1 carácter | 422 Unprocessable Entity | Cumplido |
| Otros datos inválidos · puesto de 1 carácter | 422 Unprocessable Entity | Cumplido |
| Otros datos inválidos · departamento fuera del catálogo | 422 Unprocessable Entity | Cumplido |
| Fecha de ingreso futura | 422 Unprocessable Entity | Cumplido |

**data-testid:** todos los de HU-01 en `contexto/convenciones_app.md` están en `app/frontend/src` (los 5 campos del formulario, `empleado-guardar`, `mensaje-exito`, `mensaje-error`). Los de búsqueda, edición y baja todavía no aparecen porque son de HU-02 y HU-03.

**Observación:** el plan agregó una tabla de directorio (`tabla-empleados`, `fila-empleado-{id}`), que en realidad es alcance de HU-02. El agente lo justificó como base mínima para ver el registro.

## Costo total

**1.70 USD**, según la bitácora: una sola construcción y verificación OK a la primera.

## Patrones de flujo en `flujos/flujo_s2.py`

| Patrón | Dónde aparece |
| --- | --- |
| Encadenamiento | `disenar_casos → planificar → aprobar_plan` y `construir → verificar`: aristas fijas (`add_edge`), la salida de un paso es la entrada del siguiente |
| Enrutamiento | `despues_de_analizar`: el código decide si va a `pedir_aclaracion` o directo a `disenar_casos` (`add_conditional_edges`) |
| Humano en el flujo | `pedir_aclaracion` y `aprobar_plan` usan `interrupt`; el checkpointer `InMemorySaver` guarda el estado mientras decido y `Command(resume=...)` continúa |
| Evaluador-optimizador | Ciclo `verificar ⇢ construir`: `verificar_app()` (código, sin LLM) juzga y `despues_de_verificar` reconstruye con el log del error, con tope `MAX_INTENTOS = 2` |

**¿Qué es «app LISTA»?** Solo que el backend arranca y `/api/salud` responde, y que el frontend compila con `npm run build`. No revisa las reglas de negocio; por eso hace falta la prueba manual de arriba y, en el Lab 3, las pruebas automáticas.
# Notas · Sesión 1 · Lab 1A

## ¿Por qué se presenta el PermissionError?

Las herramientas de archivos se crean con `herramientas_archivos(lectura, escritura)`, que recibe las carpetas permitidas. Antes de abrir o escribir cualquier archivo, cada herramienta llama a `_dentro_de`, que convierte la ruta en absoluta con `.resolve()` y la compara con esas carpetas. Si la ruta queda fuera, lanza `PermissionError` y el archivo nunca se toca.

Cada herramienta tiene su propia lista de permisos (mínimo privilegio):

| Prueba | Carpetas permitidas | Resultado |
| --- | --- | --- |
| `leer_archivo("historias/HU-01-registrar-empleado.md")` | `historias/`, `salida/HU-01/` | Funciona |
| `escribir_archivo("historias/prueba.txt")` | solo `salida/HU-01/` | `PermissionError`: el agente puede leer la historia, pero no modificarla |
| `leer_archivo("secretos_demo.txt")` | `historias/`, `salida/HU-01/` | `PermissionError`: el archivo está en la raíz, fuera de las dos carpetas |

## Conclusión

El límite lo pone el código, no el modelo. Aunque el modelo pida leer un secreto o escribir fuera de su carpeta (por error o por una instrucción maliciosa), `_dentro_de` lo impide. En el bucle del agente, ese error no se silencia: regresa al modelo como `tool_result` con `is_error: True` para que se corrija.

# Reporte · HU-10

**Estado:** LISTA
**Costo de agentes:** 1.56 USD
**Ciclos de corrección:** 0

## Bitácora
- Filtro de historia: OK
- Criterios escritos en criterios.feature
- Preguntas abiertas: la persona respondió 'si'
- Casos de prueba escritos en casos_prueba.json
- Plan rechazado: Agrega al plan: 1) el mensaje de éxito exacto en vacaciones-mensaje es "Solicitud registrada: N días hábiles. Te quedan M días hábiles en AAAA." 2) tras una solicitud exitosa, vacaciones-disponibles se actualiza con el nuevo saldo. 3) cumple_antiguedad acepta el aniversario exacto (mismo día y mes) y si fecha_ingreso es 29 de febrero el aniversario en año no bisiesto es el 1 de marzo. 4) se acepta si dias_habiles <= disponibles, y el error siempre dice "quedan N días hábiles" aunque N sea 1 o 0. El resto del plan está aprobado.
- Plan aprobado por una persona
- Construcción 1
- Verificación: OK
- Pruebas automatizadas: OK (21 casos)
- Despliegue: OK
- Despliegue y pruebas listos
- Pruebas E2E: 61 passed in 20.46s

## Última ejecución de pruebas
```
61 passed in 20.46s

```
# language: es
Característica: Solicitar vacaciones
  Como empleado de la empresa
  quiero solicitar días de vacaciones indicando una fecha de inicio y una de fin
  para que mi solicitud quede registrada y sepa cuántos días me quedan en el año

  Escenario: Solicitud válida que se registra y descuenta del saldo del año
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Y el empleado no tiene solicitudes de vacaciones registradas en 2026
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10"
    Entonces la API responde 201
    Y el campo "dias_habiles" de la respuesta es 5
    Y el campo "dias_restantes" de la respuesta es 7
    Y el elemento "vacaciones-mensaje" muestra "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."

  Escenario: Los sábados, domingos y festivos dentro del periodo no se descuentan
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Y el empleado no tiene solicitudes de vacaciones registradas en 2026
    Cuando solicita vacaciones del "2026-12-21" al "2026-12-31"
    Entonces la API responde 201
    Y el campo "dias_habiles" de la respuesta es 8
    Y el campo "dias_restantes" de la respuesta es 4
    Y el elemento "vacaciones-mensaje" muestra "Solicitud registrada: 8 días hábiles. Te quedan 4 días hábiles en 2026."

  Escenario: Un empleado que no existe no puede solicitar vacaciones
    Dado que no existe ningún empleado con id 9999
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10" para el empleado 9999
    Entonces la API responde 404
    Y el campo "detail" de la respuesta es "Empleado no encontrado"
    Y el elemento "vacaciones-mensaje" muestra "Empleado no encontrado"

  Escenario: Un empleado dado de baja no puede solicitar vacaciones
    Dado que existe el empleado con id 8, número "EMP-0008", fecha_ingreso "2020-01-15" y estado "baja"
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10"
    Entonces la API responde 409
    Y el campo "detail" de la respuesta es "No se pueden solicitar vacaciones para un empleado dado de baja"
    Y el elemento "vacaciones-mensaje" muestra "No se pueden solicitar vacaciones para un empleado dado de baja"

  Escenario: La fecha de fin no puede ser anterior a la fecha de inicio
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Cuando solicita vacaciones del "2026-07-10" al "2026-07-05"
    Entonces la API responde 400
    Y el campo "detail" de la respuesta es "La fecha de fin no puede ser anterior a la fecha de inicio"
    Y el elemento "vacaciones-mensaje" muestra "La fecha de fin no puede ser anterior a la fecha de inicio"

  Escenario: Un periodo no puede cruzar de un año a otro
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Cuando solicita vacaciones del "2026-12-28" al "2027-01-08"
    Entonces la API responde 400
    Y el campo "detail" de la respuesta es "Las vacaciones deben estar dentro de un mismo año calendario"
    Y el elemento "vacaciones-mensaje" muestra "Las vacaciones deben estar dentro de un mismo año calendario"

  Escenario: Un año fuera de la tabla de festivos se rechaza
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Cuando solicita vacaciones del "2028-07-06" al "2028-07-10"
    Entonces la API responde 400
    Y el campo "detail" de la respuesta es "Solo se pueden solicitar vacaciones en 2026 y 2027"
    Y el elemento "vacaciones-mensaje" muestra "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Un empleado con menos de un año de antigüedad no puede solicitar vacaciones
    Dado que existe el empleado con id 9, número "EMP-0009", fecha_ingreso "2026-01-10" y estado "activo"
    Cuando solicita vacaciones del "2026-06-01" al "2026-06-05"
    Entonces la API responde 400
    Y el campo "detail" de la respuesta es "Se requiere al menos un año de antigüedad a la fecha de inicio"
    Y el elemento "vacaciones-mensaje" muestra "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Un periodo sin ningún día hábil se rechaza
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Cuando solicita vacaciones del "2026-07-11" al "2026-07-12"
    Entonces la API responde 400
    Y el campo "detail" de la respuesta es "El periodo no incluye días hábiles"
    Y el elemento "vacaciones-mensaje" muestra "El periodo no incluye días hábiles"

  Escenario: Una solicitud que rebasa los días disponibles del año se rechaza indicando cuántos quedan
    Dado que existe el empleado con id 7, número "EMP-0007", fecha_ingreso "2024-03-10" y estado "activo"
    Y el empleado ya tiene registrada una solicitud de vacaciones del "2026-09-14" al "2026-09-18" con 4 días hábiles en 2026
    Cuando solicita vacaciones del "2026-11-02" al "2026-11-12"
    Entonces la API responde 400
    Y el campo "detail" de la respuesta es "La solicitud excede los días disponibles: quedan 8 días hábiles"
    Y el elemento "vacaciones-mensaje" muestra "La solicitud excede los días disponibles: quedan 8 días hábiles"

# Preguntas abiertas
# - No se especifica si dos solicitudes pueden tener periodos superpuestos para el mismo empleado; se asume que no se valida en esta historia.
# - No se especifica el comportamiento si fecha_inicio o fecha_fin faltan o tienen formato inválido más allá del 422 automático de FastAPI, por lo que no se agrega un escenario propio para ese caso.

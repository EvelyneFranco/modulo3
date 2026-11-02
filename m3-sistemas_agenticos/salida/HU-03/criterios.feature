# language: es
# HU-03 · Editar y dar de baja a un empleado

Característica: Editar y dar de baja a un empleado
  Como persona del área de Recursos Humanos
  quiero cambiar el puesto y el departamento de un empleado, y poder darlo de baja
  para mantener el directorio al día sin perder el historial

  Escenario: Editar puesto y departamento de un empleado activo
    Dado que existe el empleado "EMP-0001" con puesto "Analista Jr." y departamento "Ventas" en estado "activo"
    Cuando edito su puesto a "Analista Sr." y su departamento a "Finanzas"
    Entonces el sistema responde 200
    Y el empleado "EMP-0001" queda con puesto "Analista Sr." y departamento "Finanzas"

  Escenario: No se puede editar el número de empleado ni el correo
    Dado que existe el empleado "EMP-0002" con numero_empleado "EMP-0002" y correo "ana.lopez@empresa.com" en estado "activo"
    Cuando intento editar su numero_empleado a "EMP-0099" y su correo a "ana.nueva@empresa.com"
    Entonces el sistema responde 422
    Y la pantalla indica que los campos numero_empleado y correo no se pueden editar
    Y el empleado "EMP-0002" conserva numero_empleado "EMP-0002" y correo "ana.lopez@empresa.com"

  Escenario: Editar con un departamento que no está en la lista permitida
    Dado que existe el empleado "EMP-0003" con puesto "Soporte" y departamento "Operaciones" en estado "activo"
    Cuando edito su departamento a "Mercadotecnia"
    Entonces el sistema responde 422
    Y la pantalla muestra que el campo departamento debe corregirse

  Escenario: Dar de baja a un empleado activo
    Dado que existe el empleado "EMP-0004" con fecha_ingreso "2022-03-01" en estado "activo"
    Cuando doy de baja al empleado "EMP-0004" con fecha_baja "2024-05-10"
    Entonces el sistema responde 200
    Y el empleado "EMP-0004" queda con estado "baja" y fecha_baja "2024-05-10"
    Y el empleado "EMP-0004" sigue apareciendo en el directorio

  Escenario: Dar de baja con una fecha de baja anterior a la fecha de ingreso
    Dado que existe el empleado "EMP-0005" con fecha_ingreso "2023-01-15" en estado "activo"
    Cuando doy de baja al empleado "EMP-0005" con fecha_baja "2022-12-01"
    Entonces el sistema responde 422
    Y la pantalla muestra que el campo fecha_baja debe corregirse
    Y el empleado "EMP-0005" conserva estado "activo"

  Escenario: No se puede editar a un empleado ya dado de baja
    Dado que existe el empleado "EMP-0006" en estado "baja" con fecha_baja "2024-01-20"
    Cuando intento editar su puesto a "Coordinador"
    Entonces el sistema responde 409
    Y el mensaje es "No se puede editar a un empleado dado de baja"
    Y el empleado "EMP-0006" conserva su puesto original

# Preguntas abiertas
# - ¿El campo "nombre" también se puede editar en esta historia, o solo puesto y departamento?
# - ¿La fecha_ingreso se puede editar? Las reglas de negocio no lo indican para esta HU.
# - ¿Qué mensaje exacto debe mostrar la pantalla cuando fecha_baja es anterior a fecha_ingreso? Las reglas solo describen la restricción, no el texto del error.
# - ¿Se puede "reactivar" a un empleado dado de baja, o la baja es definitiva?

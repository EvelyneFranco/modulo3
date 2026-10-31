# language: es
Característica: Registrar empleado
  Como persona del área de Recursos Humanos
  Quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso
  Para darlo de alta en la empresa

  Escenario: Registro exitoso de un empleado con datos válidos
    Dado que no existe ningún empleado con correo "ana.lopez@empresa.com"
    Y el último número de empleado asignado es "EMP-0007"
    Cuando registro un empleado con nombre "Ana López", correo "Ana.Lopez@empresa.com", puesto "Analista de Datos", departamento "Tecnología" y fecha de ingreso "2024-03-01"
    Entonces el sistema responde con código 201
    Y el empleado queda registrado con número de empleado "EMP-0008"
    Y el correo del empleado se guarda como "ana.lopez@empresa.com"
    Y el estado del empleado es "activo"
    Y la pantalla muestra el mensaje de confirmación "Empleado EMP-0008 registrado con éxito"

  Escenario: No se puede registrar un empleado con un correo ya existente (sin importar mayúsculas)
    Dado que ya existe un empleado registrado con correo "carlos.ruiz@empresa.com"
    Cuando registro un empleado con nombre "Carlos Ruiz", correo "Carlos.Ruiz@EMPRESA.com", puesto "Vendedor", departamento "Ventas" y fecha de ingreso "2024-01-15"
    Entonces el sistema responde con código 409
    Y la pantalla muestra el mensaje "El correo ya está registrado"
    Y no se crea ningún empleado nuevo

  Escenario: No se puede registrar un empleado con un correo que no es corporativo
    Dado que no existe ningún empleado con correo "maria.gomez@gmail.com"
    Cuando registro un empleado con nombre "María Gómez", correo "maria.gomez@gmail.com", puesto "Contadora", departamento "Finanzas" y fecha de ingreso "2024-02-10"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "Usa el correo corporativo @empresa.com"
    Y no se crea ningún empleado nuevo

  Esquema del escenario: No se puede registrar un empleado con otros datos inválidos
    Dado que no existe ningún empleado con correo "<correo>"
    Cuando registro un empleado con nombre "<nombre>", correo "<correo>", puesto "<puesto>", departamento "<departamento>" y fecha de ingreso "<fecha_ingreso>"
    Entonces el sistema responde con código 422
    Y la pantalla indica que el campo "<campo_con_error>" debe corregirse
    Y no se crea ningún empleado nuevo

    Ejemplos:
      | nombre | correo                  | puesto             | departamento  | fecha_ingreso | campo_con_error |
      | A      | luis.diaz@empresa.com   | Diseñador          | Tecnología    | 2024-01-01    | nombre           |
      | Luis Díaz | laura.sote@empresa.com | D                | Ventas        | 2024-01-01    | puesto           |
      | Jorge Paz | jorge.paz@empresa.com | Supervisor         | Marketing     | 2024-01-01    | departamento     |

  Escenario: No se puede registrar un empleado con fecha de ingreso futura
    Dado que no existe ningún empleado con correo "pedro.sanz@empresa.com"
    Y la fecha actual del sistema es "2024-05-10"
    Cuando registro un empleado con nombre "Pedro Sanz", correo "pedro.sanz@empresa.com", puesto "Técnico", departamento "Operaciones" y fecha de ingreso "2024-06-01"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "La fecha de ingreso no puede ser futura"
    Y no se crea ningún empleado nuevo

# Preguntas abiertas
# - ¿Cuál es el mensaje exacto que debe mostrarse para cada campo inválido (nombre, puesto, departamento) según la regla 3?
#   Se asumió el texto genérico "la pantalla indica que el campo X debe corregirse" por falta de especificación.
# - ¿El departamento debe validarse contra una lista cerrada (enum) o puede ser texto libre siempre que esté en la lista?
#   Se asumió que es una lista cerrada según la tabla de reglas de negocio.
# - ¿Qué formato exacto debe tener el mensaje de confirmación mostrado tras el registro (texto literal)?
#   Se asumió un texto basado en la nota del product owner.

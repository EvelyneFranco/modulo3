# language: es
Característica: Registrar empleado
  Como persona del área de Recursos Humanos
  quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso
  para darlo de alta en la empresa

  Escenario: Registro exitoso de un empleado con datos válidos
    Dado que no existe ningún empleado con correo "ana.lopez@empresa.com"
    Y el último número de empleado asignado es "EMP-0007"
    Cuando registro un empleado con nombre "Ana López", correo "Ana.Lopez@Empresa.com", puesto "Analista de Datos", departamento "Tecnología" y fecha de ingreso "2024-03-01"
    Entonces el sistema responde con código 201
    Y el empleado queda registrado con número de empleado "EMP-0008"
    Y el correo del empleado se guarda como "ana.lopez@empresa.com"
    Y el estado del empleado es "activo"
    Y la pantalla muestra el mensaje de confirmación "Empleado EMP-0008 registrado con éxito"

  Escenario: No se puede registrar con un correo ya existente, sin importar mayúsculas
    Dado que ya existe un empleado registrado con correo "ana.lopez@empresa.com"
    Cuando registro un empleado con correo "ANA.LOPEZ@EMPRESA.COM" y los demás datos válidos
    Entonces el sistema responde con código 409
    Y la pantalla muestra el mensaje "El correo ya está registrado"
    Y no se crea ningún empleado nuevo

  Escenario: No se puede registrar con un correo que no es corporativo
    Dado que voy a registrar un nuevo empleado con datos por lo demás válidos
    Cuando registro un empleado con correo "ana.lopez@gmail.com"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "Usa el correo corporativo @empresa.com"
    Y no se crea ningún empleado nuevo

  Esquema del escenario: No se puede registrar con otros datos inválidos
    Dado que voy a registrar un nuevo empleado con datos por lo demás válidos
    Cuando registro un empleado con <campo> igual a "<valor>"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el campo "<campo>" como el campo a corregir
    Y no se crea ningún empleado nuevo

    Ejemplos:
      | campo         | valor                  |
      | nombre        | A                      |
      | nombre        |                        |
      | puesto        | A                      |
      | departamento  | Marketing              |
      | fecha_ingreso |                        |

  Escenario: No se puede registrar con una fecha de ingreso futura
    Dado que la fecha actual del sistema es "2024-05-10"
    Y voy a registrar un nuevo empleado con datos por lo demás válidos
    Cuando registro un empleado con fecha de ingreso "2024-05-11"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "La fecha de ingreso no puede ser futura"
    Y no se crea ningún empleado nuevo

# Preguntas abiertas
# - No se especifica el límite exacto de longitud a validar en los mensajes de error de nombre y puesto
#   (ej. si 1 carácter o 81 caracteres deben mostrar un texto específico distinto al genérico "campo a corregir").
# - No se especifica si el campo "fecha_ingreso" vacío debe mostrar el mismo mensaje genérico de la regla 3
#   o un mensaje propio de "campo obligatorio".
# - No se especifica el texto exacto del mensaje de confirmación mostrado en pantalla tras guardar
#   (se asumió un formato "Empleado {numero_empleado} registrado con éxito").

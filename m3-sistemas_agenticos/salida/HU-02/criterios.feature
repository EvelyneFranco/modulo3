# language: es
Característica: Consultar el directorio de empleados
  Como persona del área de Recursos Humanos
  quiero ver el directorio de empleados, buscarlos por nombre o correo y filtrarlos por departamento
  para encontrar rápido a una persona

  Escenario: Ver el directorio con los datos principales de cada empleado
    Dado que existe el empleado "EMP-0001" con nombre "Laura Gómez", puesto "Analista de Nómina", departamento "Recursos Humanos" y estado "activo"
    Cuando abro el directorio de empleados
    Entonces veo una fila con el número de empleado "EMP-0001"
    Y la fila muestra el nombre "Laura Gómez"
    Y la fila muestra el puesto "Analista de Nómina"
    Y la fila muestra el departamento "Recursos Humanos"
    Y la fila muestra el estado "activo"

  Escenario: Buscar por nombre en minúsculas encuentra coincidencias sin importar mayúsculas
    Dado que existe el empleado "EMP-0002" con nombre "Carlos Ramírez" y correo "carlos.ramirez@empresa.com"
    Cuando busco en el directorio el texto "carlos ramirez"
    Entonces veo en los resultados al empleado "EMP-0002"

  Escenario: Buscar por correo en mayúsculas encuentra coincidencias sin importar mayúsculas
    Dado que existe el empleado "EMP-0003" con nombre "Ana Torres" y correo "ana.torres@empresa.com"
    Cuando busco en el directorio el texto "ANA.TORRES@EMPRESA.COM"
    Entonces veo en los resultados al empleado "EMP-0003"

  Escenario: Filtrar por departamento muestra solo a los empleados de ese departamento
    Dado que existen los empleados:
      | numero_empleado | nombre          | departamento      |
      | EMP-0004        | Pedro Salinas   | Ventas            |
      | EMP-0005        | Mónica Lira     | Tecnología        |
    Cuando filtro el directorio por el departamento "Ventas"
    Entonces veo en los resultados al empleado "EMP-0004"
    Y no veo en los resultados al empleado "EMP-0005"

  Escenario: Buscar un texto sin coincidencias muestra un mensaje de sin resultados
    Dado que existe el empleado "EMP-0006" con nombre "Sofía Mendoza" y correo "sofia.mendoza@empresa.com"
    Cuando busco en el directorio el texto "inexistente"
    Entonces veo el mensaje "No se encontraron resultados"

  Escenario: Un empleado dado de baja sigue apareciendo en el directorio
    Dado que existe el empleado "EMP-0007" con nombre "Jorge Nieto", estado "baja" y fecha de baja "2024-03-10"
    Cuando abro el directorio de empleados
    Entonces veo en los resultados al empleado "EMP-0007"
    Y la fila muestra el estado "baja"

  Escenario: Combinar búsqueda y filtro de departamento sin coincidencias muestra un mensaje de sin resultados
    Dado que existe el empleado "EMP-0008" con nombre "Luis Peña", departamento "Finanzas" y correo "luis.pena@empresa.com"
    Cuando filtro el directorio por el departamento "Operaciones"
    Y busco en el directorio el texto "Luis Peña"
    Entonces veo el mensaje "No se encontraron resultados"

# Preguntas abiertas
# - No se especifica si la búsqueda por nombre o correo requiere coincidencia exacta o parcial; se asumió coincidencia parcial (contiene el texto).
# - No se especifica el comportamiento al filtrar por un departamento que no existe en el catálogo (Tecnología, Ventas, Finanzas, Recursos Humanos, Operaciones); no se incluyó escenario por falta de definición.
# - No se especifica si la búsqueda y el filtro de departamento se pueden combinar simultáneamente; se asumió que sí, según el escenario de combinación.

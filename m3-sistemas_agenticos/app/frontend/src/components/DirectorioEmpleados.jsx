function DirectorioEmpleados({
  empleados,
  departamentos,
  buscar,
  onCambiarBuscar,
  departamento,
  onCambiarDepartamento,
  onEditar,
  onBaja,
}) {
  return (
    <section>
      <h2>Directorio de empleados</h2>
      <div>
        <label htmlFor="buscar-empleados">Buscar</label>
        <input
          id="buscar-empleados"
          data-testid="buscar-empleados"
          value={buscar}
          onChange={(evento) => onCambiarBuscar(evento.target.value)}
          placeholder="Nombre o correo"
        />
      </div>
      <div>
        <label htmlFor="filtro-departamento">Departamento</label>
        <select
          id="filtro-departamento"
          data-testid="filtro-departamento"
          value={departamento}
          onChange={(evento) => onCambiarDepartamento(evento.target.value)}
        >
          <option value="">Todos</option>
          {departamentos.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>
      {empleados.length === 0 ? (
        <p data-testid="sin-resultados">No se encontraron resultados</p>
      ) : (
        <table data-testid="tabla-empleados">
          <thead>
            <tr>
              <th>Número</th>
              <th>Nombre</th>
              <th>Correo</th>
              <th>Puesto</th>
              <th>Departamento</th>
              <th>Fecha de ingreso</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empleados.map((empleado) => (
              <tr key={empleado.id} data-testid={`fila-empleado-${empleado.id}`}>
                <td data-testid={`numero-empleado-${empleado.id}`}>{empleado.numero_empleado}</td>
                <td>{empleado.nombre}</td>
                <td>{empleado.correo}</td>
                <td>{empleado.puesto}</td>
                <td>{empleado.departamento}</td>
                <td>{empleado.fecha_ingreso}</td>
                <td data-testid={`estado-empleado-${empleado.id}`}>
                  {empleado.estado === "activo" ? "Activo" : "Baja"}
                </td>
                <td>
                  <button
                    data-testid={`editar-empleado-${empleado.id}`}
                    onClick={() => onEditar(empleado)}
                  >
                    Editar
                  </button>
                  <button
                    data-testid={`baja-empleado-${empleado.id}`}
                    onClick={() => onBaja(empleado)}
                  >
                    Dar de baja
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default DirectorioEmpleados;

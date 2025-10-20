import React from "react";
import { Table, Spinner } from "react-bootstrap";

function ResultsTable({ results, loading }) {
  if (loading)
    return (
      <div className="text-center">
        <Spinner animation="border" />
      </div>
    );
  if (!results.length)
    return <p className="text-muted text-center">No se encontraron viajes.</p>;

  return (
    <Table bordered hover responsive>
      <thead>
        <tr>
          <th>#</th>
          <th>Conexiones</th>
          <th>Ruta</th>
          <th>Vuelos</th>
          <th>Salida</th>
          <th>Llegada</th>
        </tr>
      </thead>
      <tbody>
        {results.map((journey, index) => {
          // Construir la ruta con from_ y to
          const path = journey.path
            .map((f) => `${f.from_ || "N/A"} → ${f.to || "N/A"}`)
            .join(", ");

          // Números de vuelo
          const flights = journey.path
            .map((f) => f.flight_number || "N/A")
            .join(", ");

          // Horarios de salida y llegada
          const departure = journey.path[0]?.departure_time || "N/A";
          const arrival =
            journey.path[journey.path.length - 1]?.arrival_time || "N/A";

          return (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{journey.connections}</td>
              <td>{path}</td>
              <td>{flights}</td>
              <td>{departure}</td>
              <td>{arrival}</td>
            </tr>
          );
        })}
      </tbody>
    </Table>
  );
}

export default ResultsTable;

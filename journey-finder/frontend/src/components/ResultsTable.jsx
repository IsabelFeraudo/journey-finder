/**
 * ResultsTable Component - Journey Search Results Display
 *
 * Displays search results in a table format showing:
 * - Journey number, connections count, route path, departure and arrival times
 * - Shows loading spinner while fetching data
 * - Displays "No journeys found" message when no results
 * - Formats route paths as "City1 → City2, City2 → City3" format
 */
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
          <th>Salida</th>
          <th>Llegada</th>
        </tr>
      </thead>
      <tbody>
        {results.map((journey, index) => {
          const path = journey.path
            .map((f) => `${f.from} → ${f.to}`)
            .join(", ");
          const departure = journey.path[0]?.departure_time;
          const arrival = journey.path[journey.path.length - 1]?.arrival_time;
          return (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{journey.connections}</td>
              <td>{path}</td>
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

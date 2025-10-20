/**
 * SearchForm Component - Journey Search Interface
 *
 * A form component that allows users to search for journeys by entering:
 * - Origin city name (full name)
 * - Destination city name (full name)
 * - Departure date
 *
 * When submitted, it calls the onSearch prop with the form data.
 */
import React, { useState } from "react";
import { Form, Button, Row, Col } from "react-bootstrap";

function SearchForm({ onSearch }) {
  const [formData, setFormData] = useState({
    from: "",
    to: "",
    date: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value.toUpperCase() });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { from, to, date } = formData;

    // Validación: solo códigos de 3 letras y fecha no vacía
    if (!/^[A-Z]{3}$/.test(from) || !/^[A-Z]{3}$/.test(to)) {
      alert("Ingrese códigos de aeropuerto válidos de 3 letras");
      return;
    }
    if (!date) {
      alert("Ingrese una fecha de partida");
      return;
    }

    onSearch(formData);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Row className="mb-3">
        <Col>
          <Form.Label>Código de Origen</Form.Label>
          <Form.Control
            name="from"
            value={formData.from}
            onChange={handleChange}
            placeholder="Ej: MAD"
            required
            maxLength={3}
            pattern="[A-Za-z]{3}"
            title="Ingrese un código de aeropuerto de 3 letras"
          />
        </Col>
        <Col>
          <Form.Label>Código de Destino</Form.Label>
          <Form.Control
            name="to"
            value={formData.to}
            onChange={handleChange}
            placeholder="Ej: NYC"
            required
            maxLength={3}
            pattern="[A-Za-z]{3}"
            title="Ingrese un código de aeropuerto de 3 letras"
          />
        </Col>
      </Row>
      <Form.Group className="mb-3">
        <Form.Label>Fecha de partida</Form.Label>
        <Form.Control
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
      </Form.Group>
      <div className="text-center">
        <Button variant="primary" type="submit">
          Buscar viajes
        </Button>
      </div>
    </Form>
  );
}

export default SearchForm;

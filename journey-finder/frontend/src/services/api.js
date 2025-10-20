/**
 * Servicio API - Integración con la API de Búsqueda de Viajes
 * Maneja la comunicación con el backend para la funcionalidad de búsqueda de viajes
 * Proporciona una función para buscar viajes enviando solicitudes GET al
 * servicio backend con los parámetros de búsqueda
 */

import axios from "axios";

const API_URL = "http://localhost:8000/journeys/search";

export const searchJourneys = (params) => {
  return axios.get(API_URL, { params });
};

import time
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import config
from airports_db import get_airport_info
from accommodation_db import estimate_accommodation
from providers import build_flight_provider_links, build_hotel_provider_links


class AmadeusClient:
    """Cliente para interactuar con la API de Amadeus for Developers."""

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, env: Optional[str] = None):
        self.client_id = client_id or config.AMADEUS_CLIENT_ID
        self.client_secret = client_secret or config.AMADEUS_CLIENT_SECRET
        self.env = env or config.AMADEUS_ENV
        
        self.base_url = (
            "https://api.amadeus.com"
            if self.env == "production"
            else "https://test.api.amadeus.com"
        )
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0.0

    def _get_token(self) -> str:
        """Obtiene o renueva el token de acceso OAuth2 de Amadeus."""
        if self._access_token and time.time() < self._token_expiry - 60:
            return self._access_token

        token_url = f"{self.base_url}/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(token_url, headers=headers, data=data, timeout=15)
        if response.status_code != 200:
            raise RuntimeError(
                f"Error al autenticar con Amadeus ({response.status_code}): {response.text}\n"
                f"Verifica tus credenciales en el archivo .env (AMADEUS_CLIENT_ID y AMADEUS_CLIENT_SECRET)."
            )

        json_data = response.json()
        self._access_token = json_data["access_token"]
        self._token_expiry = time.time() + json_data.get("expires_in", 1799)
        return self._access_token

    def search_cheapest_destinations(
        self,
        origin: str,
        departure_date_range: Optional[str] = None,
        min_duration: int = 5,
        max_duration: int = 9,
        max_price: Optional[int] = None,
        view_by: str = "DESTINATION"
    ) -> List[Dict[str, Any]]:
        """
        Explora los destinos más baratos del mundo con duración flexible.
        """
        token = self._get_token()
        url = f"{self.base_url}/v1/shopping/flight-destinations"
        headers = {"Authorization": f"Bearer {token}"}
        
        duration_param = f"{min_duration},{max_duration}" if min_duration != max_duration else str(min_duration)
        
        params: Dict[str, Any] = {
            "origin": origin.upper(),
            "oneWay": "false",
            "viewBy": view_by,
            "duration": duration_param
        }
        
        if departure_date_range:
            params["departureDate"] = departure_date_range
        if max_price:
            params["maxPrice"] = max_price

        resp = requests.get(url, headers=headers, params=params, timeout=20)
        
        if resp.status_code == 400:
            err = resp.json()
            raise ValueError(f"Error en la petición a Amadeus: {err}")
        elif resp.status_code != 200:
            raise RuntimeError(f"Error de Amadeus ({resp.status_code}): {resp.text}")

        data = resp.json().get("data", [])
        return self._format_results(data, min_duration, max_duration)

    def _format_results(self, raw_data: List[Dict[str, Any]], min_duration: int, max_duration: int) -> List[Dict[str, Any]]:
        """Formatea y enriquece los resultados con detalles de aeropuertos, horarios, alojamiento y múltiples enlaces."""
        results = []
        for item in raw_data:
            dest_code = item.get("destination", "")
            orig_code = item.get("origin", "")
            airport_info = get_airport_info(dest_code)
            origin_info = get_airport_info(orig_code)
            
            flight_price = float(item.get("price", {}).get("total", 0.0))
            dep_date = item.get("departureDate", "")
            ret_date = item.get("returnDate", "")
            
            duration_days = 7
            try:
                d1 = datetime.strptime(dep_date, "%Y-%m-%d").date()
                d2 = datetime.strptime(ret_date, "%Y-%m-%d").date()
                duration_days = (d2 - d1).days
            except Exception:
                duration_days = min_duration

            if not (min_duration <= duration_days <= max_duration):
                continue
            
            out_h = 2.5 if airport_info["continent"] == "Europa" else 8.0
            ret_h = out_h
            out_airline = "Iberia / Ryanair"
            ret_airline = "Vueling / EasyJet"

            # Estimación de alojamiento
            hotel_data = estimate_accommodation(dest_code, airport_info["continent"], duration_days)
            trip_total = round(flight_price + hotel_data["hotel_total_est"], 2)

            # Múltiples proveedores y enlaces
            flight_links = build_flight_provider_links(orig_code, dest_code, dep_date, ret_date, out_airline, ret_airline)
            hotel_links = build_hotel_provider_links(airport_info["city"], airport_info["country"], dep_date, ret_date)

            results.append({
                "origin": orig_code,
                "origin_city": origin_info["city"],
                "origin_country": origin_info["country"],
                "origin_flag": origin_info["flag"],
                "destination": dest_code,
                "dest_city": airport_info["city"],
                "dest_country": airport_info["country"],
                "dest_flag": airport_info["flag"],
                "continent": airport_info["continent"],
                "departure_date": dep_date,
                "return_date": ret_date,
                "duration_days": duration_days,
                # Horarios y aerolíneas
                "outbound_dep_time": "09:30",
                "outbound_arr_time": "12:00",
                "outbound_duration_hours": out_h,
                "outbound_duration_str": f"{int(out_h)}h {int((out_h % 1) * 60):02d}m",
                "outbound_airline": out_airline,
                "return_dep_time": "18:45",
                "return_arr_time": "21:15",
                "return_duration_hours": ret_h,
                "return_duration_str": f"{int(ret_h)}h {int((ret_h % 1) * 60):02d}m",
                "return_airline": ret_airline,
                "different_airlines": True,
                "price": flight_price,
                "currency": config.DEFAULT_CURRENCY,
                # Alojamiento estimado
                "hotel_price_per_night": hotel_data["hotel_price_per_night"],
                "hotel_nights": hotel_data["hotel_nights"],
                "hotel_total_est": hotel_data["hotel_total_est"],
                "hotel_tier": hotel_data["hotel_tier"],
                "hotel_note": hotel_data["hotel_note"],
                "trip_total_est": trip_total,
                # Múltiples proveedores y webs oficiales
                "direct_link": flight_links["google_flights"],
                "skyscanner_link": flight_links["skyscanner"],
                "kayak_link": flight_links["kayak"],
                "kiwi_link": flight_links["kiwi"],
                "momondo_link": flight_links["momondo"],
                "outbound_airline_url": flight_links["outbound_airline_url"],
                "return_airline_url": flight_links["return_airline_url"],
                "booking_link": hotel_links["booking"],
                "airbnb_link": hotel_links["airbnb"],
                "google_hotels_link": hotel_links["google_hotels"]
            })

        results.sort(key=lambda x: x["price"])
        return results

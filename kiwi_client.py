import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import config
from airports_db import get_airport_info
from accommodation_db import estimate_accommodation
from providers import build_flight_provider_links, build_hotel_provider_links


class KiwiClient:
    """Cliente para la API de Kiwi (Tequila), con estimación de alojamiento y enlaces multi-proveedor."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.KIWI_API_KEY
        self.base_url = "https://api.tequila.kiwi.com/v2"

    def search_anywhere(
        self,
        origin: str,
        date_from: str = "01/01/2027",
        date_to: str = "31/10/2027",
        min_nights: int = 5,
        max_nights: int = 9,
        max_price: Optional[int] = None,
        limit: int = 50,
        currency: str = "EUR"
    ) -> List[Dict[str, Any]]:
        """
        Busca vuelos hacia 'Cualquier parte del mundo' con duración flexible.
        """
        if not self.api_key:
            raise ValueError("Falta la API Key de Kiwi (KIWI_API_KEY en .env).")

        url = f"{self.base_url}/search"
        headers = {"apikey": self.api_key}
        
        params: Dict[str, Any] = {
            "fly_from": origin.upper(),
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": min_nights,
            "nights_in_dst_to": max_nights,
            "flight_type": "round",
            "curr": currency,
            "sort": "price",
            "limit": limit,
            "one_for_city": 1,
        }

        if max_price:
            params["price_to"] = max_price

        resp = requests.get(url, headers=headers, params=params, timeout=25)
        if resp.status_code != 200:
            raise RuntimeError(f"Error de Kiwi API ({resp.status_code}): {resp.text}")

        data = resp.json().get("data", [])
        return self._format_results(data, currency, min_nights)

    def _format_results(self, raw_data: List[Dict[str, Any]], currency: str, fallback_duration: int) -> List[Dict[str, Any]]:
        results = []
        for item in raw_data:
            dest_code = item.get("flyTo", "")
            orig_code = item.get("flyFrom", "")
            
            origin_info = get_airport_info(orig_code)
            dest_info = get_airport_info(dest_code)

            route = item.get("route", [])
            departure_date = ""
            return_date = ""
            out_dep_time = ""
            out_arr_time = ""
            ret_dep_time = ""
            ret_arr_time = ""
            out_airline = "Varios"
            ret_airline = "Varios"

            out_legs = [leg for leg in route if leg.get("return", 0) == 0]
            ret_legs = [leg for leg in route if leg.get("return", 0) == 1]

            if out_legs:
                dep_raw = out_legs[0].get("local_departure", "")
                arr_raw = out_legs[-1].get("local_arrival", "")
                departure_date = dep_raw[:10]
                out_dep_time = dep_raw[11:16] if len(dep_raw) >= 16 else ""
                out_arr_time = arr_raw[11:16] if len(arr_raw) >= 16 else ""
                out_airline = out_legs[0].get("airline", "Varios")

            if ret_legs:
                dep_raw = ret_legs[0].get("local_departure", "")
                arr_raw = ret_legs[-1].get("local_arrival", "")
                return_date = dep_raw[:10]
                ret_dep_time = dep_raw[11:16] if len(dep_raw) >= 16 else ""
                ret_arr_time = arr_raw[11:16] if len(arr_raw) >= 16 else ""
                ret_airline = ret_legs[0].get("airline", "Varios")

            dur_info = item.get("duration", {})
            out_sec = dur_info.get("departure", 0)
            ret_sec = dur_info.get("return", 0)
            out_h = round(out_sec / 3600, 2) if out_sec else 2.5
            ret_h = round(ret_sec / 3600, 2) if ret_sec else 2.5

            duration_days = fallback_duration
            try:
                d1 = datetime.strptime(departure_date, "%Y-%m-%d").date()
                d2 = datetime.strptime(return_date, "%Y-%m-%d").date()
                duration_days = (d2 - d1).days
            except Exception:
                duration_days = item.get("nightsInDest", fallback_duration)

            flight_price = float(item.get("price", 0.0))

            # Estimación de alojamiento
            hotel_data = estimate_accommodation(dest_code, dest_info["continent"], duration_days)
            trip_total = round(flight_price + hotel_data["hotel_total_est"], 2)

            # Múltiples proveedores y enlaces directos
            flight_links = build_flight_provider_links(orig_code, dest_code, departure_date, return_date, out_airline, ret_airline)
            hotel_links = build_hotel_provider_links(dest_info["city"], dest_info["country"], departure_date, return_date)

            results.append({
                "origin": orig_code,
                "origin_city": origin_info["city"],
                "origin_country": origin_info["country"],
                "origin_flag": origin_info["flag"],
                "destination": dest_code,
                "dest_city": item.get("cityTo", dest_info["city"]),
                "dest_country": item.get("countryTo", {}).get("name", dest_info["country"]),
                "dest_flag": dest_info["flag"],
                "continent": dest_info["continent"],
                "departure_date": departure_date,
                "return_date": return_date,
                "duration_days": duration_days,
                # Horarios y aerolíneas
                "outbound_dep_time": out_dep_time or "09:00",
                "outbound_arr_time": out_arr_time or "11:30",
                "outbound_duration_hours": out_h,
                "outbound_duration_str": f"{int(out_h)}h {int((out_h % 1) * 60):02d}m",
                "outbound_airline": out_airline,
                "return_dep_time": ret_dep_time or "18:00",
                "return_arr_time": ret_arr_time or "20:30",
                "return_duration_hours": ret_h,
                "return_duration_str": f"{int(ret_h)}h {int((ret_h % 1) * 60):02d}m",
                "return_airline": ret_airline,
                "different_airlines": out_airline != ret_airline,
                "price": flight_price,
                "currency": currency,
                # Alojamiento estimado
                "hotel_price_per_night": hotel_data["hotel_price_per_night"],
                "hotel_nights": hotel_data["hotel_nights"],
                "hotel_total_est": hotel_data["hotel_total_est"],
                "hotel_tier": hotel_data["hotel_tier"],
                "hotel_note": hotel_data["hotel_note"],
                "trip_total_est": trip_total,
                # Múltiples comparadores y aerolíneas oficiales
                "direct_link": flight_links["google_flights"],
                "skyscanner_link": flight_links["skyscanner"],
                "kayak_link": flight_links["kayak"],
                "kiwi_link": item.get("deep_link") or flight_links["kiwi"],
                "momondo_link": flight_links["momondo"],
                "outbound_airline_url": flight_links["outbound_airline_url"],
                "return_airline_url": flight_links["return_airline_url"],
                "booking_link": hotel_links["booking"],
                "airbnb_link": hotel_links["airbnb"],
                "google_hotels_link": hotel_links["google_hotels"]
            })

        results.sort(key=lambda x: x["price"])
        return results

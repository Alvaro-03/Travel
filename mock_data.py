"""
Generador de datos de prueba para modo demostración.
Incluye horarios de salida/llegada, duraciones de vuelo por trayecto, aerolíneas,
estimación de costes de alojamiento y enlaces a múltiples buscadores / aerolíneas.
"""

from typing import List, Dict, Any
from airports_db import get_airport_info
from accommodation_db import estimate_accommodation
from providers import build_flight_provider_links, build_hotel_provider_links


def get_demo_flights(
    origin: str = "MAD",
    year: int = 2027,
    min_duration: int = 5,
    max_duration: int = 9
) -> List[Dict[str, Any]]:
    origin_info = get_airport_info(origin)
    
    # Destinos con variedad de horarios, duración de vuelo y aerolíneas combinadas
    sample_destinations = [
        # Europa cercana
        {
            "dest": "OPO", "month": 3, "day": 10, "stay": 5, "price": 28.0,
            "out_dep": "09:15", "out_arr": "10:35", "out_h": 1.33, "out_air": "Ryanair",
            "ret_dep": "18:40", "ret_arr": "20:00", "ret_h": 1.33, "ret_air": "EasyJet"
        },
        {
            "dest": "IBZ", "month": 4, "day": 14, "stay": 6, "price": 32.0,
            "out_dep": "07:30", "out_arr": "08:45", "out_h": 1.25, "out_air": "Vueling",
            "ret_dep": "21:15", "ret_arr": "22:30", "ret_h": 1.25, "ret_air": "Ryanair"
        },
        {
            "dest": "MRS", "month": 2, "day": 18, "stay": 7, "price": 39.0,
            "out_dep": "11:20", "out_arr": "13:05", "out_h": 1.75, "out_air": "Ryanair",
            "ret_dep": "16:45", "ret_arr": "18:30", "ret_h": 1.75, "ret_air": "Volotea"
        },
        {
            "dest": "LIS", "month": 5, "day": 5,  "stay": 8, "price": 44.0,
            "out_dep": "08:00", "out_arr": "09:20", "out_h": 1.33, "out_air": "TAP Portugal",
            "ret_dep": "19:30", "ret_arr": "20:50", "ret_h": 1.33, "ret_air": "EasyJet"
        },
        {
            "dest": "CRL", "month": 3, "day": 24, "stay": 9, "price": 49.0,
            "out_dep": "06:45", "out_arr": "09:10", "out_h": 2.41, "out_air": "Ryanair",
            "ret_dep": "20:10", "ret_arr": "22:35", "ret_h": 2.41, "ret_air": "Brussels Airlines"
        },
        {
            "dest": "BGY", "month": 4, "day": 21, "stay": 6, "price": 52.0,
            "out_dep": "10:15", "out_arr": "12:35", "out_h": 2.33, "out_air": "Ryanair",
            "ret_dep": "17:20", "ret_arr": "19:40", "ret_h": 2.33, "ret_air": "Wizz Air"
        },
        {
            "dest": "LGW", "month": 5, "day": 12, "stay": 7, "price": 58.0,
            "out_dep": "08:45", "out_arr": "10:15", "out_h": 2.50, "out_air": "EasyJet",
            "ret_dep": "18:00", "ret_arr": "21:30", "ret_h": 2.50, "ret_air": "British Airways"
        },
        {
            "dest": "BVA", "month": 6, "day": 2,  "stay": 8, "price": 64.0,
            "out_dep": "09:00", "out_arr": "11:10", "out_h": 2.16, "out_air": "Ryanair",
            "ret_dep": "19:40", "ret_arr": "21:50", "ret_h": 2.16, "ret_air": "Vueling"
        },
        {
            "dest": "RAK", "month": 4, "day": 7,  "stay": 5, "price": 75.0,
            "out_dep": "10:30", "out_arr": "12:45", "out_h": 2.25, "out_air": "Ryanair",
            "ret_dep": "14:15", "ret_arr": "16:30", "ret_h": 2.25, "ret_air": "Iberia Express"
        },
        {
            "dest": "PRG", "month": 5, "day": 19, "stay": 7, "price": 89.0,
            "out_dep": "07:15", "out_arr": "10:15", "out_h": 3.00, "out_air": "Smartwings",
            "ret_dep": "16:30", "ret_arr": "19:30", "ret_h": 3.00, "ret_air": "Eurowings"
        },
        {
            "dest": "BUD", "month": 6, "day": 9,  "stay": 6, "price": 95.0,
            "out_dep": "14:30", "out_arr": "17:40", "out_h": 3.16, "out_air": "Wizz Air",
            "ret_dep": "11:00", "ret_arr": "14:10", "ret_h": 3.16, "ret_air": "Ryanair"
        },
        {
            "dest": "KRK", "month": 9, "day": 15, "stay": 8, "price": 98.0,
            "out_dep": "08:20", "out_arr": "11:50", "out_h": 3.50, "out_air": "Ryanair",
            "ret_dep": "18:15", "ret_arr": "21:45", "ret_h": 3.50, "ret_air": "Wizz Air"
        },
        {
            "dest": "FCO", "month": 6, "day": 16, "stay": 7, "price": 105.0,
            "out_dep": "06:30", "out_arr": "09:00", "out_h": 2.50, "out_air": "Ryanair",
            "ret_dep": "20:45", "ret_arr": "23:15", "ret_h": 2.50, "ret_air": "ITA Airways"
        },
        {
            "dest": "ATH", "month": 9, "day": 22, "stay": 9, "price": 120.0,
            "out_dep": "11:45", "out_arr": "16:15", "out_h": 3.50, "out_air": "Aegean Airlines",
            "ret_dep": "17:30", "ret_arr": "20:00", "ret_h": 3.50, "ret_air": "Iberia"
        },
        {
            "dest": "CPH", "month": 7, "day": 7,  "stay": 6, "price": 135.0,
            "out_dep": "12:10", "out_arr": "15:35", "out_h": 3.41, "out_air": "Norwegian",
            "ret_dep": "19:00", "ret_arr": "22:25", "ret_h": 3.41, "ret_air": "SAS"
        },
        {
            "dest": "KEF", "month": 8, "day": 18, "stay": 8, "price": 185.0,
            "out_dep": "21:30", "out_arr": "00:15", "out_h": 4.75, "out_air": "Play Airlines",
            "ret_dep": "14:00", "ret_arr": "18:45", "ret_h": 4.75, "ret_air": "Iberia Express"
        },

        # Vuelos de media/larga distancia
        {
            "dest": "CAI", "month": 3, "day": 15, "stay": 8, "price": 210.0,
            "out_dep": "15:45", "out_arr": "21:15", "out_h": 4.50, "out_air": "EgyptAir",
            "ret_dep": "09:30", "ret_arr": "13:00", "ret_h": 4.50, "ret_air": "Vueling"
        },
        {
            "dest": "BOS", "month": 3, "day": 2,  "stay": 7, "price": 290.0,
            "out_dep": "12:30", "out_arr": "15:00", "out_h": 7.50, "out_air": "Level",
            "ret_dep": "17:15", "ret_arr": "06:20", "ret_h": 7.08, "ret_air": "Iberia"
        },
        {
            "dest": "JFK", "month": 4, "day": 6,  "stay": 8, "price": 315.0,
            "out_dep": "10:15", "out_arr": "13:00", "out_h": 8.75, "out_air": "Air Europa",
            "ret_dep": "19:30", "ret_arr": "08:50", "ret_h": 7.33, "ret_air": "Delta Air Lines"
        },
        {
            "dest": "DXB", "month": 4, "day": 12, "stay": 7, "price": 320.0,
            "out_dep": "14:25", "out_arr": "23:55", "out_h": 6.50, "out_air": "Emirates",
            "ret_dep": "07:35", "ret_arr": "13:20", "ret_h": 7.75, "ret_air": "Qatar Airways"
        },
        {
            "dest": "MIA", "month": 5, "day": 11, "stay": 9, "price": 350.0,
            "out_dep": "11:55", "out_arr": "16:00", "out_h": 9.08, "out_air": "Air Europa",
            "ret_dep": "20:00", "ret_arr": "10:45", "ret_h": 8.75, "ret_air": "American Airlines"
        },
        {
            "dest": "CUN", "month": 6, "day": 1,  "stay": 8, "price": 430.0,
            "out_dep": "13:45", "out_arr": "18:20", "out_h": 10.58, "out_air": "World2Fly",
            "ret_dep": "21:00", "ret_arr": "13:30", "ret_h": 9.50, "ret_air": "Iberojet"
        },
        {
            "dest": "DEL", "month": 3, "day": 9,  "stay": 8, "price": 430.0,
            "out_dep": "09:30", "out_arr": "22:15", "out_h": 9.75, "out_air": "Saudia",
            "ret_dep": "03:10", "ret_arr": "14:00", "ret_h": 10.83, "ret_air": "Etihad Airways"
        },
        {
            "dest": "BOG", "month": 4, "day": 13, "stay": 8, "price": 480.0,
            "out_dep": "12:15", "out_arr": "16:45", "out_h": 10.50, "out_air": "Avianca",
            "ret_dep": "22:40", "ret_arr": "14:30", "ret_h": 9.83, "ret_air": "Air Europa"
        },
        {
            "dest": "MEX", "month": 5, "day": 18, "stay": 9, "price": 520.0,
            "out_dep": "14:40", "out_arr": "19:50", "out_h": 12.16, "out_air": "Aeroméxico",
            "ret_dep": "22:55", "ret_arr": "16:20", "ret_h": 10.41, "ret_air": "Iberia"
        },
        {
            "dest": "BKK", "month": 5, "day": 17, "stay": 9, "price": 490.0,
            "out_dep": "10:50", "out_arr": "06:15", "out_h": 13.41, "out_air": "Qatar Airways",
            "ret_dep": "20:30", "ret_arr": "07:45", "ret_h": 14.25, "ret_air": "Emirates"
        },
        {
            "dest": "NRT", "month": 9, "day": 6,  "stay": 9, "price": 599.0,
            "out_dep": "11:55", "out_arr": "08:50", "out_h": 13.91, "out_air": "Air China",
            "ret_dep": "22:30", "ret_arr": "08:20", "ret_h": 14.83, "ret_air": "Cathay Pacific"
        }
    ]

    results = []
    for item in sample_destinations:
        stay = item["stay"]
        if not (min_duration <= stay <= max_duration):
            continue

        dest_code = item["dest"]
        dest_info = get_airport_info(dest_code)
        m = item["month"]
        d = item["day"]
        ret_d = d + stay
        ret_m = m
        if ret_d > 28:
            ret_d = ret_d - 28
            ret_m = m + 1
            
        dep_str = f"{year}-{m:02d}-{d:02d}"
        ret_str = f"{year}-{ret_m:02d}-{ret_d:02d}"

        out_h = item["out_h"]
        ret_h = item["ret_h"]
        out_air = item["out_air"]
        ret_air = item["ret_air"]
        flight_price = item["price"]

        # 1. Estimación de alojamiento
        hotel_data = estimate_accommodation(dest_code, dest_info["continent"], stay)
        trip_total = round(flight_price + hotel_data["hotel_total_est"], 2)

        # 2. Generación de enlaces a múltiples plataformas y aerolíneas oficiales
        flight_links = build_flight_provider_links(origin, dest_code, dep_str, ret_str, out_air, ret_air)
        hotel_links = build_hotel_provider_links(dest_info["city"], dest_info["country"], dep_str, ret_str)

        results.append({
            "origin": origin,
            "origin_city": origin_info["city"],
            "origin_country": origin_info["country"],
            "origin_flag": origin_info["flag"],
            "destination": dest_code,
            "dest_city": dest_info["city"],
            "dest_country": dest_info["country"],
            "dest_flag": dest_info["flag"],
            "continent": dest_info["continent"],
            "departure_date": dep_str,
            "return_date": ret_str,
            "duration_days": stay,
            # Horarios y duraciones de vuelo
            "outbound_dep_time": item["out_dep"],
            "outbound_arr_time": item["out_arr"],
            "outbound_duration_hours": out_h,
            "outbound_duration_str": f"{int(out_h)}h {int((out_h % 1) * 60):02d}m",
            "outbound_airline": out_air,
            "return_dep_time": item["ret_dep"],
            "return_arr_time": item["ret_arr"],
            "return_duration_hours": ret_h,
            "return_duration_str": f"{int(ret_h)}h {int((ret_h % 1) * 60):02d}m",
            "return_airline": ret_air,
            "different_airlines": out_air != ret_air,
            "price": flight_price,
            "currency": "EUR",
            # Estimación de alojamiento (no altera orden de vuelos más baratos)
            "hotel_price_per_night": hotel_data["hotel_price_per_night"],
            "hotel_nights": hotel_data["hotel_nights"],
            "hotel_total_est": hotel_data["hotel_total_est"],
            "hotel_tier": hotel_data["hotel_tier"],
            "hotel_note": hotel_data["hotel_note"],
            "trip_total_est": trip_total,
            # Múltiples proveedores y enlaces directos
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

    # Mantener orden estricto por precio del vuelo (requisito del usuario)
    results.sort(key=lambda x: x["price"])
    return results

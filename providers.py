"""
Generador de enlaces para múltiples proveedores de vuelos y alojamiento.
Permite comparar en:
- Metabuscadores: Google Flights, Skyscanner, Kayak, Kiwi, Momondo
- Webs oficiales de las propias aerolíneas (Ida y Vuelta de forma independiente)
- Portales de alojamiento: Booking.com, Airbnb, Google Hotels
"""

import urllib.parse
from typing import Dict, Any, Optional

# Mapeo de webs directas de las principales aerolíneas mundiales
AIRLINE_WEBSITES = {
    "ryanair": "https://www.ryanair.com/es/es",
    "vueling": "https://www.vueling.com/es",
    "iberia": "https://www.iberia.com/es/",
    "iberia express": "https://www.iberiaexpress.com/",
    "easyjet": "https://www.easyjet.com/es",
    "wizz air": "https://wizzair.com/es-es",
    "air europa": "https://www.aireuropa.com/es/es/home",
    "tap portugal": "https://www.flytap.com/es-es/",
    "tap": "https://www.flytap.com/es-es/",
    "volotea": "https://www.volotea.com/es/",
    "lufthansa": "https://www.lufthansa.com/es/es/homepage",
    "air france": "https://www.airfrance.es/",
    "british airways": "https://www.britishairways.com/travel/home/public/es_es/",
    "ita airways": "https://www.ita-airways.com/es_es/",
    "norwegian": "https://www.norwegian.com/es/",
    "sas": "https://www.flysas.com/es-es/",
    "klm": "https://www.klm.es/",
    "brussels airlines": "https://www.brusselsairlines.com/es/es/homepage",
    "smartwings": "https://www.smartwings.com/es/",
    "eurowings": "https://www.eurowings.com/es.html",
    "play airlines": "https://www.flyplay.com/es-es",
    "level": "https://www.flylevel.com/",
    "transavia": "https://www.transavia.com/es-ES/home/",
    "binter": "https://www.bintercanarias.com/",
    "aegean airlines": "https://es.aegeanair.com/",
    "turkish airlines": "https://www.turkishairlines.com/es-es/",
    "emirates": "https://www.emirates.com/es/spanish/",
    "qatar airways": "https://www.qatarairways.com/es-es/homepage.html",
    "etihad airways": "https://www.etihad.com/es-es/",
    "american airlines": "https://www.aa.com/es-es/",
    "delta air lines": "https://es.delta.com/",
    "united airlines": "https://www.united.com/es/es",
    "avianca": "https://www.avianca.com/es/",
    "aeromexico": "https://aeromexico.com/es-es",
    "latam": "https://www.latamairlines.com/es/es",
    "egyptair": "https://www.egyptair.com/es/",
    "saudia": "https://www.saudia.com/es-ES",
    "air china": "https://www.airchina.es/ES/ES/Home",
    "cathay pacific": "https://www.cathaypacific.com/cx/es_ES.html",
    "world2fly": "https://www.w2fly.es/",
    "iberojet": "https://www.iberojet.com/"
}


def get_airline_website(airline_name: Optional[str]) -> str:
    """Devuelve la web oficial de la aerolínea o una búsqueda directa si no se reconoce."""
    if not airline_name:
        return "https://www.google.com"
    name_clean = airline_name.strip().lower()
    for key, url in AIRLINE_WEBSITES.items():
        if key in name_clean:
            return url
    encoded = urllib.parse.quote(f"{airline_name} vuelos oficiales")
    return f"https://www.google.com/search?q={encoded}"


def build_flight_provider_links(
    orig: str,
    dest: str,
    dep_date: str,
    ret_date: str,
    out_airline: str = "",
    ret_airline: str = ""
) -> Dict[str, str]:
    """
    Genera los enlaces de búsqueda en múltiples plataformas de vuelos y aerolíneas directas.
    """
    orig_u = (orig or "").upper()
    dest_u = (dest or "").upper()
    orig_l = (orig or "").lower()
    dest_l = (dest or "").lower()

    # Formato fechas compacto (YYMMDD) para Skyscanner
    dep_compact = dep_date.replace("-", "")[2:] if len(dep_date) >= 10 else ""
    ret_compact = ret_date.replace("-", "")[2:] if len(ret_date) >= 10 else ""

    # 1. Google Flights
    gflights_url = f"https://www.google.com/travel/flights?q=flights+from+{orig_u}+to+{dest_u}+on+{dep_date}+through+{ret_date}"

    # 2. Skyscanner
    if dep_compact and ret_compact:
        skyscanner_url = f"https://www.skyscanner.es/transport/vuelos/{orig_l}/{dest_l}/{dep_compact}/{ret_compact}/"
    else:
        skyscanner_url = f"https://www.skyscanner.es/transport/vuelos/{orig_l}/{dest_l}/"

    # 3. Kayak
    kayak_url = f"https://www.kayak.es/flights/{orig_u}-{dest_u}/{dep_date}/{ret_date}?sort=bestflight_a"

    # 4. Kiwi.com
    kiwi_url = f"https://www.kiwi.com/es/search/tiles/{orig_l}/{dest_l}/{dep_date}/{ret_date}"

    # 5. Momondo
    momondo_url = f"https://www.momondo.es/flight-search/{orig_u}-{dest_u}/{dep_date}/{ret_date}"

    # 6. Webs oficiales de aerolíneas para cada tramo
    out_airline_url = get_airline_website(out_airline)
    ret_airline_url = get_airline_website(ret_airline)

    return {
        "google_flights": gflights_url,
        "skyscanner": skyscanner_url,
        "kayak": kayak_url,
        "kiwi": kiwi_url,
        "momondo": momondo_url,
        "outbound_airline_url": out_airline_url,
        "return_airline_url": ret_airline_url
    }


def build_hotel_provider_links(city_name: str, dest_country: str, dep_date: str, ret_date: str) -> Dict[str, str]:
    """
    Genera enlaces pre-rellenados para buscar alojamiento en Booking, Airbnb y Google Hotels.
    """
    search_query = f"{city_name}, {dest_country}".strip()
    encoded_city = urllib.parse.quote(search_query)

    # 1. Booking.com
    booking_url = (
        f"https://www.booking.com/searchresults.html?ss={encoded_city}"
        f"&checkin={dep_date}&checkout={ret_date}&group_adults=2&no_rooms=1&group_children=0"
    )

    # 2. Airbnb
    airbnb_url = (
        f"https://www.airbnb.es/s/{encoded_city}/homes"
        f"?checkin={dep_date}&checkout={ret_date}&adults=2"
    )

    # 3. Google Hotels
    ghotels_url = (
        f"https://www.google.com/travel/hotels/{encoded_city}"
        f"?dates={dep_date}_{ret_date}"
    )

    return {
        "booking": booking_url,
        "airbnb": airbnb_url,
        "google_hotels": ghotels_url
    }

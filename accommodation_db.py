"""
Base de datos y estimador de costes de alojamiento para destinos mundiales.
Proporciona precios medios por noche (€/noche), categoría de coste y cálculo total
para la estancia del viaje.
"""

from typing import Dict, Any

# Estimación media de alojamiento por noche (habitación doble estándar / apartamento céntrico para 2 personas)
# Basado en medias anuales de portales turísticos (Booking / Airbnb)
CITY_ACCOMMODATION = {
    # España
    "MAD": {"price_night": 75, "tier": "Medio", "note": "Hoteles 3★ / Apartamentos céntricos"},
    "BCN": {"price_night": 90, "tier": "Medio-Alto", "note": "Demanda turística alta"},
    "AGP": {"price_night": 65, "tier": "Medio", "note": "Costa del Sol"},
    "ALC": {"price_night": 55, "tier": "Económico-Medio", "note": "Costa Blanca"},
    "VLC": {"price_night": 65, "tier": "Medio", "note": "Valencia centro y playa"},
    "SVQ": {"price_night": 60, "tier": "Medio", "note": "Sevilla casco antiguo"},
    "BIO": {"price_night": 70, "tier": "Medio", "note": "Bilbao centro"},
    "PMI": {"price_night": 85, "tier": "Medio-Alto", "note": "Mallorca"},
    "IBZ": {"price_night": 110, "tier": "Alto", "note": "Ibiza (varía según temporada)"},
    "TFS": {"price_night": 65, "tier": "Medio", "note": "Tenerife Sur"},
    "TFN": {"price_night": 55, "tier": "Económico-Medio", "note": "Tenerife Norte"},
    "LPA": {"price_night": 60, "tier": "Medio", "note": "Gran Canaria"},
    "SCQ": {"price_night": 50, "tier": "Económico-Medio", "note": "Santiago de Compostela"},

    # Portugal
    "OPO": {"price_night": 50, "tier": "Económico-Medio", "note": "Oporto muy asequible"},
    "LIS": {"price_night": 65, "tier": "Medio", "note": "Lisboa centro"},
    "FAO": {"price_night": 55, "tier": "Medio", "note": "Algarve"},

    # Francia, Reino Unido e Irlanda
    "CDG": {"price_night": 115, "tier": "Alto", "note": "París"},
    "ORY": {"price_night": 115, "tier": "Alto", "note": "París"},
    "BVA": {"price_night": 100, "tier": "Medio-Alto", "note": "París y alrededores"},
    "NCE": {"price_night": 95, "tier": "Medio-Alto", "note": "Costa Azul / Niza"},
    "MRS": {"price_night": 70, "tier": "Medio", "note": "Marsella"},
    "LYS": {"price_night": 75, "tier": "Medio", "note": "Lyon"},
    "LHR": {"price_night": 130, "tier": "Alto", "note": "Londres"},
    "LGW": {"price_night": 125, "tier": "Alto", "note": "Londres"},
    "STN": {"price_night": 120, "tier": "Alto", "note": "Londres"},
    "LTN": {"price_night": 120, "tier": "Alto", "note": "Londres"},
    "EDI": {"price_night": 95, "tier": "Medio-Alto", "note": "Edimburgo"},
    "MAN": {"price_night": 80, "tier": "Medio", "note": "Mánchester"},
    "DUB": {"price_night": 125, "tier": "Alto", "note": "Dublín"},

    # Benelux y Alemania / Suiza / Austria
    "AMS": {"price_night": 135, "tier": "Alto", "note": "Ámsterdam"},
    "EIN": {"price_night": 85, "tier": "Medio", "note": "Eindhoven"},
    "BRU": {"price_night": 85, "tier": "Medio", "note": "Bruselas"},
    "CRL": {"price_night": 65, "tier": "Medio", "note": "Charleroi / Valonia"},
    "FRA": {"price_night": 85, "tier": "Medio", "note": "Fráncfort"},
    "MUC": {"price_night": 95, "tier": "Medio-Alto", "note": "Múnich"},
    "BER": {"price_night": 80, "tier": "Medio", "note": "Berlín"},
    "ZRH": {"price_night": 150, "tier": "Muy Alto", "note": "Zúrich"},
    "GVA": {"price_night": 145, "tier": "Muy Alto", "note": "Ginebra"},
    "VIE": {"price_night": 80, "tier": "Medio", "note": "Viena"},

    # Italia y Grecia
    "FCO": {"price_night": 85, "tier": "Medio", "note": "Roma"},
    "CIA": {"price_night": 80, "tier": "Medio", "note": "Roma"},
    "MXP": {"price_night": 90, "tier": "Medio-Alto", "note": "Milán"},
    "BGY": {"price_night": 65, "tier": "Medio", "note": "Bérgamo / Milán norte"},
    "VCE": {"price_night": 110, "tier": "Alto", "note": "Venecia"},
    "NAP": {"price_night": 60, "tier": "Económico-Medio", "note": "Nápoles muy asequible"},
    "BLQ": {"price_night": 75, "tier": "Medio", "note": "Bolonia"},
    "ATH": {"price_night": 60, "tier": "Económico-Medio", "note": "Atenas"},
    "JTR": {"price_night": 120, "tier": "Alto", "note": "Santorini"},
    "MLA": {"price_night": 65, "tier": "Medio", "note": "Malta"},

    # Europa del Este y Nórdicos
    "PRG": {"price_night": 60, "tier": "Económico-Medio", "note": "Praga excelente calidad/precio"},
    "BUD": {"price_night": 50, "tier": "Económico", "note": "Budapest muy asequible"},
    "WAW": {"price_night": 55, "tier": "Económico", "note": "Varsovia"},
    "KRK": {"price_night": 45, "tier": "Económico", "note": "Cracovia gran valor"},
    "OTP": {"price_night": 45, "tier": "Económico", "note": "Bucarest"},
    "CPH": {"price_night": 125, "tier": "Alto", "note": "Copenhague"},
    "ARN": {"price_night": 105, "tier": "Medio-Alto", "note": "Estocolmo"},
    "OSL": {"price_night": 115, "tier": "Alto", "note": "Oslo"},
    "HEL": {"price_night": 100, "tier": "Medio-Alto", "note": "Helsinki"},
    "KEF": {"price_night": 140, "tier": "Alto", "note": "Islandia / Reikiavik"},
    "IST": {"price_night": 50, "tier": "Económico", "note": "Estambul gran oferta"},
    "SAW": {"price_night": 45, "tier": "Económico", "note": "Estambul"},

    # Norteamérica
    "JFK": {"price_night": 165, "tier": "Muy Alto", "note": "Nueva York"},
    "EWR": {"price_night": 145, "tier": "Alto", "note": "Nueva York / NJ"},
    "MIA": {"price_night": 140, "tier": "Alto", "note": "Miami"},
    "LAX": {"price_night": 135, "tier": "Alto", "note": "Los Ángeles"},
    "SFO": {"price_night": 150, "tier": "Muy Alto", "note": "San Francisco"},
    "BOS": {"price_night": 145, "tier": "Alto", "note": "Boston"},
    "ORD": {"price_night": 120, "tier": "Alto", "note": "Chicago"},
    "CUN": {"price_night": 70, "tier": "Medio", "note": "Cancún hoteles y resorts"},
    "MEX": {"price_night": 50, "tier": "Económico", "note": "Ciudad de México"},

    # Latinoamérica
    "BOG": {"price_night": 38, "tier": "Económico", "note": "Bogotá muy económico"},
    "MDE": {"price_night": 40, "tier": "Económico", "note": "Medellín"},
    "LIM": {"price_night": 45, "tier": "Económico", "note": "Lima"},
    "EZE": {"price_night": 55, "tier": "Económico-Medio", "note": "Buenos Aires"},
    "SCL": {"price_night": 60, "tier": "Medio", "note": "Santiago de Chile"},
    "GRU": {"price_night": 55, "tier": "Medio", "note": "São Paulo"},
    "HAV": {"price_night": 45, "tier": "Económico", "note": "La Habana"},
    "SJO": {"price_night": 55, "tier": "Medio", "note": "Costa Rica"},

    # Asia y Medio Oriente
    "DXB": {"price_night": 95, "tier": "Medio-Alto", "note": "Dubái hoteles modernos"},
    "DOH": {"price_night": 90, "tier": "Medio-Alto", "note": "Doha"},
    "HND": {"price_night": 80, "tier": "Medio", "note": "Tokio"},
    "NRT": {"price_night": 75, "tier": "Medio", "note": "Tokio"},
    "KIX": {"price_night": 70, "tier": "Medio", "note": "Osaka"},
    "BKK": {"price_night": 35, "tier": "Muy Económico", "note": "Bangkok excelente relación calidad/precio"},
    "DPS": {"price_night": 35, "tier": "Muy Económico", "note": "Bali villas y hoteles accesibles"},
    "SIN": {"price_night": 115, "tier": "Alto", "note": "Singapur"},
    "DEL": {"price_night": 30, "tier": "Muy Económico", "note": "Nueva Delhi"},

    # África
    "RAK": {"price_night": 40, "tier": "Muy Económico", "note": "Marrakech riads y hoteles asequibles"},
    "CAI": {"price_night": 35, "tier": "Muy Económico", "note": "El Cairo"},
    "CPT": {"price_night": 65, "tier": "Medio", "note": "Ciudad del Cabo"}
}

CONTINENT_DEFAULTS = {
    "Europa": {"price_night": 75, "tier": "Medio", "note": "Media europea"},
    "Latinoamérica": {"price_night": 45, "tier": "Económico", "note": "Media latinoamericana"},
    "Norteamérica": {"price_night": 135, "tier": "Alto", "note": "Media norteamericana"},
    "Asia": {"price_night": 40, "tier": "Económico", "note": "Media asiática"},
    "Medio Oriente": {"price_night": 85, "tier": "Medio", "note": "Media medio oriente"},
    "África": {"price_night": 45, "tier": "Económico", "note": "Media africana"},
    "Oceanía": {"price_night": 110, "tier": "Alto", "note": "Media oceanía"},
    "Otro": {"price_night": 60, "tier": "Medio", "note": "Media mundial"}
}


def estimate_accommodation(iata_code: str, continent: str, stay_days: int) -> Dict[str, Any]:
    """
    Calcula la estimación de coste de alojamiento para un destino y una duración determinada.
    No influye en el filtro ni búsqueda de vuelos, pero aporta la visión completa de presupuesto.
    """
    code = (iata_code or "").strip().upper()
    info = CITY_ACCOMMODATION.get(code)
    
    if not info:
        info = CONTINENT_DEFAULTS.get(continent, CONTINENT_DEFAULTS["Otro"])

    price_night = info["price_night"]
    # Número de noches = días de estancia (habitual)
    nights = max(1, stay_days)
    total_hotel = price_night * nights

    return {
        "hotel_price_per_night": price_night,
        "hotel_nights": nights,
        "hotel_total_est": total_hotel,
        "hotel_tier": info["tier"],
        "hotel_note": info["note"]
    }

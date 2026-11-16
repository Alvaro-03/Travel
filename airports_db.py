"""
Base de datos local de aeropuertos mundiales más comunes para traducir
códigos IATA (MAD, JFK, NRT...) a nombres de ciudad, país y bandera.
"""

AIRPORTS = {
    # España
    "MAD": {"city": "Madrid", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "BCN": {"city": "Barcelona", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "AGP": {"city": "Málaga", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "ALC": {"city": "Alicante", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "VLC": {"city": "Valencia", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "SVQ": {"city": "Sevilla", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "BIO": {"city": "Bilbao", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "PMI": {"city": "Palma de Mallorca", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "IBZ": {"city": "Ibiza", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "TFS": {"city": "Tenerife Sur", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "TFN": {"city": "Tenerife Norte", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "LPA": {"city": "Gran Canaria", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "SCQ": {"city": "Santiago de Compostela", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "OVD": {"city": "Asturias", "country": "España", "flag": "🇪🇸", "continent": "Europa"},
    "ZAZ": {"city": "Zaragoza", "country": "España", "flag": "🇪🇸", "continent": "Europa"},

    # Europa Occidental y Central
    "CDG": {"city": "París (Charles de Gaulle)", "country": "Francia", "flag": "🇫🇷", "continent": "Europa"},
    "ORY": {"city": "París (Orly)", "country": "Francia", "flag": "🇫🇷", "continent": "Europa"},
    "BVA": {"city": "París (Beauvais)", "country": "Francia", "flag": "🇫🇷", "continent": "Europa"},
    "NCE": {"city": "Niza", "country": "Francia", "flag": "🇫🇷", "continent": "Europa"},
    "MRS": {"city": "Marsella", "country": "Francia", "flag": "🇫🇷", "continent": "Europa"},
    "LYS": {"city": "Lyon", "country": "Francia", "flag": "🇫🇷", "continent": "Europa"},
    "LHR": {"city": "Londres (Heathrow)", "country": "Reino Unido", "flag": "🇬🇧", "continent": "Europa"},
    "LGW": {"city": "Londres (Gatwick)", "country": "Reino Unido", "flag": "🇬🇧", "continent": "Europa"},
    "STN": {"city": "Londres (Stansted)", "country": "Reino Unido", "flag": "🇬🇧", "continent": "Europa"},
    "LTN": {"city": "Londres (Luton)", "country": "Reino Unido", "flag": "🇬🇧", "continent": "Europa"},
    "EDI": {"city": "Edimburgo", "country": "Reino Unido", "flag": "🇬🇧", "continent": "Europa"},
    "MAN": {"city": "Mánchester", "country": "Reino Unido", "flag": "🇬🇧", "continent": "Europa"},
    "DUB": {"city": "Dublín", "country": "Irlanda", "flag": "🇮🇪", "continent": "Europa"},
    "AMS": {"city": "Ámsterdam", "country": "Países Bajos", "flag": "🇳🇱", "continent": "Europa"},
    "EIN": {"city": "Eindhoven", "country": "Países Bajos", "flag": "🇳🇱", "continent": "Europa"},
    "BRU": {"city": "Bruselas", "country": "Bélgica", "flag": "🇧🇪", "continent": "Europa"},
    "CRL": {"city": "Bruselas (Charleroi)", "country": "Bélgica", "flag": "🇧🇪", "continent": "Europa"},
    "FRA": {"city": "Fráncfort", "country": "Alemania", "flag": "🇩🇪", "continent": "Europa"},
    "MUC": {"city": "Múnich", "country": "Alemania", "flag": "🇩🇪", "continent": "Europa"},
    "BER": {"city": "Berlín", "country": "Alemania", "flag": "🇩🇪", "continent": "Europa"},
    "HAM": {"city": "Hamburgo", "country": "Alemania", "flag": "🇩🇪", "continent": "Europa"},
    "CGN": {"city": "Colonia/Bonn", "country": "Alemania", "flag": "🇩🇪", "continent": "Europa"},
    "ZRH": {"city": "Zúrich", "country": "Suiza", "flag": "🇨🇭", "continent": "Europa"},
    "GVA": {"city": "Ginebra", "country": "Suiza", "flag": "🇨🇭", "continent": "Europa"},
    "VIE": {"city": "Viena", "country": "Austria", "flag": "🇦🇹", "continent": "Europa"},

    # Europa Sur
    "LIS": {"city": "Lisboa", "country": "Portugal", "flag": "🇵🇹", "continent": "Europa"},
    "OPO": {"city": "Oporto", "country": "Portugal", "flag": "🇵🇹", "continent": "Europa"},
    "FAO": {"city": "Faro (Algarve)", "country": "Portugal", "flag": "🇵🇹", "continent": "Europa"},
    "FCO": {"city": "Roma (Fiumicino)", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "CIA": {"city": "Roma (Ciampino)", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "MXP": {"city": "Milán (Malpensa)", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "BGY": {"city": "Milán (Bérgamo)", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "VCE": {"city": "Venecia", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "NAP": {"city": "Nápoles", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "BLQ": {"city": "Bolonia", "country": "Italia", "flag": "🇮🇹", "continent": "Europa"},
    "ATH": {"city": "Atenas", "country": "Grecia", "flag": "🇬🇷", "continent": "Europa"},
    "HER": {"city": "Creta (Heraklion)", "country": "Grecia", "flag": "🇬🇷", "continent": "Europa"},
    "JTR": {"city": "Santorini", "country": "Grecia", "flag": "🇬🇷", "continent": "Europa"},
    "MLA": {"city": "Malta", "country": "Malta", "flag": "🇲🇹", "continent": "Europa"},

    # Europa del Norte y Este
    "CPH": {"city": "Copenhague", "country": "Dinamarca", "flag": "🇩🇰", "continent": "Europa"},
    "ARN": {"city": "Estocolmo", "country": "Suecia", "flag": "🇸🇪", "continent": "Europa"},
    "OSL": {"city": "Oslo", "country": "Noruega", "flag": "🇳🇴", "continent": "Europa"},
    "HEL": {"city": "Helsinki", "country": "Finlandia", "flag": "🇫🇮", "continent": "Europa"},
    "KEF": {"city": "Reikiavik", "country": "Islandia", "flag": "🇮🇸", "continent": "Europa"},
    "PRG": {"city": "Praga", "country": "República Checa", "flag": "🇨🇿", "continent": "Europa"},
    "BUD": {"city": "Budapest", "country": "Hungría", "flag": "🇭🇺", "continent": "Europa"},
    "WAW": {"city": "Varsovia", "country": "Polonia", "flag": "🇵🇱", "continent": "Europa"},
    "KRK": {"city": "Cracovia", "country": "Polonia", "flag": "🇵🇱", "continent": "Europa"},
    "OTP": {"city": "Bucarest", "country": "Rumanía", "flag": "🇷🇴", "continent": "Europa"},
    "SOF": {"city": "Sofía", "country": "Bulgaria", "flag": "🇧🇬", "continent": "Europa"},
    "ZAG": {"city": "Zagreb", "country": "Croacia", "flag": "🇭🇷", "continent": "Europa"},
    "DBV": {"city": "Dubrovnik", "country": "Croacia", "flag": "🇭🇷", "continent": "Europa"},
    "IST": {"city": "Estambul", "country": "Turquía", "flag": "🇹🇷", "continent": "Europa / Asia"},
    "SAW": {"city": "Estambul (Sabiha)", "country": "Turquía", "flag": "🇹🇷", "continent": "Europa / Asia"},

    # América del Norte
    "JFK": {"city": "Nueva York (JFK)", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "EWR": {"city": "Nueva York (Newark)", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "MIA": {"city": "Miami", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "LAX": {"city": "Los Ángeles", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "SFO": {"city": "San Francisco", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "ORD": {"city": "Chicago", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "BOS": {"city": "Boston", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "LAS": {"city": "Las Vegas", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "MCO": {"city": "Orlando", "country": "Estados Unidos", "flag": "🇺🇸", "continent": "Norteamérica"},
    "YYZ": {"city": "Toronto", "country": "Canadá", "flag": "🇨🇦", "continent": "Norteamérica"},
    "YUL": {"city": "Montreal", "country": "Canadá", "flag": "🇨🇦", "continent": "Norteamérica"},
    "YVR": {"city": "Vancouver", "country": "Canadá", "flag": "🇨🇦", "continent": "Norteamérica"},
    "MEX": {"city": "Ciudad de México", "country": "México", "flag": "🇲🇽", "continent": "Latinoamérica"},
    "CUN": {"city": "Cancún", "country": "México", "flag": "🇲🇽", "continent": "Latinoamérica"},
    "GDL": {"city": "Guadalajara", "country": "México", "flag": "🇲🇽", "continent": "Latinoamérica"},

    # América del Sur y Central
    "BOG": {"city": "Bogotá", "country": "Colombia", "flag": "🇨🇴", "continent": "Latinoamérica"},
    "MDE": {"city": "Medellín", "country": "Colombia", "flag": "🇨🇴", "continent": "Latinoamérica"},
    "CTG": {"city": "Cartagena", "country": "Colombia", "flag": "🇨🇴", "continent": "Latinoamérica"},
    "LIM": {"city": "Lima", "country": "Perú", "flag": "🇵🇪", "continent": "Latinoamérica"},
    "EZE": {"city": "Buenos Aires (Ezeiza)", "country": "Argentina", "flag": "🇦🇷", "continent": "Latinoamérica"},
    "AEP": {"city": "Buenos Aires (Aeroparque)", "country": "Argentina", "flag": "🇦🇷", "continent": "Latinoamérica"},
    "SCL": {"city": "Santiago de Chile", "country": "Chile", "flag": "🇨🇱", "continent": "Latinoamérica"},
    "GRU": {"city": "São Paulo (Guarulhos)", "country": "Brasil", "flag": "🇧🇷", "continent": "Latinoamérica"},
    "GIG": {"city": "Río de Janeiro (Galeão)", "country": "Brasil", "flag": "🇧🇷", "continent": "Latinoamérica"},
    "PTY": {"city": "Ciudad de Panamá", "country": "Panamá", "flag": "🇵🇦", "continent": "Latinoamérica"},
    "SJO": {"city": "San José", "country": "Costa Rica", "flag": "🇨🇷", "continent": "Latinoamérica"},
    "HAV": {"city": "La Habana", "country": "Cuba", "flag": "🇨🇺", "continent": "Latinoamérica"},
    "SDQ": {"city": "Santo Domingo", "country": "República Dominicana", "flag": "🇩🇴", "continent": "Latinoamérica"},
    "PUJ": {"city": "Punta Cana", "country": "República Dominicana", "flag": "🇩🇴", "continent": "Latinoamérica"},

    # Asia y Medio Oriente
    "DXB": {"city": "Dubái", "country": "Emiratos Árabes Unidos", "flag": "🇦🇪", "continent": "Medio Oriente"},
    "DOH": {"city": "Doha", "country": "Catar", "flag": "🇶🇦", "continent": "Medio Oriente"},
    "HND": {"city": "Tokio (Haneda)", "country": "Japón", "flag": "🇯🇵", "continent": "Asia"},
    "NRT": {"city": "Tokio (Narita)", "country": "Japón", "flag": "🇯🇵", "continent": "Asia"},
    "KIX": {"city": "Osaka (Kansai)", "country": "Japón", "flag": "🇯🇵", "continent": "Asia"},
    "ICN": {"city": "Seúl (Incheon)", "country": "Corea del Sur", "flag": "🇰🇷", "continent": "Asia"},
    "BKK": {"city": "Bangkok (Suvarnabhumi)", "country": "Tailandia", "flag": "🇹🇭", "continent": "Asia"},
    "DMK": {"city": "Bangkok (Don Mueang)", "country": "Tailandia", "flag": "🇹🇭", "continent": "Asia"},
    "HKT": {"city": "Phuket", "country": "Tailandia", "flag": "🇹🇭", "continent": "Asia"},
    "SIN": {"city": "Singapur", "country": "Singapur", "flag": "🇸🇬", "continent": "Asia"},
    "KUL": {"city": "Kuala Lumpur", "country": "Malasia", "flag": "🇲🇾", "continent": "Asia"},
    "DPS": {"city": "Bali (Denpasar)", "country": "Indonesia", "flag": "🇮🇩", "continent": "Asia"},
    "HKG": {"city": "Hong Kong", "country": "Hong Kong", "flag": "🇭🇰", "continent": "Asia"},
    "DEL": {"city": "Nueva Delhi", "country": "India", "flag": "🇮🇳", "continent": "Asia"},
    "BOM": {"city": "Bombay (Mumbai)", "country": "India", "flag": "🇮🇳", "continent": "Asia"},

    # África
    "RAK": {"city": "Marrakech", "country": "Marruecos", "flag": "🇲🇦", "continent": "África"},
    "CMN": {"city": "Casablanca", "country": "Marruecos", "flag": "🇲🇦", "continent": "África"},
    "TNG": {"city": "Tánger", "country": "Marruecos", "flag": "🇲🇦", "continent": "África"},
    "CAI": {"city": "El Cairo", "country": "Egipto", "flag": "🇪🇬", "continent": "África"},
    "CPT": {"city": "Ciudad del Cabo", "country": "Sudáfrica", "flag": "🇿🇦", "continent": "África"},
    "JNB": {"city": "Johannesburgo", "country": "Sudáfrica", "flag": "🇿🇦", "continent": "África"},
    "SEZ": {"city": "Seychelles", "country": "Seychelles", "flag": "🇸🇨", "continent": "África"},
    "MRU": {"city": "Mauricio", "country": "Mauricio", "flag": "🇲🇺", "continent": "África"},

    # Oceanía
    "SYD": {"city": "Sídney", "country": "Australia", "flag": "🇦🇺", "continent": "Oceanía"},
    "MEL": {"city": "Melbourne", "country": "Australia", "flag": "🇦🇺", "continent": "Oceanía"},
    "AKL": {"city": "Auckland", "country": "Nueva Zelanda", "flag": "🇳🇿", "continent": "Oceanía"},
}


def get_airport_info(iata_code: str) -> dict:
    """Devuelve la información de un aeropuerto a partir de su código IATA."""
    code = (iata_code or "").strip().upper()
    if code in AIRPORTS:
        info = AIRPORTS[code].copy()
        info["iata"] = code
        return info
    return {
        "iata": code,
        "city": code,
        "country": "Desconocido",
        "flag": "✈️",
        "continent": "Otro"
    }


def format_location(iata_code: str) -> str:
    """Devuelve una cadena legible con ciudad, país y bandera."""
    info = get_airport_info(iata_code)
    if info["country"] != "Desconocido":
        return f"{info['flag']} {info['city']} ({info['country']}) [{info['iata']}]"
    return f"✈️ [{iata_code}]"

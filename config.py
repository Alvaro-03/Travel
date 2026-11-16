import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables del archivo .env si existe
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Configuración de Amadeus (API oficial de GDS - 2000 peticiones gratis al mes)
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID", "").strip()
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET", "").strip()
AMADEUS_ENV = os.getenv("AMADEUS_ENV", "production").strip().lower()

# Configuración de Kiwi Tequila (opcional, para low-cost worldwide)
KIWI_API_KEY = os.getenv("KIWI_API_KEY", "").strip()

# Moneda y origen por defecto
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "EUR").strip().upper()
DEFAULT_ORIGIN = os.getenv("DEFAULT_ORIGIN", "MAD").strip().upper()

# Token del bot de Telegram y Chat ID para alertas en tiempo real
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# Configuración del monitor en tiempo real
# Intervalo de escaneo en minutos (por defecto 30 minutos)
SCAN_INTERVAL_MINUTES = int(os.getenv("SCAN_INTERVAL_MINUTES", "30"))
# Precio máximo para considerar un vuelo como 'Chollo' para enviar alerta al móvil
ALERT_MAX_PRICE = float(os.getenv("ALERT_MAX_PRICE", "100.0"))


def has_amadeus_keys() -> bool:
    return bool(AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET)


def has_kiwi_key() -> bool:
    return bool(KIWI_API_KEY)

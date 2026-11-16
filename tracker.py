import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

HISTORY_FILE = Path(__file__).resolve().parent / "flight_history.json"
SUBSCRIBERS_FILE = Path(__file__).resolve().parent / "subscribers.json"


def load_subscribers() -> List[int]:
    """Carga los chat_ids de Telegram suscritos a las alertas en tiempo real."""
    if not SUBSCRIBERS_FILE.exists():
        return []
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("subscribers", [])
    except Exception:
        return []


def save_subscriber(chat_id: int) -> bool:
    """Añade un chat_id a la lista de suscriptores para recibir alertas."""
    subs = set(load_subscribers())
    if chat_id not in subs:
        subs.add(chat_id)
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"subscribers": list(subs)}, f, indent=2)
        return True
    return False


def remove_subscriber(chat_id: int) -> bool:
    """Elimina un chat_id de la lista de suscriptores."""
    subs = set(load_subscribers())
    if chat_id in subs:
        subs.remove(chat_id)
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"subscribers": list(subs)}, f, indent=2)
        return True
    return False


def load_flight_history() -> Dict[str, Any]:
    """Carga el historial previo de vuelos escaneados para detectar cambios."""
    if not HISTORY_FILE.exists():
        return {"last_scan": None, "flights": {}}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_scan": None, "flights": {}}


def save_flight_history(flights: List[Dict[str, Any]]):
    """Guarda el estado actual de los vuelos con marca de tiempo."""
    flight_dict = {}
    for f in flights:
        key = f"{f['origin']}_{f['destination']}_{f['departure_date']}_{f['return_date']}"
        flight_dict[key] = {
            "price": f["price"],
            "dest_city": f["dest_city"],
            "dest_country": f["dest_country"],
            "dest_flag": f["dest_flag"],
            "departure_date": f["departure_date"],
            "return_date": f["return_date"],
            "duration_days": f.get("duration_days", 7),
            "outbound_airline": f.get("outbound_airline", ""),
            "return_airline": f.get("return_airline", ""),
            "hotel_total_est": f.get("hotel_total_est", 0),
            "trip_total_est": f.get("trip_total_est", 0),
            "direct_link": f.get("direct_link", ""),
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    data = {
        "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "flights": flight_dict
    }

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def analyze_new_deals(
    current_flights: List[Dict[str, Any]],
    alert_max_price: float = 100.0,
    min_price_drop: float = 5.0
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Compara los vuelos actuales contra el historial para identificar:
    1. Bajadas de precio respecto al último escaneo.
    2. Nuevos chollos por debajo del umbral de alerta (alert_max_price).
    
    Devuelve: (lista_chollos_detectados, vuelos_actualizados_con_etiquetas)
    """
    history = load_flight_history()
    prev_flights = history.get("flights", {})
    is_first_run = len(prev_flights) == 0

    deals_to_notify = []
    enriched_flights = []

    for f in current_flights:
        key = f"{f['origin']}_{f['destination']}_{f['departure_date']}_{f['return_date']}"
        current_price = f["price"]
        prev_data = prev_flights.get(key)

        flight_copy = dict(f)
        flight_copy["deal_type"] = None
        flight_copy["price_diff"] = 0.0

        if prev_data:
            prev_price = prev_data.get("price", current_price)
            diff = prev_price - current_price

            # ¿Ha bajado de precio?
            if diff >= min_price_drop:
                flight_copy["deal_type"] = "price_drop"
                flight_copy["price_diff"] = round(diff, 2)
                flight_copy["prev_price"] = prev_price
                deals_to_notify.append(flight_copy)
        else:
            # Nuevo destino no registrado antes
            if not is_first_run and current_price <= alert_max_price:
                flight_copy["deal_type"] = "new_deal"
                flight_copy["price_diff"] = 0.0
                deals_to_notify.append(flight_copy)
            elif is_first_run and current_price <= alert_max_price:
                # En la primera ejecución solo alertamos de los chollos más top
                flight_copy["deal_type"] = "top_deal"
                if current_price <= 50.0:  # Súper chollo inicial
                    deals_to_notify.append(flight_copy)

        enriched_flights.append(flight_copy)

    # Actualizar historial
    save_flight_history(current_flights)

    return deals_to_notify, enriched_flights

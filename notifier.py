"""
Módulo de notificaciones push a Telegram para alertas en tiempo real de vuelos y chollos.
"""

import requests
from typing import List, Dict, Any
import config
from tracker import load_subscribers


def get_all_target_chats() -> List[int]:
    """Obtiene todos los IDs de chat a los que se deben enviar alertas."""
    chats = set(load_subscribers())
    # Si hay un CHAT_ID explícito en el .env, añadirlo
    env_chat_id = getattr(config, "TELEGRAM_CHAT_ID", "")
    if env_chat_id and str(env_chat_id).strip():
        try:
            chats.add(int(str(env_chat_id).strip()))
        except ValueError:
            pass
    return list(chats)


def send_deal_alert(deal: Dict[str, Any], bot_token: str = None) -> int:
    """
    Envía una notificación push a todos los teléfonos/chats suscritos en Telegram.
    Devuelve la cantidad de mensajes enviados con éxito.
    """
    token = bot_token or config.TELEGRAM_BOT_TOKEN
    if not token:
        print("⚠️  Aviso: No se pueden enviar alertas por Telegram porque falta TELEGRAM_BOT_TOKEN en .env.")
        return 0

    target_chats = get_all_target_chats()
    if not target_chats:
        print("ℹ️  No hay chats suscritos a las alertas. Habla con el bot en Telegram y envía /alertas para suscribirte.")
        return 0

    deal_type = deal.get("deal_type")
    price = deal.get("price", 0)
    diff = deal.get("price_diff", 0)
    prev = deal.get("prev_price", price + diff)
    stay = deal.get("duration_days", 7)

    # Encabezado según tipo de oferta
    if deal_type == "price_drop":
        header = f"📉 <b>¡BAJADA DE PRECIO DETECTADA!</b> (-{diff:.0f} €)"
        price_line = f"💵 <b>Precio ahora: {price:.0f} €</b> (antes {prev:.0f} €)"
    elif deal_type == "new_deal":
        header = "✨ <b>¡NUEVO CHOLLO ENCONTRADO EN 2027!</b>"
        price_line = f"💵 <b>Precio I/V: {price:.0f} €</b>"
    else:
        header = "🔥 <b>¡SÚPER OFERTA DESTACADA 2027!</b>"
        price_line = f"💵 <b>Precio I/V: {price:.0f} €</b>"

    diff_tag = "🔀 Cías. Distintas" if deal.get("different_airlines") else "Misma Aerolínea"

    text = (
        f"{header}\n\n"
        f"📍 Destino: {deal.get('dest_flag')} <b>{deal.get('dest_city')} ({deal.get('dest_country')}) [{deal.get('destination')}]</b>\n"
        f"🛫 Salida desde: <b>{deal.get('origin')}</b>\n"
        f"📅 Fechas: <b>{deal.get('departure_date')}</b> al <b>{deal.get('return_date')}</b> ({stay} días)\n"
        f"{price_line}\n"
        f"⏱️ Horarios:\n"
        f"  • Ida: {deal.get('outbound_dep_time')} ➔ {deal.get('outbound_arr_time')} ({deal.get('outbound_airline')})\n"
        f"  • Vuelta: {deal.get('return_dep_time')} ➔ {deal.get('return_arr_time')} ({deal.get('return_airline')})\n"
        f"  • {diff_tag}\n\n"
        f"🏨 <b>Alojamiento estimado:</b> ~{deal.get('hotel_price_per_night', 0)} €/noche (~{deal.get('hotel_total_est', 0)} € estancia)\n"
        f"🏷️ <b>Presupuesto total estimado: ~{deal.get('trip_total_est', 0)} €</b>\n\n"
        f"🔗 <a href=\"{deal.get('direct_link')}\">Ver en Google Flights</a> | "
        f"<a href=\"{deal.get('skyscanner_link')}\">Skyscanner</a> | "
        f"<a href=\"{deal.get('booking_link')}\">Booking</a>"
    )

    sent_count = 0
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for chat_id in target_chats:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                sent_count += 1
            else:
                print(f"Error al enviar a chat {chat_id}: {resp.text}")
        except Exception as e:
            print(f"Error enviando notificación a {chat_id}: {e}")

    return sent_count

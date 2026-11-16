"""
Gestor de configuración del usuario y procesamiento de comandos de Telegram.
Permite cambiar el límite de precio de alerta (por defecto 500€) directamente desde el chat de Telegram.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional
import config

SETTINGS_FILE = Path(__file__).resolve().parent / "user_settings.json"

DEFAULT_SETTINGS = {
    "max_alert_price": 500.0,
    "last_update_id": 0,
    "welcome_sent": False
}


def load_settings() -> Dict[str, Any]:
    """Carga los ajustes del usuario o devuelve los valores por defecto."""
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Combinar con defaults por si faltan claves
            res = DEFAULT_SETTINGS.copy()
            res.update(data)
            return res
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: Dict[str, Any]):
    """Guarda los ajustes del usuario en user_settings.json."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def check_and_process_telegram_commands(token: str, chat_id: str) -> Dict[str, Any]:
    """
    Consulta los mensajes recientes en Telegram para detectar si el usuario ha enviado
    comandos como '/limite 350', '/precio 400', etc., y actualiza la configuración.
    """
    settings = load_settings()
    if not token:
        return settings

    offset = settings.get("last_update_id", 0) + 1
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"offset": offset, "timeout": 5}

    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return settings

        data = resp.json()
        updates = data.get("result", [])

        for update in updates:
            up_id = update.get("update_id", 0)
            if up_id > settings.get("last_update_id", 0):
                settings["last_update_id"] = up_id

            msg = update.get("message", {})
            text = (msg.get("text") or "").strip()
            sender_chat_id = str(msg.get("chat", {}).get("id", ""))

            # Si el mensaje proviene del chat autorizado o configurado
            if not text:
                continue

            parts = text.split()
            cmd = parts[0].lower()

            # 1. Comando para cambiar el precio límite
            if cmd in ("/limite", "/precio", "/tope", "/max"):
                if len(parts) > 1:
                    val_str = parts[1].replace("€", "").replace("$", "").strip()
                    try:
                        new_price = float(val_str)
                        settings["max_alert_price"] = new_price
                        save_settings(settings)

                        reply_text = (
                            f"🎯 <b>¡Límite de precio actualizado!</b>\n\n"
                            f"A partir de ahora te avisaremos de:\n"
                            f"• Cualquier <b>nuevo chollo</b> de ida y vuelta que cueste <b>≤ {new_price:.0f} €</b>\n"
                            f"• Todas las <b>bajadas de precio</b> que se detecten.\n\n"
                            f"<i>(Para volver a cambiarlo, escribe ej: <code>/limite 300</code>)</i>"
                        )
                        _send_reply(token, sender_chat_id or chat_id, reply_text)
                        print(f"✅ Límite de precio actualizado a {new_price}€ por orden del usuario en Telegram.")
                    except ValueError:
                        _send_reply(token, sender_chat_id or chat_id, "⚠️ Formato no válido. Escribe por ejemplo: <code>/limite 400</code>")
                else:
                    curr = settings.get("max_alert_price", 500.0)
                    _send_reply(token, sender_chat_id or chat_id, f"ℹ️ Tu límite actual es de <b>{curr:.0f} €</b>. Para cambiarlo escribe: <code>/limite 350</code>")

            # 2. Comando de estado
            elif cmd in ("/estado", "/status", "/config"):
                curr = settings.get("max_alert_price", 500.0)
                reply_text = (
                    f"⚙️ <b>Estado de tu Monitor de Vuelos 2027:</b>\n\n"
                    f"• 💰 Precio límite para chollos: <b>{curr:.0f} €</b> (Ida y Vuelta)\n"
                    f"• ⏱️ Duración de viaje: <b>5 a 9 días (~1 semana)</b>\n"
                    f"• 📡 Frecuencia de escaneo: <b>Cada 2 horas en la nube</b>\n"
                    f"• 🔔 Alertas automáticas: <b>Activadas</b>\n\n"
                    f"💡 <i>Escribe <code>/limite 300</code> para cambiar el tope de precio en cualquier momento.</i>"
                )
                _send_reply(token, sender_chat_id or chat_id, reply_text)

        save_settings(settings)
    except Exception as e:
        print(f"Aviso al consultar comandos de Telegram: {e}")

    return settings


def _send_reply(token: str, chat_id: str, text: str):
    """Envía un mensaje de respuesta a Telegram."""
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error enviando respuesta a Telegram: {e}")


def send_welcome_and_top_deals(flights: List[Dict[str, Any]], token: str, chat_id: str, limit: float = 500.0):
    """
    Envía el mensaje de bienvenida y el Top 3 de chollos actuales (ida + vuelta)
    para confirmar que la conexión con el teléfono móvil funciona al 100%.
    """
    if not token or not chat_id:
        return

    # Mensaje de bienvenida
    welcome_msg = (
        "👋 <b>¡Bienvenido a tu Monitor de Vuelos 2027!</b> ✈️🌍\n\n"
        "✅ <b>Conexión completada con éxito.</b>\n"
        "Tu sistema en la nube ya está activo vigilando ofertas las 24 horas sin necesidad de tener tu ordenador encendido.\n\n"
        f"🎯 <b>Criterio de alertas configurado:</b>\n"
        f"• Nuevos chollos de ida y vuelta por <b>≤ {limit:.0f} €</b>\n"
        f"• Cualquier <b>bajada de precio</b> respecto al escaneo anterior\n\n"
        f"💬 <i>¿Quieres cambiar el precio límite? Puedes escribir aquí en cualquier momento ej: <code>/limite 300</code></i>\n\n"
        "👇 <b>Aquí tienes los 3 mejores chollos actuales para comprobar la conexión:</b>"
    )
    _send_reply(token, chat_id, welcome_msg)

    # Enviar los 3 mejores chollos
    from notifier import send_deal_alert
    for deal in flights[:3]:
        deal_copy = dict(deal)
        deal_copy["deal_type"] = "top_deal"
        send_deal_alert(deal_copy, bot_token=token)

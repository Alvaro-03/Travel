#!/usr/bin/env python3
"""
========================================================================
🤖  BOT DE TELEGRAM PARA COMPARAR VUELOS BARATOS MUNDIALES (2027)  🤖
========================================================================
Permite consultar vuelos y RECIBIR ALERTAS EN TIEMPO REAL al móvil
cuando bajen los precios o se detecten nuevos chollos.
"""

import time
import requests
import config
from flight_scanner import fetch_flights
from filter_engine import apply_flight_filters
from airports_db import get_airport_info
from tracker import save_subscriber, remove_subscriber, load_subscribers


class TelegramFlightBot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.offset = 0

    def send_message(self, chat_id: int, text: str, parse_mode: str = "HTML"):
        """Envía un mensaje al usuario por Telegram."""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Error al enviar mensaje a Telegram: {e}")

    def handle_command(self, chat_id: int, message_text: str):
        text = message_text.strip()
        parts = text.split()
        cmd = parts[0].lower() if parts else ""

        if cmd in ("/start", "/ayuda", "/help"):
            msg = (
                "✈️ <b>Bienvenido al Bot de Vuelos Baratos 2027</b> 🌍🏨\n\n"
                "Te ayudo a encontrar los destinos más baratos del mundo en 2027 y <b>te aviso al móvil cuando haya ofertas en tiempo real</b>.\n\n"
                "<b>🔔 Alertas automáticas:</b>\n"
                "• <code>/alertas</code> : Activa o desactiva avisos al móvil cuando baje el precio de un vuelo o aparezca un nuevo chollo.\n"
                "• <code>/estado</code> : Estado de la monitorización en vivo.\n\n"
                "<b>🔍 Búsqueda manual:</b>\n"
                "• <code>/vuelos [ORIGEN]</code> : Vuelos baratos de 5 a 9 días (ej: <code>/vuelos MAD</code>)\n"
                "• <code>/chollos</code> : Top 5 chollos mundiales con estimación de hotel.\n"
                "• <code>/ayuda</code> : Muestra este mensaje."
            )
            self.send_message(chat_id, msg)

        elif cmd == "/alertas":
            subs = load_subscribers()
            if chat_id in subs:
                remove_subscriber(chat_id)
                self.send_message(chat_id, "🔕 <b>Alertas desactivadas</b>. Ya no recibirás notificaciones automáticas en este chat.")
            else:
                save_subscriber(chat_id)
                self.send_message(
                    chat_id,
                    "🔔 <b>¡Alertas en tiempo real activadas!</b>\n\n"
                    "A partir de ahora, cada vez que el monitor detecte una <b>bajada de precio</b> o un <b>nuevo chollo</b> para 2027, "
                    "recibirás un aviso inmediato en este chat con todos los detalles y enlaces."
                )

        elif cmd == "/estado":
            subs = load_subscribers()
            is_sub = "✅ Activadas para este chat" if chat_id in subs else "❌ Desactivadas (usa /alertas para activarlas)"
            msg = (
                "📡 <b>Estado del Monitor en Tiempo Real</b>\n\n"
                f"• Origen por defecto: <b>{config.DEFAULT_ORIGIN}</b>\n"
                f"• Intervalo de escaneo: <b>Cada {config.SCAN_INTERVAL_MINUTES} minutos</b>\n"
                f"• Umbral de chollos: <b>Vuelos ≤ {config.ALERT_MAX_PRICE} €</b>\n"
                f"• Tus alertas: <b>{is_sub}</b>\n"
                f"• Dispositivos suscritos totales: <b>{len(subs)}</b>"
            )
            self.send_message(chat_id, msg)

        elif cmd == "/chollos":
            self.send_message(chat_id, "🔍 Buscando chollos mundiales (5 a 9 días) para 2027...")
            flights, _ = fetch_flights(origin=config.DEFAULT_ORIGIN, year=2027, min_duration=5, max_duration=9)
            filtered = apply_flight_filters(flights, {"require_different_airlines": True}) or flights
            self._send_flight_list(chat_id, filtered[:5], origin=config.DEFAULT_ORIGIN, min_d=5, max_d=9)

        elif cmd == "/vuelos":
            origin = parts[1].upper() if len(parts) > 1 else config.DEFAULT_ORIGIN
            base_days = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 7
            flex = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 2
            
            min_d = max(1, base_days - flex)
            max_d = base_days + flex

            orig_info = get_airport_info(origin)
            self.send_message(
                chat_id,
                f"🔎 Buscando vuelos desde <b>{orig_info['flag']} {orig_info['city']} [{origin}]</b> para 2027 ({min_d} a {max_d} días)..."
            )
            
            flights, _ = fetch_flights(origin=origin, year=2027, min_duration=min_d, max_duration=max_d)
            self._send_flight_list(chat_id, flights[:8], origin=origin, min_d=min_d, max_d=max_d)

        else:
            self.send_message(
                chat_id,
                "❓ Comando no reconocido. Escribe <code>/vuelos MAD</code>, <code>/alertas</code> o <code>/ayuda</code>."
            )

    def _send_flight_list(self, chat_id: int, flights: list, origin: str, min_d: int, max_d: int):
        if not flights:
            self.send_message(chat_id, "❌ No se encontraron vuelos disponibles con esos criterios.")
            return

        orig_info = get_airport_info(origin)
        msg_lines = [
            f"🌍 <b>Destinos más baratos en 2027</b>",
            f"📍 Origen: {orig_info['flag']} <b>{orig_info['city']} [{origin}]</b>",
            f"⏱️ Estancia: <b>{min_d} a {max_d} días</b>\n"
        ]

        for idx, f in enumerate(flights, start=1):
            stay = f.get('duration_days', 7)
            diff_tag = "🔀 Cías. Distintas" if f.get('different_airlines') else "Misma Cía"
            line = (
                f"<b>{idx}. {f['dest_flag']} {f['dest_city']} ({f['dest_country']})</b>\n"
                f"   💵 <b>Vuelo I/V: {f['price']:.0f} {f['currency']}</b> ({stay} días • {diff_tag})\n"
                f"   🏨 Alojamiento est.: ~{f.get('hotel_price_per_night', 0)}€/noche (~{f.get('hotel_total_est', 0)}€ estancia)\n"
                f"   🏷️ <b>Total viaje estimado: ~{f.get('trip_total_est', 0)} €</b>\n"
                f"   🛫 Ida: {f.get('outbound_dep_time')} ➔ {f.get('outbound_arr_time')} ({f.get('outbound_airline')})\n"
                f"   🛬 Vuelta: {f.get('return_dep_time')} ➔ {f.get('return_arr_time')} ({f.get('return_airline')})\n"
                f"   🔍 Comparar: <a href=\"{f['direct_link']}\">Google</a> | <a href=\"{f['skyscanner_link']}\">Skyscanner</a> | <a href=\"{f['kayak_link']}\">Kayak</a>\n"
                f"   🏨 Hoteles: <a href=\"{f['booking_link']}\">Booking</a> | <a href=\"{f['airbnb_link']}\">Airbnb</a>\n"
            )
            msg_lines.append(line)

        self.send_message(chat_id, "\n".join(msg_lines))

    def run(self):
        """Bucle principal de escucha con Long Polling."""
        print("🤖 Bot de Telegram en ejecución. Esperando mensajes...")
        print("💡 Para activar alertas al móvil, abre tu chat con el bot y escribe /alertas")
        print("💡 Para detener el bot, presiona Ctrl + C.")
        
        while True:
            try:
                url = f"{self.base_url}/getUpdates"
                params = {"offset": self.offset, "timeout": 20}
                resp = requests.get(url, params=params, timeout=25)
                
                if resp.status_code == 200:
                    data = resp.json()
                    for update in data.get("result", []):
                        self.offset = update["update_id"] + 1
                        message = update.get("message")
                        if message and "text" in message:
                            chat_id = message["chat"]["id"]
                            text = message["text"]
                            user = message.get("from", {}).get("first_name", "Usuario")
                            print(f"📩 Mensaje recibido de {user}: {text}")
                            self.handle_command(chat_id, text)
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Bot detenido.")
                break
            except Exception as e:
                print(f"Error en polling: {e}")
                time.sleep(3)


def main():
    if not config.TELEGRAM_BOT_TOKEN:
        print("=" * 70)
        print("⚠️  ATENCIÓN: Falta el token de Telegram (TELEGRAM_BOT_TOKEN).")
        print("Para recibir alertas en tu móvil:")
        print("1. Abre Telegram y busca @BotFather")
        print("2. Escribe /newbot y sigue las instrucciones para crear tu bot.")
        print("3. Pega el token recibido en el archivo .env:")
        print("   TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz")
        print("=" * 70)
        return

    bot = TelegramFlightBot(token=config.TELEGRAM_BOT_TOKEN)
    bot.run()


if __name__ == "__main__":
    main()

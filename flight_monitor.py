#!/usr/bin/env python3
"""
========================================================================
📡  MONITOR EN TIEMPO REAL DE VUELOS 2027 CON ALERTAS AL TELÉFONO  📡
========================================================================
Ejecuta un ciclo continuo que:
1. Rastrea vuelos y ofertas a todo el mundo a lo largo del tiempo.
2. Detecta bajadas de precio y nuevos chollos frente al escaneo anterior.
3. Envía notificaciones push automáticas a Telegram (móvil).
4. Actualiza en vivo el panel HTML interactivo (comparador_vuelos_2027.html).
"""

import time
import argparse
import webbrowser
from datetime import datetime
from typing import Dict, Any

import config
from flight_scanner import fetch_flights
from filter_engine import apply_flight_filters
from tracker import analyze_new_deals, load_subscribers
from notifier import send_deal_alert, get_all_target_chats
from reporter import export_to_html, export_to_csv
from airports_db import get_airport_info


def print_monitor_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════════╗
    ║        📡  MONITOR CONTINUO EN TIEMPO REAL - VUELOS BARATOS 2027 ✈️ 🔔            ║
    ║        Detección de Bajadas • Avisos al Móvil • Actualización en Vivo            ║
    ╚══════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_monitor(
    origin: str = "MAD",
    year: int = 2027,
    min_duration: int = 5,
    max_duration: int = 9,
    interval_minutes: int = 30,
    alert_max_price: float = 100.0,
    filters: Dict[str, Any] = None,
    open_browser_on_start: bool = True
):
    print_monitor_banner()
    orig_info = get_airport_info(origin)
    filters = filters or {}

    print(f"📍 Aeropuerto de Origen: {orig_info['flag']} {orig_info['city']} [{origin}]")
    print(f"📅 Año de Búsqueda: {year} (Estancia: {min_duration} a {max_duration} días)")
    print(f"⏱️  Intervalo de escaneo: Cada {interval_minutes} minutos")
    print(f"💰 Umbral de Alerta a tu teléfono: Vuelos ≤ {alert_max_price:.0f} € o bajadas de precio")
    
    target_chats = get_all_target_chats()
    if target_chats:
        print(f"📱 Dispositivos suscritos para recibir alertas al móvil: {len(target_chats)} chat(s)")
    else:
        print("⚠️  Aviso: No hay teléfonos suscritos todavía.")
        print("   👉 Para recibir los avisos en tu móvil: abre Telegram, habla con tu bot y escribe /alertas")

    print("\n🟢 Iniciando primer escaneo en tiempo real...")
    first_run = True

    try:
        iteration = 1
        while True:
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"\n[{now_str}] 🔎 Escaneo #{iteration} en curso...")

            # 1. Obtener vuelos
            raw_flights, source = fetch_flights(
                origin=origin,
                year=year,
                min_duration=min_duration,
                max_duration=max_duration
            )

            # 2. Aplicar filtros opcionales de usuario
            filtered_flights = apply_flight_filters(raw_flights, filters)

            # 3. Analizar contra historial para detectar bajadas de precio y nuevos chollos
            deals_found, enriched_flights = analyze_new_deals(
                filtered_flights,
                alert_max_price=alert_max_price
            )

            # 4. Actualizar el panel interactivo HTML y el archivo CSV
            duration_label = f"{min_duration} a {max_duration} días"
            html_file = export_to_html(
                enriched_flights,
                origin=origin,
                duration_info=duration_label,
                last_update=now_str,
                refresh_seconds=interval_minutes * 60
            )
            csv_file = export_to_csv(enriched_flights)

            print(f"✅ Panel web actualizado: {html_file}")
            print(f"📊 Opciones analizadas: {len(enriched_flights)} destinos")

            # Abrir navegador en la primera iteración si se indicó
            if first_run and open_browser_on_start:
                webbrowser.open(f"file://{html_file}")
                first_run = False

            # 5. Notificar alertas al teléfono si hay novedades
            if deals_found:
                print(f"🚨 ¡Se han detectado {len(deals_found)} oferta(s) para avisar!")
                for deal in deals_found:
                    deal_type_desc = "Bajada de precio" if deal.get("deal_type") == "price_drop" else "Chollo destacado"
                    print(f"   📲 Enviando aviso de {deal['dest_flag']} {deal['dest_city']} ({deal['price']:.0f} € - {deal_type_desc})...")
                    sent = send_deal_alert(deal)
                    if sent > 0:
                        print(f"      ✉️ Notificación entregada a {sent} dispositivo(s).")
            else:
                print("ℹ️  No hay variaciones de precio en esta ronda. Todo monitorizado.")

            iteration += 1
            wait_seconds = interval_minutes * 60
            print(f"⏳ Próxima comprobación en {interval_minutes} minutos. Presiona Ctrl + C para detener.")

            # Espera con cuenta atrás
            time.sleep(wait_seconds)

    except KeyboardInterrupt:
        print("\n\n🛑 Monitor en tiempo real detenido por el usuario.")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor en tiempo real de vuelos 2027 con alertas al móvil."
    )
    parser.add_argument("--origin", "-o", default=None, help="Código IATA del aeropuerto origen (ej. MAD)")
    parser.add_argument("--duration", "-d", type=int, default=7, help="Duración central en días (por defecto: 7)")
    parser.add_argument("--flex", "-f", type=int, default=2, help="Flexibilidad en días (+/-) (por defecto: 2)")
    parser.add_argument("--year", "-y", type=int, default=2027, help="Año de búsqueda (por defecto: 2027)")
    parser.add_argument("--interval", "-i", type=int, default=None, help="Intervalo de escaneo en minutos (por defecto en config o 30)")
    parser.add_argument("--max-alert-price", type=float, default=None, help="Precio máximo para alertar un nuevo chollo (ej. 80)")
    parser.add_argument("--distintas-companias", action="store_true", help="Exige aerolíneas distintas en ida y vuelta")
    parser.add_argument("--max-hours-ida", type=float, default=None, help="Tope horas ida")
    parser.add_argument("--max-hours-vuelta", type=float, default=None, help="Tope horas vuelta")
    parser.add_argument("--no-browser", action="store_true", help="No abrir el navegador automáticamente")

    args = parser.parse_args()

    origin = (args.origin or config.DEFAULT_ORIGIN or "MAD").upper()
    interval = args.interval or config.SCAN_INTERVAL_MINUTES or 30
    alert_price = args.max_alert_price or config.ALERT_MAX_PRICE or 100.0

    min_duration = max(1, args.duration - args.flex)
    max_duration = args.duration + args.flex

    filters = {
        "require_different_airlines": args.distintas_companias,
        "max_hours_outbound": args.max_hours_ida,
        "max_hours_return": args.max_hours_vuelta
    }

    run_monitor(
        origin=origin,
        year=args.year,
        min_duration=min_duration,
        max_duration=max_duration,
        interval_minutes=interval,
        alert_max_price=alert_price,
        filters=filters,
        open_browser_on_start=not args.no_browser
    )


if __name__ == "__main__":
    main()

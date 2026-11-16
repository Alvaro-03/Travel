#!/usr/bin/env python3
"""
========================================================================
✈️  EXPLORADOR Y COMPARADOR MUNDIAL DE VUELOS BARATOS 2027  ✈️
========================================================================
Permite buscar los vuelos más baratos hacia cualquier rincón del mundo
para viajes de duración flexible (ej. 1 semana +/- 2 días) con:
- Estimación de costes de alojamiento (por noche y total del viaje)
- Enlaces y comprobación en múltiples plataformas (Google, Skyscanner, Kayak, Kiwi, Momondo)
- Webs directas oficiales de las aerolíneas (Ida y Vuelta)
- Filtros opcionales de horas máximas de vuelo, franjas horarias y aerolíneas combinadas
- Modo monitorización en tiempo real con alertas al móvil
"""

import sys
import argparse
import webbrowser
from typing import List, Dict, Any, Tuple, Optional

import config
from amadeus_client import AmadeusClient
from kiwi_client import KiwiClient
from mock_data import get_demo_flights
from filter_engine import apply_flight_filters
from reporter import export_to_html, export_to_csv
from airports_db import get_airport_info


def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════════╗
    ║        🌍  COMPARADOR DE VUELOS Y VIAJES POR EL MUNDO (2027) ✈️ 🏨                 ║
    ║        Multi-Buscadores • Webs Aerolíneas • Estimación Alojamiento • Horarios    ║
    ╚══════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_flights_table(flights: List[Dict[str, Any]], limit: int = 25):
    """Muestra los vuelos en la terminal incluyendo la estimación de alojamiento y aerolíneas."""
    if not flights:
        print("\n❌ No se encontraron opciones que cumplan con todos los criterios.\n")
        return

    print("\n" + "=" * 126)
    print(f"{'#':<3} | {'DESTINO':<22} | {'DÍAS':<5} | {'VUELO I/V':<10} | {'HOTEL/NOCHE':<12} | {'HOTEL TOTAL':<12} | {'TOTAL VIAJE':<12} | {'AEROLÍNEAS (IDA ➔ VUELTA)'}")
    print("=" * 126)

    for idx, f in enumerate(flights[:limit], start=1):
        city_str = f"{f['dest_flag']} {f['dest_city'][:15]} [{f['destination']}]"
        stay_str = f"{f.get('duration_days', 7)}d"
        vuelo_str = f"{f['price']:.0f} {f['currency']}"
        hotel_night_str = f"~{f.get('hotel_price_per_night', 0)} €/noche"
        hotel_total_str = f"~{f.get('hotel_total_est', 0)} €"
        trip_total_str = f"~{f.get('trip_total_est', 0)} €"

        out_air = f.get('outbound_airline', 'Varios')[:10]
        ret_air = f.get('return_airline', 'Varios')[:10]
        diff_mark = "🔀" if f.get("different_airlines") else "•"
        airlines_str = f"{diff_mark} {out_air} ➔ {ret_air}"

        print(f"{idx:<3} | {city_str:<22} | {stay_str:<5} | {vuelo_str:<10} | {hotel_night_str:<12} | {hotel_total_str:<12} | {trip_total_str:<12} | {airlines_str}")

    print("=" * 126)
    print(f"Mostrando {min(len(flights), limit)} opciones ordenadas por el precio del vuelo más barato.")
    print("💡 Nota: El coste de alojamiento es una estimación media y no altera el orden de los vuelos más baratos.\n")


def fetch_flights(
    origin: str,
    year: int = 2027,
    min_duration: int = 5,
    max_duration: int = 9,
    max_price: int = None,
    force_source: str = "auto"
) -> Tuple[List[Dict[str, Any]], str]:
    """Consulta vuelos según las APIs configuradas o recurre al modo demo."""
    if force_source == "demo":
        print("ℹ️  Modo DEMO activado explícitamente.")
        flights = get_demo_flights(origin=origin, year=year, min_duration=min_duration, max_duration=max_duration)
        return flights, "demo"

    # 1. Intentar con Amadeus si hay credenciales
    if config.has_amadeus_keys() and force_source in ("auto", "amadeus"):
        try:
            print(f"📡 Conectando a la API de Amadeus ({config.AMADEUS_ENV})...")
            client = AmadeusClient()
            date_range = f"{year}-01-01,{year}-10-31"
            flights = client.search_cheapest_destinations(
                origin=origin,
                departure_date_range=date_range,
                min_duration=min_duration,
                max_duration=max_duration,
                max_price=max_price
            )
            if flights:
                return flights, "amadeus"
        except Exception as e:
            print(f"⚠️  Aviso: Consulta a Amadeus falló ({e}).")

    # 2. Intentar con Kiwi si hay credenciales
    if config.has_kiwi_key() and force_source in ("auto", "kiwi"):
        try:
            print("📡 Conectando a la API de Kiwi Tequila...")
            client = KiwiClient()
            flights = client.search_anywhere(
                origin=origin,
                date_from=f"01/01/{year}",
                date_to=f"31/10/{year}",
                min_nights=min_duration,
                max_nights=max_duration,
                max_price=max_price,
                currency=config.DEFAULT_CURRENCY
            )
            if flights:
                return flights, "kiwi"
        except Exception as e:
            print(f"⚠️  Aviso: Consulta a Kiwi falló ({e}).")

    # Fallback al modo Demo
    print("ℹ️  No se encontraron claves de API en el archivo .env o la consulta falló.")
    print(f"👉 Mostrando datos simulados realistas de 2027 (duración flexible: {min_duration} a {max_duration} días).")
    print("💡 Para conectar con datos en vivo 100% reales, introduce tus claves gratuitas en el archivo .env\n")
    flights = get_demo_flights(origin=origin, year=year, min_duration=min_duration, max_duration=max_duration)
    return flights, "demo"


def run_interactive_menu():
    """Menú interactivo con soporte de filtros opcionales avanzados y estimación hotelera."""
    print_banner()

    default_orig = config.DEFAULT_ORIGIN or "MAD"
    orig_input = input(f"📍 Aeropuerto de origen [IATA, Enter para {default_orig}]: ").strip().upper()
    origin = orig_input if orig_input else default_orig
    origin_info = get_airport_info(origin)
    print(f"✈️  Origen seleccionado: {origin_info['flag']} {origin_info['city']} ({origin_info['country']}) [{origin}]")

    dur_input = input("⏳ Duración central en días [Enter para 7 días / 1 semana]: ").strip()
    target_duration = int(dur_input) if dur_input.isdigit() else 7

    flex_input = input("🔀 Flexibilidad en días (+/-) [Enter para 2 días (viajes de 5 a 9 días)]: ").strip()
    flexibility = int(flex_input) if flex_input.isdigit() else 2

    min_duration = max(1, target_duration - flexibility)
    max_duration = target_duration + flexibility

    year_input = input("📅 Año de búsqueda [Enter para 2027]: ").strip()
    year = int(year_input) if year_input.isdigit() else 2027

    price_input = input("💰 Presupuesto máximo del VUELO en EUR [Enter para sin límite]: ").strip()
    max_price = int(price_input) if price_input.isdigit() else None

    # Preguntar si desea configurar filtros avanzados opcionales
    filters: Dict[str, Any] = {}
    print("\n" + "-" * 75)
    adv_choice = input("⚙️  ¿Deseas configurar filtros avanzados (tope horas, horarios, aerolíneas)? [s/N]: ").strip().lower()
    
    if adv_choice == "s":
        print("\n💡 Nota: Si no especificas un valor (pulsas Enter), ese filtro se ignora.")
        
        # 1. Tope de horas
        h_ida = input("⏱️  Horas máximas de vuelo para la IDA (ej. 4.5) [Enter = sin límite]: ").strip()
        if h_ida:
            try: filters["max_hours_outbound"] = float(h_ida)
            except ValueError: pass

        h_vta = input("⏱️  Horas máximas de vuelo para la VUELTA (ej. 5.0) [Enter = sin límite]: ").strip()
        if h_vta:
            try: filters["max_hours_return"] = float(h_vta)
            except ValueError: pass

        # 2. Franja de salida ida
        sal_ida_min = input("🌅 Salida de IDA NO antes de las (HH:MM, ej. 08:00) [Enter = sin filtro]: ").strip()
        if sal_ida_min: filters["outbound_dep_from"] = sal_ida_min
        
        sal_ida_max = input("🌅 Salida de IDA NO después de las (HH:MM, ej. 14:00) [Enter = sin filtro]: ").strip()
        if sal_ida_max: filters["outbound_dep_to"] = sal_ida_max

        # 3. Franja de salida vuelta
        sal_vta_min = input("🌇 Salida de VUELTA NO antes de las (HH:MM, ej. 16:00) [Enter = sin filtro]: ").strip()
        if sal_vta_min: filters["return_dep_from"] = sal_vta_min

        sal_vta_max = input("🌇 Salida de VUELTA NO después de las (HH:MM, ej. 22:00) [Enter = sin filtro]: ").strip()
        if sal_vta_max: filters["return_dep_to"] = sal_vta_max

        # 4. Aerolíneas distintas
        diff_air = input("✨ ¿Exigir compañías aéreas distintas en ida y vuelta? [s/N]: ").strip().lower()
        if diff_air == "s":
            filters["require_different_airlines"] = True

    print(f"\n🔍 Buscando los vuelos más baratos del mundo desde {origin} para {year} ({min_duration} a {max_duration} días)...")
    raw_flights, source = fetch_flights(
        origin=origin,
        year=year,
        min_duration=min_duration,
        max_duration=max_duration,
        max_price=max_price
    )

    if max_price:
        raw_flights = [f for f in raw_flights if f["price"] <= max_price]

    filtered_flights = apply_flight_filters(raw_flights, filters)
    display_flights_table(filtered_flights)

    duration_label = f"{min_duration} a {max_duration} días (~{target_duration} días +/- {flexibility})"
    print("Acciones disponibles:")
    print("1. Abrir panel visual interactivo en el navegador (HTML)")
    print("2. Exportar resultados a Excel / CSV")
    print("3. Ambas (HTML + CSV)")
    print("4. 📡 Iniciar Monitor en TIEMPO REAL continuo (con avisos automáticos al móvil)")
    print("5. Salir")
    choice = input("Elige una opción [1/2/3/4/5, por defecto 1]: ").strip() or "1"

    if choice in ("1", "3"):
        html_file = export_to_html(filtered_flights, origin=origin, duration_info=duration_label)
        print(f"✅ Panel HTML generado: {html_file}")
        webbrowser.open(f"file://{html_file}")
    if choice in ("2", "3"):
        csv_file = export_to_csv(filtered_flights)
        print(f"✅ Archivo CSV generado: {csv_file}")
    if choice == "4":
        from flight_monitor import run_monitor
        run_monitor(
            origin=origin,
            year=year,
            min_duration=min_duration,
            max_duration=max_duration,
            interval_minutes=config.SCAN_INTERVAL_MINUTES,
            alert_max_price=config.ALERT_MAX_PRICE,
            filters=filters,
            open_browser_on_start=True
        )

    print("\n👋 ¡Buen viaje y feliz búsqueda de chollos!\n")


def main():
    parser = argparse.ArgumentParser(
        description="Buscador mundial de vuelos y viajes 2027 con estimación de alojamiento y multi-buscador."
    )
    parser.add_argument("--origin", "-o", default=None, help="Código IATA del aeropuerto origen (ej. MAD, BCN)")
    parser.add_argument("--duration", "-d", type=int, default=7, help="Duración central del viaje en días (por defecto: 7)")
    parser.add_argument("--flex", "-f", type=int, default=2, help="Margen de flexibilidad en días (+/-) (por defecto: 2)")
    parser.add_argument("--min-days", type=int, default=None, help="Días mínimos explícitos (ej. 5)")
    parser.add_argument("--max-days", type=int, default=None, help="Días máximos explícitos (ej. 9)")
    parser.add_argument("--year", "-y", type=int, default=2027, help="Año de viaje (por defecto: 2027)")
    parser.add_argument("--max-price", "-m", type=int, default=None, help="Precio máximo deseado para el vuelo")

    # Monitor continuo
    parser.add_argument("--monitor", action="store_true", help="Inicia el monitor en tiempo real continuo con alertas")
    parser.add_argument("--interval", "-i", type=int, default=None, help="Intervalo del monitor en minutos")

    # Filtros de horas de vuelo
    parser.add_argument("--max-hours-ida", type=float, default=None, help="Tope de horas de vuelo para la ida")
    parser.add_argument("--max-hours-vuelta", type=float, default=None, help="Tope de horas de vuelo para la vuelta")

    # Franjas horarias
    parser.add_argument("--salida-ida-min", default=None, help="Hora mínima salida ida (HH:MM)")
    parser.add_argument("--salida-ida-max", default=None, help="Hora máxima salida ida (HH:MM)")
    parser.add_argument("--llegada-ida-min", default=None, help="Hora mínima llegada ida (HH:MM)")
    parser.add_argument("--llegada-ida-max", default=None, help="Hora máxima llegada ida (HH:MM)")
    parser.add_argument("--salida-vuelta-min", default=None, help="Hora mínima salida vuelta (HH:MM)")
    parser.add_argument("--salida-vuelta-max", default=None, help="Hora máxima salida vuelta (HH:MM)")
    parser.add_argument("--llegada-vuelta-min", default=None, help="Hora mínima llegada vuelta (HH:MM)")
    parser.add_argument("--llegada-vuelta-max", default=None, help="Hora máxima llegada vuelta (HH:MM)")

    # Aerolíneas
    parser.add_argument("--distintas-companias", action="store_true", help="Exige aerolíneas distintas en ida y vuelta")

    # Ordenación
    parser.add_argument("--sort-by", choices=["flight", "trip", "hotel"], default="flight", help="Criterio de ordenación")

    parser.add_argument("--source", choices=["auto", "amadeus", "kiwi", "demo"], default="auto", help="Fuente de datos")
    parser.add_argument("--export", choices=["none", "html", "csv", "all"], default="none", help="Exportar reporte")
    parser.add_argument("--open-browser", action="store_true", help="Abrir el informe HTML en el navegador al terminar")

    args = parser.parse_args()

    # Si se pide monitor directamente
    if args.monitor:
        from flight_monitor import run_monitor
        origin = (args.origin or config.DEFAULT_ORIGIN or "MAD").upper()
        min_d = args.min_days or max(1, args.duration - args.flex)
        max_d = args.max_days or (args.duration + args.flex)
        filters = {
            "require_different_airlines": args.distintas_companias,
            "max_hours_outbound": args.max_hours_ida,
            "max_hours_return": args.max_hours_vuelta
        }
        run_monitor(
            origin=origin,
            year=args.year,
            min_duration=min_d,
            max_duration=max_d,
            interval_minutes=args.interval or config.SCAN_INTERVAL_MINUTES or 30,
            alert_max_price=args.max_price or config.ALERT_MAX_PRICE or 100.0,
            filters=filters,
            open_browser_on_start=not args.open_browser
        )
        return

    if args.origin is None and args.export == "none" and not args.open_browser and args.max_hours_ida is None:
        run_interactive_menu()
        return

    if args.min_days is not None and args.max_days is not None:
        min_duration = args.min_days
        max_duration = args.max_days
    else:
        min_duration = max(1, args.duration - args.flex)
        max_duration = args.duration + args.flex

    origin = (args.origin or config.DEFAULT_ORIGIN or "MAD").upper()
    print_banner()
    print(f"🔍 Buscando destinos más baratos desde {origin} para {args.year} ({min_duration} a {max_duration} días)...")
    
    raw_flights, source = fetch_flights(
        origin=origin,
        year=args.year,
        min_duration=min_duration,
        max_duration=max_duration,
        max_price=args.max_price,
        force_source=args.source
    )

    if args.max_price:
        raw_flights = [f for f in raw_flights if f["price"] <= args.max_price]

    filters = {
        "max_hours_outbound": args.max_hours_ida,
        "max_hours_return": args.max_hours_vuelta,
        "outbound_dep_from": args.salida_ida_min,
        "outbound_dep_to": args.salida_ida_max,
        "outbound_arr_from": args.llegada_ida_min,
        "outbound_arr_to": args.llegada_ida_max,
        "return_dep_from": args.salida_vuelta_min,
        "return_dep_to": args.salida_vuelta_max,
        "return_arr_from": args.llegada_vuelta_min,
        "return_arr_to": args.llegada_vuelta_max,
        "require_different_airlines": args.distintas_companias,
    }

    filtered_flights = apply_flight_filters(raw_flights, filters)

    # Ordenación
    if args.sort_by == "trip":
        filtered_flights.sort(key=lambda x: x.get("trip_total_est", 0))
    elif args.sort_by == "hotel":
        filtered_flights.sort(key=lambda x: x.get("hotel_price_per_night", 0))
    else:
        filtered_flights.sort(key=lambda x: x["price"])

    display_flights_table(filtered_flights)

    duration_label = f"{min_duration} a {max_duration} días (~{args.duration} días +/- {args.flex})"

    if args.export in ("html", "all") or args.open_browser:
        html_file = export_to_html(filtered_flights, origin=origin, duration_info=duration_label)
        print(f"📄 Reporte HTML creado: {html_file}")
        if args.open_browser:
            webbrowser.open(f"file://{html_file}")

    if args.export in ("csv", "all"):
        csv_file = export_to_csv(filtered_flights)
        print(f"📊 Archivo CSV creado: {csv_file}")


if __name__ == "__main__":
    main()

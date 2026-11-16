#!/usr/bin/env python3
"""
Servidor web ligero para desplegar en la nube (Render, Railway, Fly.io, VPS).
- Sirve el panel comparador_vuelos_2027.html en el puerto asignado (PORT).
- Ejecuta el monitor en segundo plano para escanear vuelos y enviar alertas a Telegram.
- Todo con la biblioteca estándar de Python (sin dependencias adicionales).
"""

import os
import sys
import threading
import http.server
import socketserver
from pathlib import Path

import config
from flight_monitor import run_monitor

PORT = int(os.getenv("PORT", 8080))
BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "comparador_vuelos_2027.html"


class FlightDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        # Redirigir la raíz al panel HTML
        if self.path == "/" or self.path == "":
            self.path = "/comparador_vuelos_2027.html"
        return super().do_GET()


def start_web_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), FlightDashboardHandler) as httpd:
        print(f"🌐 Servidor Web activo en http://0.0.0.0:{PORT}")
        print(f"📄 Dashboard visible en: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except Exception as e:
            print(f"Servidor web detenido: {e}")


def main():
    print("=" * 80)
    print("🚀 INICIANDO SERVICIO EN LA NUBE (SERVIDOR WEB + MONITOR CONTINUO) 🚀")
    print("=" * 80)

    # 1. Hilo en segundo plano: Monitor de vuelos con alertas a Telegram
    monitor_thread = threading.Thread(
        target=run_monitor,
        kwargs={
            "origin": config.DEFAULT_ORIGIN,
            "year": 2027,
            "min_duration": 5,
            "max_duration": 9,
            "interval_minutes": config.SCAN_INTERVAL_MINUTES,
            "alert_max_price": config.ALERT_MAX_PRICE,
            "open_browser_on_start": False
        },
        daemon=True
    )
    monitor_thread.start()
    print("📡 Hilo del monitor de vuelos iniciado en segundo plano.")

    # 2. Hilo principal: Servidor web accesible desde el móvil o cualquier navegador
    start_web_server()


if __name__ == "__main__":
    main()

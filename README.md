# ✈️ Monitor Mundial de Vuelos y Viajes 2027 en Tiempo Real

Sistema integral en Python para rastrear y comparar los vuelos más baratos hacia **cualquier parte del mundo** para viajes de **duración flexible (ej. 5 a 9 días)** durante el año **2027**, con:

- ☁️ **Ejecución en la Nube 24/7 (Sin tener el ordenador encendido)**: Puedes ejecutarlo gratis en GitHub Actions, Render, Railway o un VPS para apagar tu PC completamente. Consulta la guía en [DESPLIEGUE_NUBE.md](DESPLIEGUE_NUBE.md).
- 📡 **Monitorización en Tiempo Real**: Escaneo continuo en segundo plano a lo largo del tiempo.
- 🔔 **Alertas Push al Teléfono Móvil**: Avisos instantáneos por **Telegram** cada vez que:
  - Un vuelo **baja de precio** frente al escaneo anterior.
  - Aparece un **nuevo chollo** por debajo de tu presupuesto objetivo (ej. ≤ 100€).
- 🌐 **Panel Web Auto-Actualizable ([comparador_vuelos_2027.html](comparador_vuelos_2027.html))**: Se actualiza y recarga automáticamente en tu navegador con una barra de estado en vivo (🟢 *Live*), contador regresivo y distintivos destacados para los chollos recién detectados.
- 🏨 **Estimación de Alojamiento**: Media por noche (€/noche), total estancia y presupuesto global (Vuelo + Hotel).
- 🔍 **Comprobación en Múltiples Plataformas**:
  - Metabuscadores: **Google Flights**, **Skyscanner**, **Kayak**, **Kiwi.com**, **Momondo**.
  - **Webs Oficiales de las Aerolíneas**: Enlaces directos a las páginas oficiales de cada compañía que opera el vuelo (Ida y Vuelta).
  - Portales de Alojamiento: **Booking.com**, **Airbnb**, **Google Hotels**.
- ⏱️ **Tope de Horas y Horarios Opcionales**: Límite de horas en el avión y franjas horarias deseadas para ida y vuelta.
- 🔀 **Compañías Combinadas (*Hacker Fares*)**: Soporta y permite exigir aerolíneas distintas en ida y vuelta.

---

## 📱 Cómo Activar las Alertas al Móvil (en 2 minutos)

1. En Telegram, busca el bot oficial `@BotFather` y escribe `/newbot`.
2. Sigue los pasos y copia el token que te dé.
3. Pégalo en tu archivo [.env](.env):
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz
   ```
4. Abre Telegram, entra en tu nuevo bot y escribe:
   ```text
   /alertas
   ```
   *El bot responderá: "🔔 ¡Alertas en tiempo real activadas!" y tu teléfono quedará registrado.*
5. ¡Listo! A partir de ese instante, cualquier vuelo que baje de precio o cualquier nuevo chollo que detecte el monitor te llegará al móvil como notificación push.

---

## 🚀 Modos de Ejecución

### 1. Iniciar el Monitor en Tiempo Real (En local)

```bash
python flight_monitor.py --origin MAD --duration 7 --flex 2 --interval 30 --max-alert-price 100
```

### 2. Servidor Web Local / Nube

```bash
python web_server.py
```
*(Inicia el servidor web en http://localhost:8080 y arranca el monitor de vuelos en segundo plano).*

### 3. Ejecución en la Nube 24/7 (Ordenador Apagado)
Consulta la guía completa paso a paso en [DESPLIEGUE_NUBE.md](DESPLIEGUE_NUBE.md).

---

## 📁 Estructura del Sistema

- [web_server.py](web_server.py): Servidor HTTP ligero para desplegar en servicios en la nube.
- [flight_monitor.py](flight_monitor.py): Bucle de monitorización continua en tiempo real.
- [tracker.py](tracker.py): Historial de escaneos previos, detección de bajadas de precio y gestión de suscriptores al móvil.
- [notifier.py](notifier.py): Despachador de notificaciones push formateadas con emojis, enlaces directos y detalles de hotel.
- [telegram_bot.py](telegram_bot.py): Bot de Telegram interactivo con comandos `/alertas`, `/estado`, `/vuelos` y `/chollos`.
- [comparador_vuelos_2027.html](comparador_vuelos_2027.html): Dashboard web interactivo con refresco automático en vivo.
- [providers.py](providers.py): Enlaces dinámicos a Google, Skyscanner, Kayak, Kiwi, Momondo, Booking, Airbnb y webs de aerolíneas.
- [accommodation_db.py](accommodation_db.py): Estimador de costes medios de alojamiento.
- [filter_engine.py](filter_engine.py): Filtros de tope de horas y franjas horarias.
- [DESPLIEGUE_NUBE.md](DESPLIEGUE_NUBE.md): Opciones para correrlo en la nube gratis.
- [config.py](config.py) y [.env](.env): Configuración central y credenciales.

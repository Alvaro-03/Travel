# ☁️ Guía de Despliegue en la Nube (24/7 sin encender tu ordenador)

No necesitas tener tu ordenador encendido ni consumiendo electricidad para que el monitor siga buscando ofertas y avisándote al móvil. Tienes las siguientes opciones gratuitas y sencillas:

---

## 🏆 Opción 1: GitHub Actions + GitHub Pages (100% Gratuita, Sin Servidores)
*La opción recomendada para no pagar nada ni configurar servidores.*

### ¿Cómo funciona?
- **GitHub ejecuta el script en sus servidores en la nube** de forma programada (por ejemplo, cada 2 horas o 1 hora).
- Tu ordenador puede estar totalmente **apagado**.
- Si detecta un chollo o bajada de precio, **te llega la notificación a Telegram en tu móvil**.
- Además, actualiza automáticamente la web en **GitHub Pages**, dándote un enlace público (ej. `https://tu-usuario.github.io/viajes/`) que puedes abrir desde el móvil cuando quieras.

### Pasos para activarla (en 3 minutos):
1. Sube esta carpeta a un repositorio en tu cuenta de [GitHub](https://github.com) (puede ser público o privado).
2. En GitHub, ve a **Settings** > **Secrets and variables** > **Actions** y añade tus secretos:
   - `AMADEUS_CLIENT_ID`
   - `AMADEUS_CLIENT_SECRET`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. El archivo de automatización ya lo tienes listo en [.github/workflows/flight_scanner.yml](.github/workflows/flight_scanner.yml).
4. Para activar la web: ve a **Settings** > **Pages** > en *Branch* selecciona `gh-pages` y pulsa *Save*.
5. ¡Listo! Se ejecutará automáticamente según la programación fijada y podrás apagar tu PC.

---

## ⚡ Opción 2: Plataformas PaaS 24/7 (Render / Railway)
*Ideal si quieres tener un proceso continuo 24/7 y una página web activa al instante.*

Hemos creado el archivo [web_server.py](web_server.py), [Dockerfile](Dockerfile) y [Procfile](Procfile) listos para estas plataformas.

### Pasos en Render (Gratis):
1. Entra en [Render.com](https://render.com) y crea una cuenta.
2. Haz clic en **New +** > **Web Service**.
3. Conecta tu repositorio de GitHub.
4. En *Runtime* elige **Python** o **Docker**.
5. En *Environment Variables*, añade:
   - `AMADEUS_CLIENT_ID`
   - `AMADEUS_CLIENT_SECRET`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
6. Pulsa **Deploy**.
   - Render mantendrá el monitor ejecutándose en segundo plano enviando alertas a tu móvil.
   - Te dará una URL directa (ej. `https://viajes-2027.onrender.com`) accesible desde tu teléfono 24/7.

---

## 💻 Opción 3: Servidor VPS "Always Free" (Oracle Cloud)
*Para usuarios que prefieren tener una máquina virtual completa sin pagar nada.*

Oracle Cloud ofrece instancias gratuitas para siempre (*Always Free Tier*):
1. Regístrate en [Oracle Cloud](https://www.oracle.com/cloud/free/).
2. Crea una máquina virtual Ubuntu *Always Free*.
3. Conéctate por SSH, clona tu repositorio y lanza el monitor en segundo plano con `systemd` o `nohup`:
   ```bash
   nohup python3 flight_monitor.py --origin MAD --interval 30 > monitor.log 2>&1 &
   ```
4. Funcionará de forma ininterrumpida los 365 días del año.

---

## 🍓 Opción 4: En casa con Raspberry Pi
Si tienes una Raspberry Pi conectada a tu router:
- Consume menos de 3 vatios (apenas unos céntimos de electricidad al año).
- Solo tienes que clonar la carpeta y dejar corriendo:
  ```bash
  python3 flight_monitor.py --origin MAD --interval 30
  ```

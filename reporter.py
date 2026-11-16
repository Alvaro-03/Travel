import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def export_to_csv(flights: List[Dict[str, Any]], filename: str = "vuelos_baratos_2027.csv") -> str:
    """Exporta los vuelos a CSV con información de vuelos, alojamiento estimado y enlaces a múltiples buscadores."""
    filepath = Path(filename).resolve()
    keys = [
        "price", "currency", "destination", "dest_city", "dest_country", "continent", "duration_days",
        "deal_type", "price_diff",
        "hotel_price_per_night", "hotel_nights", "hotel_total_est", "hotel_tier", "hotel_note", "trip_total_est",
        "outbound_airline", "outbound_dep_time", "outbound_arr_time", "outbound_duration_str", "outbound_duration_hours",
        "return_airline", "return_dep_time", "return_arr_time", "return_duration_str", "return_duration_hours",
        "different_airlines", "origin", "origin_city", "departure_date", "return_date",
        "direct_link", "skyscanner_link", "kayak_link", "kiwi_link", "momondo_link",
        "outbound_airline_url", "return_airline_url",
        "booking_link", "airbnb_link", "google_hotels_link"
    ]
    
    with open(filepath, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for flight in flights:
            writer.writerow(flight)
            
    return str(filepath)


def export_to_html(
    flights: List[Dict[str, Any]],
    origin: str,
    duration_info: str = "5 a 9 días (~1 semana +/- 2 días)",
    last_update: str = None,
    refresh_seconds: int = 120,
    filename: str = "comparador_vuelos_2027.html"
) -> str:
    """Genera un reporte interactivo en HTML con actualización en tiempo real, múltiples buscadores y estimación de hotel."""
    filepath = Path(filename).resolve()
    flights_json = json.dumps(flights, ensure_ascii=False)
    timestamp_str = last_update or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Monitor de Vuelos en Tiempo Real 2027 - Salidas desde {origin}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #131c2e;
      --accent: #38bdf8;
      --accent-hover: #0284c7;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --price-tag: #22c55e;
      --hotel-color: #f59e0b;
      --total-color: #ec4899;
      --border: #22324d;
      --tag-diff: #a855f7;
      --deal-badge: #ef4444;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 20px;
    }}
    header {{
      max-width: 1350px;
      margin: 0 auto 20px;
      text-align: center;
      padding: 10px;
    }}
    .live-status-bar {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: rgba(34, 197, 94, 0.1);
      border: 1px solid rgba(34, 197, 94, 0.3);
      padding: 6px 18px;
      border-radius: 30px;
      margin-bottom: 14px;
      font-size: 0.85rem;
      font-weight: 600;
    }}
    .pulse-dot {{
      width: 10px;
      height: 10px;
      background-color: #22c55e;
      border-radius: 50%;
      box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7);
      animation: pulse 1.8s infinite;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }}
      70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }}
      100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }}
    }}
    header h1 {{
      font-size: 2.3rem;
      margin-bottom: 6px;
    }}
    header h1 span {{ color: var(--accent); }}
    header p {{
      color: var(--text-muted);
      font-size: 1.05rem;
    }}
    .header-info-row {{
      display: flex;
      justify-content: center;
      gap: 12px;
      margin-top: 10px;
      flex-wrap: wrap;
    }}
    .badge-info {{
      background: rgba(56, 189, 248, 0.12);
      color: var(--accent);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.82rem;
      font-weight: 600;
    }}
    .badge-refresh {{
      background: #1e293b;
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.82rem;
      font-weight: 600;
    }}
    .panel-controls {{
      max-width: 1350px;
      margin: 0 auto 25px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px;
    }}
    .panel-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .filter-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }}
    .filter-item {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .filter-item label {{
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .filter-item input, .filter-item select {{
      background: #090d16;
      border: 1px solid var(--border);
      color: white;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.9rem;
      outline: none;
    }}
    .filter-item input:focus, .filter-item select:focus {{
      border-color: var(--accent);
    }}
    .checkbox-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 20px;
      padding-top: 12px;
      border-top: 1px solid var(--border);
    }}
    .checkbox-label {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.9rem;
      cursor: pointer;
      font-weight: 500;
    }}
    .checkbox-label input {{
      width: 18px;
      height: 18px;
      accent-color: var(--tag-diff);
      cursor: pointer;
    }}
    .grid {{
      max-width: 1350px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 20px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .card:hover {{
      transform: translateY(-4px);
      border-color: var(--accent);
    }}
    .card.highlight-drop {{
      border-color: rgba(239, 68, 68, 0.6);
      box-shadow: 0 0 15px rgba(239, 68, 68, 0.15);
    }}
    .card.highlight-new {{
      border-color: rgba(56, 189, 248, 0.6);
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }}
    .dest-title {{
      font-size: 1.3rem;
      font-weight: 700;
    }}
    .dest-country {{
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .price-box {{
      text-align: right;
    }}
    .price-flight {{
      font-size: 1.45rem;
      font-weight: 800;
      color: var(--price-tag);
      background: rgba(34, 197, 94, 0.12);
      padding: 4px 10px;
      border-radius: 8px;
      display: inline-block;
    }}
    .price-label {{
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 2px;
    }}
    .badges {{
      display: flex;
      gap: 6px;
      margin-top: 8px;
      flex-wrap: wrap;
    }}
    .badge {{
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 600;
    }}
    .continent-badge {{
      background: #1e293b;
      color: var(--accent);
    }}
    .duration-badge {{
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
    }}
    .diff-badge {{
      background: rgba(168, 85, 247, 0.18);
      color: #c084fc;
    }}
    .alert-badge {{
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}
    
    /* Sección de Alojamiento Estimado */
    .hotel-section {{
      background: rgba(245, 158, 11, 0.08);
      border: 1px solid rgba(245, 158, 11, 0.25);
      border-radius: 10px;
      padding: 12px;
      margin: 12px 0;
    }}
    .hotel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
      color: var(--hotel-color);
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .hotel-breakdown {{
      display: flex;
      justify-content: space-between;
      font-size: 0.88rem;
      margin-bottom: 8px;
    }}
    .trip-total-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #090d16;
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 0.85rem;
      font-weight: 600;
    }}
    .trip-total-val {{
      color: var(--total-color);
      font-size: 1.1rem;
      font-weight: 800;
    }}
    .hotel-links {{
      display: flex;
      gap: 6px;
      margin-top: 8px;
    }}
    .hotel-btn {{
      flex: 1;
      text-align: center;
      background: #1e293b;
      color: #cbd5e1;
      text-decoration: none;
      font-size: 0.75rem;
      padding: 5px 8px;
      border-radius: 6px;
      font-weight: 600;
      transition: background 0.2s, color 0.2s;
    }}
    .hotel-btn:hover {{
      background: var(--hotel-color);
      color: #090d16;
    }}

    /* Tramos de Vuelo */
    .flight-leg {{
      background: #090d16;
      border-radius: 8px;
      padding: 10px 12px;
      margin: 6px 0;
      font-size: 0.85rem;
      border-left: 3px solid var(--accent);
    }}
    .flight-leg.return {{
      border-left-color: #a855f7;
    }}
    .leg-header {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
      color: var(--text-muted);
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 600;
    }}
    .leg-airline {{
      color: white;
      font-weight: 600;
    }}
    .airline-direct-link {{
      color: var(--accent);
      text-decoration: none;
      font-size: 0.75rem;
      margin-left: 6px;
      border-bottom: 1px dashed var(--accent);
    }}
    .airline-direct-link:hover {{
      color: white;
    }}
    .leg-times {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 500;
    }}
    .time-val {{
      font-size: 1.05rem;
      font-weight: 700;
      color: white;
    }}
    .leg-duration {{
      font-size: 0.8rem;
      color: var(--text-muted);
      background: #1e293b;
      padding: 2px 6px;
      border-radius: 4px;
    }}

    /* Comparar en Múltiples Buscadores */
    .multi-search {{
      margin-top: 14px;
    }}
    .multi-search-title {{
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .provider-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 6px;
    }}
    .provider-btn {{
      display: block;
      text-align: center;
      background: #1e293b;
      color: #94a3b8;
      text-decoration: none;
      padding: 6px 4px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      transition: background 0.2s, color 0.2s;
    }}
    .provider-btn.google:hover {{ background: #4285f4; color: white; }}
    .provider-btn.skyscanner:hover {{ background: #00a698; color: white; }}
    .provider-btn.kayak:hover {{ background: #ff690f; color: white; }}
    .provider-btn.kiwi:hover {{ background: #00a99d; color: white; }}
    .provider-btn.momondo:hover {{ background: #e01764; color: white; }}
  </style>
</head>
<body>

  <header>
    <div class="live-status-bar">
      <div class="pulse-dot"></div>
      <span>Monitor en Tiempo Real Activo</span>
      <span style="color:var(--text-muted); font-size:0.75rem;">| Actualizado: {timestamp_str}</span>
    </div>

    <h1>✈️ Monitor Mundial de Vuelos <span>2027</span></h1>
    <p>Rastreo continuo de ofertas con avisos al móvil y estimación hotelera desde <strong>{origin}</strong></p>
    
    <div class="header-info-row">
      <div class="badge-info">⏱️ Estancia: {duration_info}</div>
      <div class="badge-refresh">🔄 Auto-refresco en: <strong id="timerSec">{refresh_seconds}s</strong></div>
    </div>
  </header>

  <div class="panel-controls">
    <div class="panel-title">
      <span>⚙️ Filtros y Opciones de Comparación</span>
      <span id="counterText" style="color: var(--accent);">Mostrando {len(flights)} opciones</span>
    </div>

    <!-- Primera fila: Búsqueda, Continente, Días y Criterio de Orden -->
    <div class="filter-grid">
      <div class="filter-item">
        <label>Buscar destino o aerolínea</label>
        <input type="text" id="searchInput" placeholder="Ej: Roma, Tokio, Ryanair..." oninput="filterFlights()">
      </div>

      <div class="filter-item">
        <label>Continente</label>
        <select id="continentFilter" onchange="filterFlights()">
          <option value="ALL">Todos los continentes</option>
          <option value="Europa">Europa</option>
          <option value="Latinoamérica">Latinoamérica</option>
          <option value="Norteamérica">Norteamérica</option>
          <option value="Asia">Asia</option>
          <option value="Medio Oriente">Medio Oriente</option>
          <option value="África">África</option>
        </select>
      </div>

      <div class="filter-item">
        <label>Ordenar resultados por:</label>
        <select id="sortCriteria" onchange="filterFlights()">
          <option value="flight_price">Vuelo más barato (por defecto)</option>
          <option value="trip_total">Total viaje (Vuelo + Hotel estimado)</option>
          <option value="hotel_price">Alojamiento más asequible/noche</option>
        </select>
      </div>

      <div class="filter-item">
        <label>Presupuesto Vuelo Máx (€)</label>
        <input type="number" id="maxFlightPrice" placeholder="Sin límite" oninput="filterFlights()">
      </div>

      <div class="filter-item">
        <label>Presupuesto Total Máx (Vuelo+Hotel)</label>
        <input type="number" id="maxTripPrice" placeholder="Sin límite" oninput="filterFlights()">
      </div>
    </div>

    <!-- Segunda fila: Horarios y tope de horas -->
    <div class="filter-grid">
      <div class="filter-item">
        <label>⏱️ Horas Máx Vuelo IDA</label>
        <input type="number" step="0.5" id="maxHoursOutbound" placeholder="Ej: 4.5 (vacío = sin tope)" oninput="filterFlights()">
      </div>

      <div class="filter-item">
        <label>⏱️ Horas Máx Vuelo VUELTA</label>
        <input type="number" step="0.5" id="maxHoursReturn" placeholder="Ej: 5.0 (vacío = sin tope)" oninput="filterFlights()">
      </div>

      <div class="filter-item">
        <label>🌅 Franja Salida IDA</label>
        <select id="outDepWindow" onchange="filterFlights()">
          <option value="ALL">Cualquier hora de salida</option>
          <option value="morning">Mañana (06:00 - 12:00)</option>
          <option value="midday">Mediodía (12:00 - 16:00)</option>
          <option value="afternoon">Tarde (16:00 - 20:00)</option>
          <option value="night">Noche (20:00 - 24:00)</option>
        </select>
      </div>

      <div class="filter-item">
        <label>🌇 Franja Salida VUELTA</label>
        <select id="retDepWindow" onchange="filterFlights()">
          <option value="ALL">Cualquier hora de regreso</option>
          <option value="after_16">Regreso por la tarde (> 16:00)</option>
          <option value="after_18">Regreso por la noche (> 18:00)</option>
          <option value="morning">Regreso por la mañana (< 12:00)</option>
        </select>
      </div>
    </div>

    <!-- Tercera fila: Checkbox aerolíneas distintas y chollos -->
    <div class="checkbox-row">
      <label class="checkbox-label">
        <input type="checkbox" id="requireDiffAirlines" onchange="filterFlights()">
        <span>✨ <strong>Exigir compañías distintas</strong> en ida y vuelta (ej. Ida Ryanair, Vuelta Vueling)</span>
      </label>

      <label class="checkbox-label">
        <input type="checkbox" id="onlyDeals" onchange="filterFlights()">
        <span>🔥 <strong>Solo bajadas de precio / nuevos chollos</strong></span>
      </label>
    </div>
  </div>

  <div class="grid" id="flightGrid"></div>

  <script>
    let flights = {flights_json};

    function timeToMinutes(t) {{
      if (!t || !t.includes(':')) return -1;
      const [h, m] = t.split(':').map(Number);
      return h * 60 + m;
    }}

    function matchesTimeWindow(timeStr, windowKey) {{
      if (windowKey === 'ALL') return true;
      const mins = timeToMinutes(timeStr);
      if (mins < 0) return true;

      if (windowKey === 'morning') return mins >= 6 * 60 && mins < 12 * 60;
      if (windowKey === 'midday') return mins >= 12 * 60 && mins < 16 * 60;
      if (windowKey === 'afternoon') return mins >= 16 * 60 && mins < 20 * 60;
      if (windowKey === 'night') return mins >= 20 * 60;
      if (windowKey === 'after_16') return mins >= 16 * 60;
      if (windowKey === 'after_18') return mins >= 18 * 60;
      return true;
    }}

    function renderCards(list) {{
      const grid = document.getElementById('flightGrid');
      grid.innerHTML = '';
      
      list.forEach(f => {{
        const card = document.createElement('div');
        const isDrop = f.deal_type === 'price_drop';
        const isNew = f.deal_type === 'new_deal';
        card.className = 'card' + (isDrop ? ' highlight-drop' : (isNew ? ' highlight-new' : ''));
        
        let alertBadgeHtml = '';
        if (isDrop) {{
          alertBadgeHtml = `<span class="badge alert-badge">📉 ¡Bajó ${{f.price_diff}} €!</span>`;
        }} else if (isNew) {{
          alertBadgeHtml = `<span class="badge alert-badge">✨ ¡Nuevo Chollo!</span>`;
        }}

        card.innerHTML = `
          <div>
            <div class="card-top">
              <div>
                <div class="dest-title">${{f.dest_flag}} ${{f.dest_city}}</div>
                <div class="dest-country">${{f.dest_country}} [${{f.destination}}]</div>
                <div class="badges">
                  ${{alertBadgeHtml}}
                  <span class="badge continent-badge">${{f.continent}}</span>
                  <span class="badge duration-badge">⏱️ ${{f.duration_days}} días</span>
                  ${{f.different_airlines ? '<span class="badge diff-badge">🔀 Cías. Distintas</span>' : ''}}
                </div>
              </div>
              <div class="price-box">
                <div class="price-flight">${{f.price}} ${{f.currency}}</div>
                <div class="price-label">Vuelo I/V</div>
              </div>
            </div>

            <!-- Tramo Ida -->
            <div class="flight-leg">
              <div class="leg-header">
                <span>🛫 IDA • ${{f.departure_date}}</span>
                <div>
                  <span class="leg-airline">${{f.outbound_airline}}</span>
                  <a href="${{f.outbound_airline_url}}" target="_blank" rel="noopener" class="airline-direct-link" title="Web oficial de la aerolínea">Web Oficial ↗</a>
                </div>
              </div>
              <div class="leg-times">
                <div>
                  <span class="time-val">${{f.outbound_dep_time}}</span>
                  <span style="color:var(--text-muted); font-size:0.85rem;"> ➔ </span>
                  <span class="time-val">${{f.outbound_arr_time}}</span>
                </div>
                <span class="leg-duration">⌛ ${{f.outbound_duration_str}}</span>
              </div>
            </div>

            <!-- Tramo Vuelta -->
            <div class="flight-leg return">
              <div class="leg-header">
                <span>🛬 VUELTA • ${{f.return_date}}</span>
                <div>
                  <span class="leg-airline">${{f.return_airline}}</span>
                  <a href="${{f.return_airline_url}}" target="_blank" rel="noopener" class="airline-direct-link" title="Web oficial de la aerolínea">Web Oficial ↗</a>
                </div>
              </div>
              <div class="leg-times">
                <div>
                  <span class="time-val">${{f.return_dep_time}}</span>
                  <span style="color:var(--text-muted); font-size:0.85rem;"> ➔ </span>
                  <span class="time-val">${{f.return_arr_time}}</span>
                </div>
                <span class="leg-duration">⌛ ${{f.return_duration_str}}</span>
              </div>
            </div>

            <!-- Estimación de Alojamiento -->
            <div class="hotel-section">
              <div class="hotel-header">
                <span>🏨 Alojamiento Estimado (${{f.hotel_tier}})</span>
                <span>~${{f.hotel_price_per_night}} € / noche</span>
              </div>
              <div class="hotel-breakdown">
                <span style="color:var(--text-muted);">Estancia ${{f.hotel_nights}} noches:</span>
                <strong style="color:var(--hotel-color);">~${{f.hotel_total_est}} €</strong>
              </div>
              <div class="trip-total-bar">
                <span>Presupuesto Total (Vuelo + Hotel):</span>
                <span class="trip-total-val">~${{f.trip_total_est}} €</span>
              </div>
              <div class="hotel-links">
                <a href="${{f.booking_link}}" target="_blank" rel="noopener" class="hotel-btn">Booking.com ↗</a>
                <a href="${{f.airbnb_link}}" target="_blank" rel="noopener" class="hotel-btn">Airbnb ↗</a>
                <a href="${{f.google_hotels_link}}" target="_blank" rel="noopener" class="hotel-btn">Google Hotels ↗</a>
              </div>
            </div>
          </div>

          <!-- Múltiples Buscadores de Vuelos -->
          <div class="multi-search">
            <div class="multi-search-title">🔍 Comprobar y reservar vuelos en:</div>
            <div class="provider-grid">
              <a href="${{f.direct_link}}" target="_blank" rel="noopener" class="provider-btn google">Google</a>
              <a href="${{f.skyscanner_link}}" target="_blank" rel="noopener" class="provider-btn skyscanner">Skyscanner</a>
              <a href="${{f.kayak_link}}" target="_blank" rel="noopener" class="provider-btn kayak">Kayak</a>
              <a href="${{f.kiwi_link}}" target="_blank" rel="noopener" class="provider-btn kiwi">Kiwi</a>
              <a href="${{f.momondo_link}}" target="_blank" rel="noopener" class="provider-btn momondo">Momondo</a>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});

      document.getElementById('counterText').textContent = `Mostrando ${{list.length}} opciones`;
    }}

    function filterFlights() {{
      const search = document.getElementById('searchInput').value.toLowerCase().trim();
      const continent = document.getElementById('continentFilter').value;
      const sortBy = document.getElementById('sortCriteria').value;
      const maxFPrice = parseFloat(document.getElementById('maxFlightPrice').value);
      const maxTPrice = parseFloat(document.getElementById('maxTripPrice').value);
      const maxHOut = parseFloat(document.getElementById('maxHoursOutbound').value);
      const maxHRet = parseFloat(document.getElementById('maxHoursReturn').value);
      const outDepWindow = document.getElementById('outDepWindow').value;
      const retDepWindow = document.getElementById('retDepWindow').value;
      const reqDiff = document.getElementById('requireDiffAirlines').checked;
      const onlyDeals = document.getElementById('onlyDeals').checked;

      let filtered = flights.filter(f => {{
        if (onlyDeals && !f.deal_type) return false;

        if (search) {{
          const match = f.dest_city.toLowerCase().includes(search) || 
                        f.dest_country.toLowerCase().includes(search) ||
                        f.destination.toLowerCase().includes(search) ||
                        f.outbound_airline.toLowerCase().includes(search) ||
                        f.return_airline.toLowerCase().includes(search);
          if (!match) return false;
        }}

        if (continent !== 'ALL' && f.continent !== continent) return false;
        if (!isNaN(maxFPrice) && f.price > maxFPrice) return false;
        if (!isNaN(maxTPrice) && f.trip_total_est > maxTPrice) return false;
        if (!isNaN(maxHOut) && f.outbound_duration_hours > maxHOut) return false;
        if (!isNaN(maxHRet) && f.return_duration_hours > maxHRet) return false;
        if (!matchesTimeWindow(f.outbound_dep_time, outDepWindow)) return false;
        if (!matchesTimeWindow(f.return_dep_time, retDepWindow)) return false;
        if (reqDiff && !f.different_airlines) return false;

        return true;
      }});

      if (sortBy === 'trip_total') {{
        filtered.sort((a, b) => a.trip_total_est - b.trip_total_est);
      }} else if (sortBy === 'hotel_price') {{
        filtered.sort((a, b) => a.hotel_price_per_night - b.hotel_price_per_night);
      }} else {{
        filtered.sort((a, b) => a.price - b.price);
      }}

      renderCards(filtered);
    }}

    // Auto-recarga suave
    let remainingSec = {refresh_seconds};
    const timerElem = document.getElementById('timerSec');
    setInterval(() => {{
      remainingSec--;
      if (remainingSec <= 0) {{
        window.location.reload();
      }} else if (timerElem) {{
        timerElem.textContent = remainingSec + 's';
      }}
    }}, 1000);

    // Render inicial
    renderCards(flights);
  </script>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return str(filepath)

"""
Motor de filtrado avanzado de vuelos por:
- Duración máxima de vuelo en horas (ida y vuelta por separado)
- Franjas horarias de salida y llegada (ida y vuelta por separado)
- Compañías aéreas (permitir o exigir aerolíneas distintas entre ida y vuelta)
"""

from typing import List, Dict, Any, Optional


def time_to_minutes(time_str: str) -> Optional[int]:
    """Convierte 'HH:MM' a minutos desde la medianoche para comparaciones precisas."""
    if not time_str or ":" not in time_str:
        return None
    try:
        parts = time_str.strip().split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return None


def is_time_in_range(flight_time: str, min_time: Optional[str], max_time: Optional[str]) -> bool:
    """Verifica si una hora HH:MM entra dentro del rango min_time y max_time."""
    if not flight_time:
        return True
    
    t_min = time_to_minutes(min_time) if min_time else None
    t_max = time_to_minutes(max_time) if max_time else None
    t_val = time_to_minutes(flight_time)
    
    if t_val is None:
        return True

    if t_min is not None and t_val < t_min:
        return False
    if t_max is not None and t_val > t_max:
        return False

    return True


def matches_filters(flight: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    """
    Evalúa si un vuelo cumple con todos los filtros activos.
    Si un filtro no está especificado (None o vacío), se ignora automáticamente.
    """
    # 1. Tope de horas máximas para la ida
    max_h_ida = filters.get("max_hours_outbound")
    if max_h_ida is not None:
        flight_h_ida = flight.get("outbound_duration_hours", 0.0)
        if flight_h_ida > float(max_h_ida):
            return False

    # 2. Tope de horas máximas para la vuelta
    max_h_vuelta = filters.get("max_hours_return")
    if max_h_vuelta is not None:
        flight_h_vuelta = flight.get("return_duration_hours", 0.0)
        if flight_h_vuelta > float(max_h_vuelta):
            return False

    # 3. Franja horaria de salida de la ida
    if not is_time_in_range(
        flight.get("outbound_dep_time", ""),
        filters.get("outbound_dep_from"),
        filters.get("outbound_dep_to")
    ):
        return False

    # 4. Franja horaria de llegada de la ida
    if not is_time_in_range(
        flight.get("outbound_arr_time", ""),
        filters.get("outbound_arr_from"),
        filters.get("outbound_arr_to")
    ):
        return False

    # 5. Franja horaria de salida de la vuelta
    if not is_time_in_range(
        flight.get("return_dep_time", ""),
        filters.get("return_dep_from"),
        filters.get("return_dep_to")
    ):
        return False

    # 6. Franja horaria de llegada de la vuelta
    if not is_time_in_range(
        flight.get("return_arr_time", ""),
        filters.get("return_arr_from"),
        filters.get("return_arr_to")
    ):
        return False

    # 7. Regla de aerolíneas distintas (Ida ≠ Vuelta)
    if filters.get("require_different_airlines"):
        airline_ida = (flight.get("outbound_airline") or "").strip().lower()
        airline_vuelta = (flight.get("return_airline") or "").strip().lower()
        if airline_ida and airline_vuelta and airline_ida == airline_vuelta:
            return False

    return True


def apply_flight_filters(flights: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filtra una lista de vuelos según los filtros configurados."""
    if not filters:
        return flights
    return [f for f in flights if matches_filters(f, filters)]

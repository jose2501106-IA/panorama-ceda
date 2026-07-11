#!/usr/bin/env python3
"""
Pipeline diario de factores externos (clima) para el Panorama CEDA.

- Consulta Open-Meteo (gratis, sin llave) para las zonas productoras configuradas.
- Aplica reglas conservadoras (regla editorial: hecho + dirección, sin magnitudes inventadas).
- Escribe datos/factores_auto.json (lo lee el frontend) y agrega el registro a datos/ceda.db (SQLite).

Corre solo, todos los días, vía GitHub Actions (.github/workflows/datos.yml).
Para probarlo a mano: python3 scripts/actualiza_factores.py
"""
import json
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_JSON = RAIZ / "datos" / "factores_auto.json"
ARCHIVO_DB = RAIZ / "datos" / "ceda.db"

# Zonas productoras por producto. Ajustar/agregar con confianza:
# coordenadas aproximadas del centro de la zona de producción.
ZONAS = [
    {"producto": "Guayaba", "zona": "Calvillo, Aguascalientes", "lat": 21.85, "lon": -102.71},
    {"producto": "Jitomate saladette", "zona": "Culiacán, Sinaloa", "lat": 24.81, "lon": -107.39},
    {"producto": "Cebolla blanca", "zona": "Bajío (Salamanca, Gto.)", "lat": 20.57, "lon": -101.19},
    {"producto": "Papa alpha", "zona": "Valle de Toluca, Edomex", "lat": 19.29, "lon": -99.65},
]

# Umbrales conservadores (72 horas hacia adelante)
UMBRAL_HELADA_C = 2.0      # tmin <= 2°C: riesgo de helada
UMBRAL_LLUVIA_MM = 50.0    # lluvia acumulada >= 50 mm: riesgo en corte/transporte
UMBRAL_CALOR_C = 38.0      # tmax >= 38°C: estrés de cultivo


def consulta_open_meteo(lat, lon):
    """Pronóstico diario a 3 días. Devuelve dict de Open-Meteo."""
    import requests
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_min,temperature_2m_max,precipitation_sum"
        "&forecast_days=3&timezone=America%2FMexico_City"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def analiza(diario):
    """Aplica reglas sobre el bloque 'daily' de Open-Meteo. Devuelve (señal, dirección, detalle) o None."""
    tmins = diario.get("temperature_2m_min") or []
    tmaxs = diario.get("temperature_2m_max") or []
    lluvias = diario.get("precipitation_sum") or []
    tmin = min([t for t in tmins if t is not None], default=None)
    tmax = max([t for t in tmaxs if t is not None], default=None)
    lluvia = sum([p for p in lluvias if p is not None])

    if tmin is not None and tmin <= UMBRAL_HELADA_C:
        return ("helada", "alza", f"pronóstico de mínima de {tmin:.0f}°C en las próximas 72 h", tmin, tmax, lluvia)
    if lluvia >= UMBRAL_LLUVIA_MM:
        return ("lluvia fuerte", "incierto", f"lluvia acumulada de {lluvia:.0f} mm prevista en 72 h", tmin, tmax, lluvia)
    if tmax is not None and tmax >= UMBRAL_CALOR_C:
        return ("calor extremo", "incierto", f"máxima de {tmax:.0f}°C prevista en 72 h", tmin, tmax, lluvia)
    return (None, None, None, tmin, tmax, lluvia)


def guarda_sqlite(filas):
    con = sqlite3.connect(ARCHIVO_DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS clima_diario (
            consultado TEXT NOT NULL,
            producto TEXT NOT NULL,
            zona TEXT NOT NULL,
            tmin_72h REAL, tmax_72h REAL, lluvia_72h_mm REAL,
            senal TEXT, direccion TEXT
        )""")
    con.executemany(
        "INSERT INTO clima_diario VALUES (?,?,?,?,?,?,?,?)", filas)
    con.commit()
    con.close()


def main():
    ahora = datetime.now(timezone(timedelta(hours=-6))).strftime("%Y-%m-%d %H:%M")
    factores, filas = [], []

    for z in ZONAS:
        try:
            datos = consulta_open_meteo(z["lat"], z["lon"])
        except Exception as e:
            print(f"AVISO: fallo consultando {z['zona']}: {e}", file=sys.stderr)
            continue
        senal, direccion, detalle, tmin, tmax, lluvia = analiza(datos.get("daily", {}))
        filas.append((ahora, z["producto"], z["zona"], tmin, tmax, lluvia, senal, direccion))
        if senal:
            factores.append({
                "tipo": "clima",
                "descripcion": f"{senal.capitalize()} en {z['zona']}: {detalle} (Open-Meteo)",
                "productos": [z["producto"]],
                "direccion": direccion,
            })

    ARCHIVO_JSON.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_JSON.write_text(json.dumps({
        "generado": ahora,
        "fuente": "Open-Meteo (open-meteo.com), datos CC BY 4.0",
        "factores": factores,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if filas:
        guarda_sqlite(filas)
    print(f"OK: {len(factores)} factor(es) con señal, {len(filas)} zona(s) registradas en SQLite.")


if __name__ == "__main__":
    main()

"""
Seed script for the Sistema de Renta de Discos.

Run this AFTER your backend is up (docker compose up --build), so it can
POST data through the real API — this exercises schemas, services, and
repositories exactly like Angular will, instead of writing to Mongo
directly and skipping your business logic.

Usage:
    pip install requests
    python seed_data.py
"""

import requests

BASE_URL = "http://localhost:8000"

discos = [
    {"titulo": "Abbey Road", "artista": "The Beatles", "genero": "Rock", "anio_lanzamiento": 1969, "stock_total": 3},
    {"titulo": "Thriller", "artista": "Michael Jackson", "genero": "Pop", "anio_lanzamiento": 1982, "stock_total": 5},
    {"titulo": "Rumours", "artista": "Fleetwood Mac", "genero": "Rock", "anio_lanzamiento": 1977, "stock_total": 2},
    {"titulo": "Back to Black", "artista": "Amy Winehouse", "genero": "Soul", "anio_lanzamiento": 2006, "stock_total": 4},
    {"titulo": "Random Access Memories", "artista": "Daft Punk", "genero": "Electronic", "anio_lanzamiento": 2013, "stock_total": 1},
]

clientes = [
    {"nombre": "Ana Torres", "email": "ana.torres@example.com", "telefono": "3001234567"},
    {"nombre": "Carlos Ruiz", "email": "carlos.ruiz@example.com", "telefono": "3007654321"},
    {"nombre": "Beatriz Gomez", "email": "beatriz.gomez@example.com", "telefono": "3009998888"},
]


def unwrap(resp_json: dict) -> dict:
    """Pulls id + attributes out of a JSON:API single-resource response."""
    data = resp_json["data"]
    return {"id": data["id"], **data["attributes"]}


def unwrap_error(resp) -> str:
    try:
        return resp.json()["errors"][0]["detail"]
    except Exception:
        return resp.text


def seed():
    disco_ids = []
    print("Creando discos...")
    for d in discos:
        resp = requests.post(f"{BASE_URL}/discos/", json=d)
        if resp.status_code == 201:
            created = unwrap(resp.json())
            disco_ids.append(created["id"])
            print(f"  OK: {d['titulo']} -> id {created['id']}")
        else:
            print(f"  FALLO ({resp.status_code}) para {d['titulo']}: {unwrap_error(resp)}")

    cliente_ids = []
    print("\nCreando clientes...")
    for c in clientes:
        resp = requests.post(f"{BASE_URL}/clientes/", json=c)
        if resp.status_code == 201:
            created = unwrap(resp.json())
            cliente_ids.append(created["id"])
            print(f"  OK: {c['nombre']} -> id {created['id']} (estado: {created['estado']})")
        else:
            print(f"  FALLO ({resp.status_code}) para {c['nombre']}: {unwrap_error(resp)}")

    if len(cliente_ids) >= 3:
        print("\nDesactivando a Beatriz Gomez para probar la ruta de cliente inactivo...")
        resp = requests.patch(f"{BASE_URL}/clientes/{cliente_ids[2]}/desactivar")
        if resp.status_code == 200:
            print(f"  OK: {unwrap(resp.json())}")
        else:
            print(f"  FALLO ({resp.status_code}): {unwrap_error(resp)}")

    if disco_ids and cliente_ids:
        print("\nCreando una renta de ejemplo (cliente activo, disco con stock)...")
        resp = requests.post(f"{BASE_URL}/rentas/", json={"cliente_id": cliente_ids[0], "disco_id": disco_ids[0]})
        if resp.status_code == 201:
            print(f"  OK: renta creada -> {unwrap(resp.json())}")
        else:
            print(f"  FALLO ({resp.status_code}): {unwrap_error(resp)}")

        print("\nIntentando una renta con el cliente inactivo (debe fallar con 403)...")
        resp = requests.post(f"{BASE_URL}/rentas/", json={"cliente_id": cliente_ids[2], "disco_id": disco_ids[1]})
        print(f"  Status {resp.status_code}: {unwrap_error(resp) if resp.status_code >= 400 else unwrap(resp.json())}")

    print("\nListo. Revisa http://localhost:8000/docs -> GET /discos/ y GET /clientes/ para confirmar.")


if __name__ == "__main__":
    seed()
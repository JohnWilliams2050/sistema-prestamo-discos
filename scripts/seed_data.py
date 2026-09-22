"""
Seed script for the Music Disc Loan System.

Run this AFTER your backend is up (uvicorn or docker compose), so it can
POST data through the real API — this exercises schemas, services, and
repositories exactly like the frontend will, instead of writing to Mongo
directly and skipping your business logic.

Usage:
    pip install requests
    python seed_data.py
"""

import requests

BASE_URL = "http://localhost:8000"

discs = [
    {"title": "Abbey Road", "artist": "The Beatles", "genre": "Rock", "format": "Vinyl", "total_copies": 3},
    {"title": "Thriller", "artist": "Michael Jackson", "genre": "Pop", "format": "CD", "total_copies": 5},
    {"title": "Rumours", "artist": "Fleetwood Mac", "genre": "Rock", "format": "Vinyl", "total_copies": 2},
    {"title": "Back to Black", "artist": "Amy Winehouse", "genre": "Soul", "format": "CD", "total_copies": 4},
    {"title": "Random Access Memories", "artist": "Daft Punk", "genre": "Electronic", "format": "CD", "total_copies": 1},
]

# NOTE: adjust these field names if your Member schema differs from this guess
# (name, email, active) — check your app/schemas/member.py to confirm.
members = [
    {"name": "Ana Torres", "email": "ana.torres@example.com", "active": True},
    {"name": "Carlos Ruiz", "email": "carlos.ruiz@example.com", "active": True},
    {"name": "Beatriz Gomez", "email": "beatriz.gomez@example.com", "active": False},
]


def seed():
    disc_ids = []
    print("Creating discs...")
    for d in discs:
        resp = requests.post(f"{BASE_URL}/discs", json=d)
        if resp.status_code == 201:
            created = resp.json()
            disc_ids.append(created["id"])
            print(f"  OK: {d['title']} -> id {created['id']}")
        else:
            print(f"  FAILED ({resp.status_code}) for {d['title']}: {resp.text}")

    member_ids = []
    print("\nCreating members...")
    for m in members:
        resp = requests.post(f"{BASE_URL}/members", json=m)
        if resp.status_code == 201:
            created = resp.json()
            member_ids.append(created["id"])
            print(f"  OK: {m['name']} -> id {created['id']}")
        else:
            print(f"  FAILED ({resp.status_code}) for {m['name']}: {resp.text}")
    if len(member_ids) >= 3:
        print("\nDeactivating Beatriz Gomez to test the inactive-member path...")
        resp = requests.patch(f"{BASE_URL}/members/{member_ids[2]}/deactivate")
        print(f"  Status {resp.status_code}: {resp.json()}")
    if disc_ids and member_ids:
        print("\nCreating a sample loan (first active member borrows first disc)...")
        loan_payload = {"disc_id": disc_ids[0], "member_id": member_ids[0]}
        resp = requests.post(f"{BASE_URL}/loans", json=loan_payload)
        if resp.status_code == 201:
            print(f"  OK: loan created -> {resp.json()}")
        else:
            print(f"  FAILED ({resp.status_code}): {resp.text}")

        print("\nTrying a loan for the inactive member (should fail with 403/409)...")
        bad_payload = {"disc_id": disc_ids[1], "member_id": member_ids[2]}
        resp = requests.post(f"{BASE_URL}/loans", json=bad_payload)
        print(f"  Got status {resp.status_code}: {resp.text}")

    print("\nDone. Check http://localhost:8000/docs -> GET /discs and GET /members to confirm.")


if __name__ == "__main__":
    seed()

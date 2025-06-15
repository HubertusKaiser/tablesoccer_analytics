import sqlite3
from config import DB_DATEI, TABELLE

def init_db():
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABELLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_a_spieler1 TEXT,
            team_a_spieler2 TEXT,
            team_b_spieler1 TEXT,
            team_b_spieler2 TEXT,
            tore_team_a INTEGER,
            tore_team_b INTEGER,
            gewinner TEXT,
            datum TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_last_matches(limit=10):
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    c.execute(f"""
        SELECT datum, team_a_spieler1, team_a_spieler2,
               tore_team_a, tore_team_b, team_b_spieler1,
               team_b_spieler2, gewinner
        FROM {TABELLE}
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    daten = c.fetchall()
    conn.close()
    return daten

def insert_match(a1, a2, b1, b2, ta, tb, gewinner, datum):
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    c.execute(f"""
        INSERT INTO {TABELLE}
        (team_a_spieler1, team_a_spieler2,
         team_b_spieler1, team_b_spieler2,
         tore_team_a, tore_team_b, gewinner, datum)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (a1, a2, b1, b2, ta, tb, gewinner, datum))
    conn.commit()
    conn.close()

def get_player_frequencies():
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    counts = {}
    for spalte in ["team_a_spieler1", "team_a_spieler2", "team_b_spieler1", "team_b_spieler2"]:
        c.execute(f"SELECT {spalte} FROM {TABELLE}")
        for (name,) in c.fetchall():
            if name:
                counts[name] = counts.get(name, 0) + 1
    conn.close()
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)

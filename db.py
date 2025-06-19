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

def get_last_match():
    conn = sqlite3.connect(DB_DATEI)  
    c = conn.cursor()
    c.execute(f"""
        SELECT team_a_spieler1,
               team_a_spieler2, 
               team_b_spieler1, 
               team_b_spieler2, 
               tore_team_a,
               tore_team_b, 
               datum 
        FROM {TABELLE} ORDER BY rowid DESC LIMIT 1
    """)
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'team_a1': row[0], 'team_a2': row[1],
            'team_b1': row[2], 'team_b2': row[3],
            'tore_a': row[4], 'tore_b': row[5],
            'datum': row[6]
        }
    return None

def delete_last_match():
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    c.execute(f"""DELETE FROM {TABELLE} WHERE rowid = (SELECT MAX(rowid) FROM {TABELLE})""")
    conn.commit()
    conn.close()

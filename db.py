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


def get_all_players():
    """Get all unique players from the database"""
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    
    # Get all player names from all columns where players can appear
    c.execute(f"""
        SELECT DISTINCT team_a_spieler1, team_a_spieler2, team_b_spieler1, team_b_spieler2 
        FROM {TABELLE}
    """)
    
    # Get all unique player names
    players = set()
    for row in c.fetchall():
        for player in row:
            if player:
                players.add(player)
    
    conn.close()
    return sorted(players)  # Return sorted list of players


def delete_player_games(player):
    """Delete all games where the specified player appears"""
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    
    # Delete games where player appears in any of the player columns
    c.execute(f"""
        DELETE FROM {TABELLE}
        WHERE team_a_spieler1 = ? OR team_a_spieler2 = ? 
           OR team_b_spieler1 = ? OR team_b_spieler2 = ?
    """, (player, player, player, player))
    
    conn.commit()
    conn.close()


def rename_player(old_name, new_name):
    """Rename all occurrences of a player's name in the database"""
    if not old_name or not new_name:
        raise ValueError("Both old and new names must be provided")
    
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    
    # Update all occurrences of the old name to the new name
    c.execute(f"""
        UPDATE {TABELLE}
        SET team_a_spieler1 = CASE WHEN team_a_spieler1 = ? THEN ? ELSE team_a_spieler1 END,
            team_a_spieler2 = CASE WHEN team_a_spieler2 = ? THEN ? ELSE team_a_spieler2 END,
            team_b_spieler1 = CASE WHEN team_b_spieler1 = ? THEN ? ELSE team_b_spieler1 END,
            team_b_spieler2 = CASE WHEN team_b_spieler2 = ? THEN ? ELSE team_b_spieler2 END
        WHERE team_a_spieler1 = ? OR team_a_spieler2 = ? 
           OR team_b_spieler1 = ? OR team_b_spieler2 = ?
    """, (
        old_name, new_name,
        old_name, new_name,
        old_name, new_name,
        old_name, new_name,
        old_name, old_name,
        old_name, old_name
    ))
    
    conn.commit()
    conn.close()

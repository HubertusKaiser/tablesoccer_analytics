import sqlite3
from config import DB_DATEI, TABELLE
from contextlib import contextmanager

@contextmanager
def db_connection():
    """Context manager for database connection"""
    conn = sqlite3.connect(DB_DATEI)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with db_connection() as conn:
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

def fetch_last_matches(limit=10):
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(f"""
            SELECT datum, team_a_spieler1, team_a_spieler2,
                   tore_team_a, tore_team_b, team_b_spieler1,
                   team_b_spieler2, gewinner
            FROM {TABELLE}
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return c.fetchall()

def insert_match(a1, a2, b1, b2, ta, tb, gewinner, datum):
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(f"""
            INSERT INTO {TABELLE}
            (team_a_spieler1, team_a_spieler2,
             team_b_spieler1, team_b_spieler2,
             tore_team_a, tore_team_b, gewinner, datum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (a1, a2, b1, b2, ta, tb, gewinner, datum))
        conn.commit()

def get_player_frequencies():
    """Returns a sorted list of (player, frequency) tuples."""
    with db_connection() as conn:
        c = conn.cursor()
        counts = {}
        for spalte in ["team_a_spieler1", "team_a_spieler2", "team_b_spieler1", "team_b_spieler2"]:
            c.execute(f"SELECT {spalte} FROM {TABELLE}")
            for (name,) in c.fetchall():
                if name:
                    counts[name] = counts.get(name, 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)

def get_last_match():
    with db_connection() as conn:
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
        if row:
            return {
                'team_a1': row[0], 'team_a2': row[1],
                'team_b1': row[2], 'team_b2': row[3],
                'tore_a': row[4], 'tore_b': row[5],
                'datum': row[6]
            }
        return None

def delete_last_match():
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(f"""DELETE FROM {TABELLE} WHERE rowid = (SELECT MAX(rowid) FROM {TABELLE})""")
        conn.commit()

def get_all_players():
    """Get all unique players from the database"""
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(f"""
            SELECT DISTINCT team_a_spieler1, team_a_spieler2, team_b_spieler1, team_b_spieler2 
            FROM {TABELLE}
        """)
        players = set()
        for row in c.fetchall():
            for player in row:
                if player:
                    players.add(player)
        return sorted(players)

def delete_player_games(player):
    """Delete all games where the specified player appears"""
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(f"""
            DELETE FROM {TABELLE}
            WHERE team_a_spieler1 = ? OR team_a_spieler2 = ? 
               OR team_b_spieler1 = ? OR team_b_spieler2 = ?
        """, (player, player, player, player))
        conn.commit()

def rename_player(old_name, new_name):
    """Rename all occurrences of a player's name in the database"""
    if not old_name or not new_name:
        raise ValueError("Both old and new names must be provided")
    with db_connection() as conn:
        c = conn.cursor()
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

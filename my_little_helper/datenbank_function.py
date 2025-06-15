# -----------------------------------
# 🛠️ DATENBANK-FUNKTIONEN
# -----------------------------------
# Diese Datei enthält Funktionen zur Interaktion mit der SQLite-Datenbank.
import sqlite3
from datetime import datetime
from parameter import *

def init_db():
    conn = sqlite3.connect()
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABELLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_a_spieler1 {FELD_TYP_TEXT},
            team_a_spieler2 {FELD_TYP_TEXT},
            team_b_spieler1 {FELD_TYP_TEXT},
            team_b_spieler2 {FELD_TYP_TEXT},
            tore_team_a {FELD_TYP_INT},
            tore_team_b {FELD_TYP_INT},
            gewinner {FELD_TYP_TEXT},
            datum {FELD_TYP_TEXT}
        )
    """)
    conn.commit()
    conn.close()



def get_spieler_liste():
    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    c.execute(f"""
        SELECT team_a_spieler1, team_a_spieler2, team_b_spieler1, team_b_spieler2 FROM {TABELLE}
    """)
    rows = c.fetchall()
    conn.close()

    # Alle Namen in eine Liste sammeln
    namen = []
    for row in rows:
        for name in row:
            if name:
                namen.append(name.strip())

    # Zähle Vorkommen
    zähler = Counter(namen)
    # Sortiert nach Häufigkeit (absteigend), dann alphabetisch (optional)
    sortierte_namen = [name for name, _ in zähler.most_common()]
    return sortierte_namen




# -----------------------------------
# 💾 SPIEL SPEICHERN
# -----------------------------------

def spiel_speichern():
    a1 = entry_team_a_1.get().strip()
    a2 = entry_team_a_2.get().strip()
    b1 = entry_team_b_1.get().strip()
    b2 = entry_team_b_2.get().strip()
    tore_a = tore_team_a.get()
    tore_b = tore_team_b.get()

    if not all([a1, a2, b1, b2]):
        messagebox.showwarning(TXT_ERROR, TXT_FEHLENDE_NAMEN)
        return

    # Duplikatprüfung
    spieler = [a1, a2, b1, b2]
    if len(set(spieler)) < 4:
        messagebox.showwarning(TXT_ERROR, "Ein Spieler wurde mehrfach eingetragen.")
        return

    if tore_a == tore_b:
        messagebox.showwarning(TXT_ERROR, TXT_UNENTSCHIEDEN)
        return

    gewinner = "Team A" if tore_a > tore_b else "Team B"
    datum = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(DB_DATEI)
    c = conn.cursor()
    c.execute(f"""
        INSERT INTO {TABELLE} 
        (team_a_spieler1, team_a_spieler2, team_b_spieler1, team_b_spieler2,
         tore_team_a, tore_team_b, gewinner, datum)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (a1, a2, b1, b2, tore_a, tore_b, gewinner, datum))
    conn.commit()
    conn.close()

    letzter_text = f"{a1} & {a2} gewannen {tore_a}:{tore_b} gegen {b1} & {b2}" if gewinner == "Team A" \
                   else f"{b1} & {b2} gewannen {tore_b}:{tore_a} gegen {a1} & {a2}"

    root.destroy()
    erstelle_fenster(letzter_text)

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from collections import Counter
# -----------------------------------
# 🔧 KONFIGURATION & TEXTE
# -----------------------------------

DB_DATEI = "kicker.db"
TABELLE = "spiele"

TXT_TITEL = "Kicker Ergebnis Eintragen"
TXT_LABEL_A1 = "Team A Spieler 1"
TXT_LABEL_A2 = "Team A Spieler 2"
TXT_LABEL_B1 = "Team B Spieler 1"
TXT_LABEL_B2 = "Team B Spieler 2"
TXT_TORE_A = "Tore Team A (0–10)"
TXT_TORE_B = "Tore Team B (0–10)"
TXT_SPEICHERN = "Spiel speichern"
TXT_SAVED = "Spiel wurde erfolgreich gespeichert."
TXT_ERROR = "Fehler"
TXT_UNENTSCHIEDEN = "Unentschieden ist nicht erlaubt."
TXT_FEHLENDE_NAMEN = "Alle Spielernamen müssen ausgefüllt sein."

# -----------------------------------
# 🛠️ DATENBANK-FUNKTIONEN
# -----------------------------------

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

# -----------------------------------
# 🖼️ GUI SETUP
 
def erstelle_fenster(text_oben=None):
    global root, entry_team_a_1, entry_team_a_2, entry_team_b_1, entry_team_b_2
    global tore_team_a, tore_team_b

    init_db()
    spieler_namen = get_spieler_liste()

    root = tk.Tk()
    root.title(TXT_TITEL)
    root.geometry("400x450")
    root.grid_columnconfigure(0, weight=1)
    for i in range(14):
        root.grid_rowconfigure(i, weight=1)

    row_idx = 0
    if text_oben:
        label_result = tk.Label(root, text="Letztes Spiel: " + text_oben, fg="gray", font=("Arial", 9))
        label_result.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        row_idx += 1

    def make_cb(row):
        cb = ttk.Combobox(root, values=spieler_namen)
        cb.grid(row=row, column=0, sticky="ew", padx=10, pady=2)
        cb.set("")
        return cb

    tk.Label(root, text=TXT_LABEL_A1).grid(row=row_idx, column=0, sticky="w", padx=10)
    entry_team_a_1 = make_cb(row_idx+1)

    tk.Label(root, text=TXT_LABEL_A2).grid(row=row_idx+2, column=0, sticky="w", padx=10)
    entry_team_a_2 = make_cb(row_idx+3)

    tk.Label(root, text=TXT_LABEL_B1).grid(row=row_idx+4, column=0, sticky="w", padx=10)
    entry_team_b_1 = make_cb(row_idx+5)

    tk.Label(root, text=TXT_LABEL_B2).grid(row=row_idx+6, column=0, sticky="w", padx=10)
    entry_team_b_2 = make_cb(row_idx+7)

    tk.Label(root, text=TXT_TORE_A).grid(row=row_idx+8, column=0, sticky="w", padx=10)
    tore_team_a = tk.IntVar(value=0)
    tk.Spinbox(root, from_=0, to=10, textvariable=tore_team_a).grid(row=row_idx+9, column=0, sticky="ew", padx=10)

    tk.Label(root, text=TXT_TORE_B).grid(row=row_idx+10, column=0, sticky="w", padx=10)
    tore_team_b = tk.IntVar(value=0)
    tk.Spinbox(root, from_=0, to=10, textvariable=tore_team_b).grid(row=row_idx+11, column=0, sticky="ew", padx=10)

    btn = tk.Button(root, text=TXT_SPEICHERN, command=spiel_speichern)
    btn.grid(row=row_idx+12, column=0, sticky="nsew", padx=10, pady=10)
    root.grid_rowconfigure(row_idx+12, weight=2)

    root.mainloop()


if __name__ == "__main__":
    erstelle_fenster()
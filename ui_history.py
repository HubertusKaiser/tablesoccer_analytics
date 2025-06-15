import tkinter as tk
from db import fetch_last_matches

def zeige_letzte_spiele(root):
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()

    daten = fetch_last_matches()

    tk.Label(root, text="Letzte 10 Spiele:", font=("Arial", 14, "bold")).pack(pady=10)
    for eintrag in daten:
        datum, a1, a2, ta, tb, b1, b2, gewinner = eintrag
        if gewinner == "Team A":
            text = f"{datum}: {a1} & {a2} gewannen {ta}:{tb} gegen {b1} & {b2}"
        else:
            text = f"{datum}: {b1} & {b2} gewannen {tb}:{ta} gegen {a1} & {a2}"
        tk.Label(root, text=text, anchor="w", justify="left", wraplength=400).pack(padx=10, pady=2, anchor="w")

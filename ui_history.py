import tkinter as tk
from tkinter import simpledialog, messagebox
from db import fetch_last_matches, delete_last_match, get_last_match

def zeige_letzte_spiele(root):
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()

    daten = fetch_last_matches()

    def loesche_letztes_spiel():
        match = get_last_match()
        if match:
            msg = (
                f"Letztes Spiel:\n"
                f"{match['team_a1']} & {match['team_a2']} ({match['tore_a']}) "
                f"vs {match['team_b1']} & {match['team_b2']} ({match['tore_b']})\n"
                f"Datum: {match['datum']}\n\nWirklich löschen?"
            )
            if messagebox.askyesno("Letztes Spiel löschen", msg):
                delete_last_match()
                messagebox.showinfo("Gelöscht", "Letztes Spiel wurde gelöscht.")
        else:
            messagebox.showinfo("Keine Spiele", "Es ist kein Spiel zum Löschen vorhanden.")


    tk.Label(root, text="Letzte 10 Spiele:", font=("Arial", 14, "bold")).pack(pady=10)
    for eintrag in daten:
        datum, a1, a2, ta, tb, b1, b2, gewinner = eintrag
        if gewinner == "Team A":
            text = f"{datum}:   {a1} & {a2}  {ta}:{tb}  {b1} & {b2}"
        else:
            text = f"{datum}:   {b1} & {b2}  {tb}:{ta}  {a1} & {a2}"
        tk.Label(root, text=text, anchor="w", justify="left", wraplength=800, font=("Arial", 14)).pack(padx=10, pady=2, anchor="w")

    tk.Button(root, text="Letztes Spiel löschen", command=loesche_letztes_spiel, bg="red", fg="white").pack(fill="x", padx=10, pady=10)


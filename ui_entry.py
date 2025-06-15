import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from db import get_player_frequencies, insert_match

def zeige_eingabe_fenster(root):
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()

    selected_players = []
    spieler_buttons = {}

    def aktualisiere_button_farben():
        for name, btn in spieler_buttons.items():
            if name in selected_players:
                index = selected_players.index(name)
                btn.config(bg="lightgreen" if index < 2 else "lightblue")
            else:
                btn.config(bg="SystemButtonFace")

    def toggle_player(name):
        if name in selected_players:
            selected_players.remove(name)
        elif len(selected_players) < 4:
            selected_players.append(name)
        else:
            messagebox.showinfo("Maximal 4 Spieler", "Du kannst nur 4 Spieler auswählen.")
        aktualisiere_button_farben()

    def neuer_spieler_popup():
        name = simpledialog.askstring("Neuer Spieler", "Name des neuen Spielers:")
        if name:
            name = name.strip()
            if name and name not in [n for (n, _) in spieler_liste]:
                spieler_liste.append((name, 0))
                build_buttons()

    def build_buttons():
        for widget in spieler_frame.winfo_children():
            widget.destroy()
        spieler_buttons.clear()
        for name, _ in spieler_liste:
            b = tk.Button(spieler_frame, text=name, anchor="w", command=lambda n=name: toggle_player(n))
            b.pack(fill="x", padx=5, pady=2)
            spieler_buttons[name] = b
        aktualisiere_button_farben()

    def versuche_speichern():
        if len(selected_players) != 4:
            messagebox.showerror("Fehler", "Bitte genau 4 Spieler auswählen.")
            return

        a1, a2, b1, b2 = selected_players
        ta = tore_team_a.get()
        tb = tore_team_b.get()

        if ta == tb:
            messagebox.showerror("Fehler", "Unentschieden ist nicht erlaubt.")
            return

        gewinner = "Team A" if ta > tb else "Team B"
        datum = datetime.now().strftime("%Y-%m-%d %H:%M")

        insert_match(a1, a2, b1, b2, ta, tb, gewinner, datum)

        messagebox.showinfo("Erfolg", "Spiel gespeichert!")
        selected_players.clear()
        aktualisiere_button_farben()

    spieler_liste = get_player_frequencies()

    spieler_frame = tk.Frame(root)
    spieler_frame.pack(fill="both", expand=True, padx=10, pady=5)
    build_buttons()

    tk.Button(root, text="Neuen Spieler hinzufügen", command=neuer_spieler_popup).pack(pady=5)

    tore_team_a = tk.IntVar(value=0)
    tore_team_b = tk.IntVar(value=0)

    tore_frame = tk.Frame(root)
    tore_frame.pack(pady=10)

    tk.Label(tore_frame, text="Tore Team A").grid(row=0, column=0)
    tk.Spinbox(tore_frame, from_=0, to=10, textvariable=tore_team_a, width=5).grid(row=0, column=1, padx=5)

    tk.Label(tore_frame, text="Tore Team B").grid(row=1, column=0)
    tk.Spinbox(tore_frame, from_=0, to=10, textvariable=tore_team_b, width=5).grid(row=1, column=1, padx=5)

    tk.Button(root, text="Spiel speichern", command=versuche_speichern, height=2).pack(fill="x", padx=10, pady=10)

import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from db import get_player_frequencies, insert_match

def zeige_eingabe_fenster_numpad(root):
    # Alle Widgets außer Menü löschen
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()

    selected_players = []
    spieler_buttons = {}

    def aktualisiere_button_farben():
        for name, btn in spieler_buttons.items():
            if name in selected_players:
                idx = selected_players.index(name)
                btn.config(bg="lightgreen" if idx < 2 else "lightblue")
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
        # Buttons neu anordnen in 3 Spalten mit festem Zellenraster
        for w in spieler_frame.winfo_children():
            w.destroy()
        spieler_buttons.clear()
        num_buttons = len(spieler_liste)
        num_rows = (num_buttons + 2) // 3
        for idx, (name, _) in enumerate(spieler_liste):
            row = idx // 3
            col = idx % 3
            b = tk.Button(
                spieler_frame,
                text=name,
                anchor="w",
                command=lambda n=name: toggle_player(n),
                font=("Arial", 14)
            )
            # Einheitliche Button-Größe per cellconfigure, Schrift unabhängig
            b.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            spieler_buttons[name] = b

        # Spalten und Zeilen flexibel machen, alle Zellen gleich groß
        for c in range(3):
            spieler_frame.columnconfigure(c, weight=1, uniform="players")
        for r in range(num_rows):
            spieler_frame.rowconfigure(r, weight=1, uniform="players")

        aktualisiere_button_farben()

    class Numpad(tk.Frame):
        def __init__(self, master, tore_team_a_var, tore_team_b_var, **kwargs):
            super().__init__(master, **kwargs)
            self.tore_team_a = tore_team_a_var
            self.tore_team_b = tore_team_b_var
            self.active_team = 'A'
            self.build_ui()

        def build_ui(self):
            for i in range(3):
                self.columnconfigure(i, weight=1)
            for j in range(6):
                self.rowconfigure(j, weight=1)

            self.label = tk.Label(self, text="Aktiv: Team A", font=("Arial", 12, "bold"))
            self.label.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")

            self.switch_button = tk.Button(self, text="⇆ Team wechseln", command=self.toggle_team)
            self.switch_button.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

            buttons = [
                ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2),
                ('7', 4, 0), ('8', 4, 1), ('9', 4, 2),
                ('10', 5, 0), ('0', 5, 1), ('←', 5, 2),
            ]
            for (text, r, c) in buttons:
                btn = tk.Button(self, text=text, command=lambda t=text: self.press(t), font=("Arial", 12))
                btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        def toggle_team(self):
            self.active_team = 'B' if self.active_team == 'A' else 'A'
            self.label.config(text=f"Aktiv: Team {self.active_team}")

        def get_active_var(self):
            return self.tore_team_a if self.active_team == 'A' else self.tore_team_b

        def press(self, key):
            var = self.get_active_var()
            val = var.get()
            if key == '←':
                var.set(val[:-1])
            else:
                var.set(val + key)
                self.toggle_team()
                self.switch_button.grid_remove()

    def versuche_speichern():
        if len(selected_players) != 4:
            messagebox.showerror("Fehler", "Bitte genau 4 Spieler auswählen.")
            return
        a1, a2, b1, b2 = selected_players
        ta = int(tore_team_a.get() or 0)
        tb = int(tore_team_b.get() or 0)
        if ta == tb:
            messagebox.showerror("Fehler", "Unentschieden ist nicht erlaubt.")
            return
        gewinner = "Team A" if ta > tb else "Team B"
        datum = datetime.now().strftime("%Y-%m-%d %H:%M")
        insert_match(a1, a2, b1, b2, ta, tb, gewinner, datum)
        messagebox.showinfo("Erfolg", "Spiel gespeichert!")
        selected_players.clear()
        aktualisiere_button_farben()

    # Setup UI
    spieler_liste = get_player_frequencies()
    spieler_frame = tk.Frame(root)
    spieler_frame.pack(fill="both", expand=True, padx=10, pady=5)
    build_buttons()

    action_frame = tk.Frame(root)
    action_frame.pack(fill="x", padx=10, pady=5)
    tk.Button(action_frame, text="Neuen Spieler hinzufügen", command=neuer_spieler_popup).pack(side="left")

    tore_team_a = tk.StringVar()
    tore_team_b = tk.StringVar()
    input_frame = tk.Frame(root)
    input_frame.pack(fill="x", padx=10, pady=5)
    for c in range(4):
        input_frame.columnconfigure(c, weight=1)
    tk.Label(input_frame, text="Tore Team A:", bg="lightgreen").grid(row=0, column=0, sticky="e")
    tk.Entry(input_frame, textvariable=tore_team_a, font=("Arial", 16), justify="center").grid(row=0, column=1, sticky="ew")
    tk.Label(input_frame, text="Tore Team B:", bg="lightblue").grid(row=0, column=2, sticky="e")
    tk.Entry(input_frame, textvariable=tore_team_b, font=("Arial", 16), justify="center").grid(row=0, column=3, sticky="ew")

    numpad = Numpad(root, tore_team_a, tore_team_b)
    numpad.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Button(root, text="Spiel speichern", command=versuche_speichern, height=2).pack(fill="x", padx=10, pady=10)

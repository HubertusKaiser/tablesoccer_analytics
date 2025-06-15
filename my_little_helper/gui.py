from my_little_helper.datenbank_function import init_db, get_spieler_liste, spiel_speichern

def erstelle_fenster(text_oben=None):

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

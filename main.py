import tkinter as tk
from config import text_parameter
from db import init_db
from ui_history import zeige_letzte_spiele
from ui_entry_numpad import zeige_eingabe_fenster_numpad

def main():
    init_db()

    root = tk.Tk()
    root.title(text_parameter.titel)
    # root.geometry("1700x500") # may be set later if needed

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Menü", menu=menu)
    menu.add_command(label="Ergebnisse eintragen", command=lambda: zeige_eingabe_fenster_numpad(root))
    menu.add_command(label="Letzte Spiele", command=lambda: zeige_letzte_spiele(root))

    zeige_eingabe_fenster_numpad(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from config import text_parameter
from db import init_db
from ui_entry import zeige_eingabe_fenster
from ui_history import zeige_letzte_spiele

def main():
    init_db()

    root = tk.Tk()
    root.title(text_parameter.titel)
    root.geometry("450x600")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Menü", menu=menu)
    menu.add_command(label="Ergebnisse eintragen", command=lambda: zeige_eingabe_fenster(root))
    menu.add_command(label="Letzte Spiele", command=lambda: zeige_letzte_spiele(root))

    zeige_eingabe_fenster(root)
    root.mainloop()

if __name__ == "__main__":
    main()

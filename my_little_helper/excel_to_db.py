import pandas as pd
import sqlite3

# Parameter
csv_datei = "Kicker_Tabelle.csv"
sqlite_datei = "kicker_tabelle.db"
tabelle_name = "ergebnisse"  # Name der Zieltabelle

# CSV einlesen
df = pd.read_csv(csv_datei)

# SQLite-Verbindung herstellen
with sqlite3.connect(sqlite_datei) as conn:
    # DataFrame in SQLite-Tabelle schreiben
    df.to_sql(tabelle_name, conn, if_exists='replace', index=False)

print(f"Die Daten aus '{csv_datei}' wurden erfolgreich in die SQLite-Datenbank '{sqlite_datei}' geschrieben.")
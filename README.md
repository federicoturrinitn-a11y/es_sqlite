# es_sqlite
#proviammo così
📦 SQLite – Tutte le Operazioni
pythonimport sqlite3

# Crea (o apre) il file del database. Usa ":memory:" per un DB temporaneo in RAM
conn = sqlite3.connect("database.db")
# Il cursor è lo "strumento" con cui esegui le query
cursor = conn.cursor()

1. 🏗️ CREATE TABLE

Crea la struttura della tabella. IF NOT EXISTS evita errori se la tabella esiste già. INTEGER PRIMARY KEY si autoincrementa automaticamente tramite il rowid interno di SQLite.

pythoncursor.execute("""
    CREATE TABLE IF NOT EXISTS nome_tabella (
        id INTEGER PRIMARY KEY,       -- si autoincrementa da solo
        campo_testo TEXT NOT NULL,    -- testo obbligatorio
        campo_numero INTEGER,         -- numero intero (opzionale)
        campo_decimale REAL,          -- numero con virgola (opzionale)
        campo_opzionale TEXT          -- NULL di default se non specificato
    )
""")
conn.commit()

2. ➕ INSERT

Aggiunge una nuova riga. I ? sono segnaposto sicuri per i valori — mai concatenare stringhe nelle query per evitare SQL injection.

pythoncursor.execute(
    "INSERT INTO nome_tabella (campo_testo, campo_numero) VALUES (?, ?)",
    ("valore_testo", 42)
)
conn.commit()
print(f"ID inserito: {cursor.lastrowid}")  # id dell'ultimo record inserito
Insert multiplo – più efficiente di tanti INSERT singoli:
pythondati = [("valore_1", 10), ("valore_2", 20)]
cursor.executemany(
    "INSERT INTO nome_tabella (campo_testo, campo_numero) VALUES (?, ?)",
    dati
)
conn.commit()

3. 🔍 SELECT

Legge i dati. fetchall() restituisce una lista di tuple, fetchone() solo la prima riga trovata.

Tutti i record:
pythoncursor.execute("SELECT * FROM nome_tabella")
risultati = cursor.fetchall()  # es: [(1, "testo", 42, 3.14, None), ...]
for riga in risultati:
    print(f"ID: {riga[0]} | Testo: {riga[1]} | Numero: {riga[2]}")
Un solo record per ID:
pythonid_cercato = 1
cursor.execute("SELECT * FROM nome_tabella WHERE id = ?", (id_cercato,))
riga = cursor.fetchone()  # restituisce None se non trovato
if riga:
    print(f"Trovato: {riga[1]}")
Con filtro + ordinamento:
pythonvalore_minimo = 15
cursor.execute("""
    SELECT campo_testo, campo_numero
    FROM nome_tabella
    WHERE campo_numero > ?
    ORDER BY campo_numero DESC
    LIMIT 10
""", (valore_minimo,))
for riga in cursor.fetchall():
    print(f"Testo: {riga[0]} | Numero: {riga[1]}")
Accesso per nome colonna – più leggibile degli indici numerici. Va impostato subito dopo connect():
pythonconn.row_factory = sqlite3.Row
cursor = conn.cursor()  # ricreare il cursor dopo aver impostato row_factory
cursor.execute("SELECT * FROM nome_tabella")
for riga in cursor.fetchall():
    print(f"Testo: {riga['campo_testo']} | Numero: {riga['campo_numero']}")

4. ✏️ UPDATE

Modifica i valori di record esistenti. Specifica sempre WHERE, altrimenti aggiorni tutte le righe!

pythonnuovo_valore = "testo_aggiornato"
id_da_aggiornare = 1
cursor.execute(
    "UPDATE nome_tabella SET campo_testo = ? WHERE id = ?",
    (nuovo_valore, id_da_aggiornare)
)
conn.commit()
print(f"Righe modificate: {cursor.rowcount}")

5. 🗑️ DELETE

Elimina uno o più record. Senza WHERE cancelli tutto il contenuto della tabella!

pythonid_da_eliminare = 1
cursor.execute("DELETE FROM nome_tabella WHERE id = ?", (id_da_eliminare,))
conn.commit()
print(f"Righe eliminate: {cursor.rowcount}")
Svuotare tutta la tabella:
pythoncursor.execute("DELETE FROM nome_tabella")
conn.commit()

6. 🔢 COUNT / Aggregazioni

Funzioni che calcolano statistiche su un insieme di righe. Utili per ottenere totali, massimi, minimi e medie senza caricare tutti i dati.

pythoncursor.execute("""
    SELECT COUNT(*), MAX(campo_numero), MIN(campo_numero), AVG(campo_numero)
    FROM nome_tabella
""")
riga = cursor.fetchone()
print(f"Totale: {riga[0]} | Max: {riga[1]} | Min: {riga[2]} | Media: {riga[3]:.2f}")

7. 🔗 JOIN

Unisce dati di due tabelle collegate da una chiave esterna. INNER JOIN (o semplicemente JOIN) restituisce solo le righe che hanno corrispondenza in entrambe le tabelle.

pythonsoglia = 10
cursor.execute("""
    SELECT t1.campo_testo, t2.campo_collegato
    FROM nome_tabella t1
    INNER JOIN tabella_secondaria t2 ON t1.id_fk = t2.id
    WHERE t1.campo_numero > ?
""", (soglia,))
for riga in cursor.fetchall():
    print(f"{riga[0]} → {riga[1]}")

SQLite supporta anche LEFT JOIN (include righe senza corrispondenza) ma non RIGHT JOIN né FULL OUTER JOIN.


8. 🏗️ ALTER TABLE

Modifica la struttura di una tabella esistente. SQLite supporta solo ADD COLUMN — non è possibile eliminare o rinominare colonne direttamente.

pythoncursor.execute("""
    ALTER TABLE nome_tabella
    ADD COLUMN nuova_colonna TEXT DEFAULT 'valore_default'
""")
conn.commit()

9. ❌ DROP TABLE

Elimina completamente la tabella e tutti i suoi dati. Operazione irreversibile.

pythoncursor.execute("DROP TABLE IF EXISTS nome_tabella")
conn.commit()

10. 🛡️ Gestione errori

Racchiudi le operazioni critiche in un try/except. In caso di errore, rollback() annulla le modifiche non ancora salvate con commit().

pythontry:
    cursor.execute(
        "INSERT INTO nome_tabella (campo_testo, campo_numero) VALUES (?, ?)",
        (valore_testo, valore_numero)
    )
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Errore vincolo: {e}")    # es. valore NULL su campo NOT NULL
    conn.rollback()
except sqlite3.OperationalError as e:
    print(f"Errore operativo: {e}")  # es. tabella inesistente, sintassi errata
finally:
    conn.close()  # chiude sempre la connessione, anche in caso di errore

🔑 Tipi di dati SQLite
Tipo SQLiteEquivalente PythonUso tipicoINTEGERintID, contatori, anniREALfloatPrezzi, misure, percentualiTEXTstrNomi, descrizioni, dateBLOBbytesFile binari, immaginiNULLNoneValore assente/non definito

Le correzioni principali rispetto a prima: rimosso AUTOINCREMENT, aggiunto il cursor = conn.cursor() dopo row_factory, specificato che SQLite non supporta RIGHT JOIN e FULL OUTER JOIN, e rimosso DEFAULT NULL che è già il comportamento di default.come faccio ad aggiungere un altra colonna?22:26Hai già la risposta nel punto 8! 😄
pythoncursor.execute("""
    ALTER TABLE nome_tabella
    ADD COLUMN nuova_colonna TEXT DEFAULT 'valore_default'
""")
conn.commit()
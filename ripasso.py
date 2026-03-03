
import sqlite3
conn = sqlite3.connect("libri.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS libri (
               
               id INTEGER PRIMARY KEY,
               titolo TEXT,
               autore TEXT,
               n_copie INTEGER
               )
               """)

conn.commit()



while True:
    print("1. vedere tutta la lista")
    print("2. aggiungere libro alla lista")
    print("3. selezionare per nome una lista")
    print("4. aggiungere una copia alla lista")
    print("5. esci dalla selezione: ")
    decisione= input("cosa vuoi fare? ")
    if decisione == "1":
        cursor.execute("""SELECT * FROM libri
        """)
        risultati = cursor.fetchall()
        for i in risultati:
            print(i)
    if decisione == "2":
        nome=input("inserisci il nome del libro: ")
        autore=input("inserisci il nome del autore: ")
        copie=int(input("inserire in numero delle copie: "))
        query= """INSERT INTO libri (titolo, autore, n_copie ) VALUES (?,?,?)"""
        cursor.execute(query, (nome,autore,copie))
        conn.commit()
    if decisione == "3":
        resc=input("dimmi che libro vuoi cercare: ")
        fin= f"%{resc}%"
        cursor.execute("""SELECT titolo FROM libri WHERE titolo LIKE ?""", (fin,))
        result = cursor.fetchall()
        if result:
            for i in result:
                print(i)
        else:
            print("nessun brano trovato")
    if decisione == "4":
        piu=input("che libro vuoi aggiungere")
        cursor.execute("UPDATE libri SET n_copie = n_copie + 1 WHERE titolo= ?",(piu,))
        conn.commit()







    if decisione =="5":
        break 


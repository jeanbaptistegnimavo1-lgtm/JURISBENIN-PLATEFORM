import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

try:
    curseur.execute("ALTER TABLE textes ADD COLUMN numero TEXT DEFAULT ''")
    print("Colonne 'numero' ajoutée.")
except sqlite3.OperationalError:
    print("La colonne 'numero' existe déjà.")

connexion.commit()
connexion.close()
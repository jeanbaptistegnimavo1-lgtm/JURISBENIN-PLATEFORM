import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

curseur.execute("""
    UPDATE textes
    SET nature = 'Loi'
    WHERE TRIM(LOWER(nature)) = 'loi'
""")

print(curseur.rowcount, "lignes corrigées")

connexion.commit()
connexion.close()
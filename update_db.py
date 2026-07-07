import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

try:
    curseur.execute(
        "ALTER TABLE lois ADD COLUMN pdf TEXT"
    )
except:
    pass

try:
    curseur.execute(
        "ALTER TABLE decrets ADD COLUMN pdf TEXT"
    )
except:
    pass

connexion.commit()
connexion.close()

print("Base mise à jour.")
import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

try:
    curseur.execute(
        "ALTER TABLE lois ADD COLUMN pdf TEXT"
    )
except:
    pass

try:
    curseur.execute(
        "ALTER TABLE decrets ADD COLUMN pdf TEXT"
    )
except:
    pass

connexion.commit()
connexion.close()

print("Base mise à jour.")
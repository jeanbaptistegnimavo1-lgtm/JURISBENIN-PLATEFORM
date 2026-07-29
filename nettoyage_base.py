import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

# Numéros des vrais textes à garder
numeros_a_garder = [
    "du 11 décembre 1990",
    "2018-16",
    "98-004",
    "2013-01",
    "2017-20",
    "2012-15",
    "91-009",
    "2004-07"
]

# Supprimer tous les textes sauf les vrais
placeholders = ",".join("?" * len(numeros_a_garder))
curseur.execute(
    f"DELETE FROM textes WHERE numero NOT IN ({placeholders})",
    numeros_a_garder
)

supprimes = curseur.rowcount
connexion.commit()
connexion.close()

print(f"✅ {supprimes} texte(s) de test supprimé(s).")
print("Base de données nettoyée.")
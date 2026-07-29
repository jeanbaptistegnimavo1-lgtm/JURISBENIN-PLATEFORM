import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

# Ajouter la colonne provisoire
try:
    curseur.execute("ALTER TABLE textes ADD COLUMN provisoire INTEGER DEFAULT 0")
    print("✅ Colonne 'provisoire' ajoutée.")
except Exception:
    print("⚠️  Colonne déjà existante.")

# Marquer les 8 textes actuels comme provisoires
curseur.execute("UPDATE textes SET provisoire = 1")
print(f"✅ {curseur.rowcount} texte(s) marqué(s) comme provisoires.")

connexion.commit()
connexion.close()
import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
connexion.row_factory = sqlite3.Row
curseur = connexion.cursor()

# 1. Création de la table unique "textes"
curseur.execute("""
CREATE TABLE IF NOT EXISTS textes (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    titre     TEXT NOT NULL,
    nature    TEXT NOT NULL,
    categorie TEXT DEFAULT '',
    date      TEXT NOT NULL,
    contenu   TEXT NOT NULL,
    pdf       TEXT
)
""")

# 2. Migration des lois -> textes (nature = type existant, ex: "Loi", "Code", "Constitution")
lois = curseur.execute("SELECT * FROM lois").fetchall()
for loi in lois:
    curseur.execute("""
        INSERT INTO textes (titre, nature, categorie, date, contenu, pdf)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        loi["titre"],
        loi["type"],
        loi["categorie"] or "",
        loi["date"],
        loi["contenu"],
        loi["pdf"]
    ))

print(f"{len(lois)} lois migrées vers 'textes'.")

# 3. Migration des décrets -> textes (nature = "Décret")
decrets = curseur.execute("SELECT * FROM decrets").fetchall()
for decret in decrets:
    curseur.execute("""
        INSERT INTO textes (titre, nature, categorie, date, contenu, pdf)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        decret["titre"],
        "Décret",
        decret["categorie"] if "categorie" in decret.keys() else "",
        decret["date"],
        decret["contenu"],
        None
    ))

print(f"{len(decrets)} décrets migrés vers 'textes'.")

connexion.commit()
connexion.close()

print("Migration terminée. Les anciennes tables 'lois' et 'decrets' sont conservées intactes.")
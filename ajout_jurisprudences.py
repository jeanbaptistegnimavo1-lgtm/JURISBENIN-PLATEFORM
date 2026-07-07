import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS jurisprudences (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    titre          TEXT NOT NULL,
    juridiction    TEXT NOT NULL,
    chambre        TEXT DEFAULT '',
    numero_affaire TEXT DEFAULT '',
    date           TEXT NOT NULL,
    parties        TEXT DEFAULT '',
    matiere        TEXT DEFAULT '',
    resume         TEXT DEFAULT '',
    decision       TEXT NOT NULL,
    textes_cites   TEXT DEFAULT '',
    pdf            TEXT
)
""")

print("Table 'jurisprudences' créée avec succès.")

connexion.commit()
connexion.close()
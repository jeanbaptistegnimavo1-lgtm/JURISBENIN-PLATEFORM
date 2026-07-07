import sqlite3
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

# CORRECTION 5 : colonne categorie directement dans le CREATE TABLE
curseur.execute("""
CREATE TABLE IF NOT EXISTS lois (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    titre    TEXT NOT NULL,
    type     TEXT NOT NULL,
    categorie TEXT DEFAULT '',
    date     TEXT NOT NULL,
    contenu  TEXT NOT NULL,
    pdf      TEXT
)
""")

curseur.execute("""
CREATE TABLE IF NOT EXISTS decrets (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    titre     TEXT NOT NULL,
    date      TEXT NOT NULL,
    contenu   TEXT NOT NULL,
    categorie TEXT DEFAULT ''
)
""")

curseur.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# CORRECTION 4 : mot de passe hashé dès la création
curseur.execute("""
INSERT OR IGNORE INTO admin (username, password)
VALUES (?, ?)
""", ("admin", hash_password("juris123")))

# Migration : si l'admin existe déjà avec un mot de passe en clair, le hasher
curseur.execute("SELECT id, password FROM admin WHERE username = 'admin'")
row = curseur.fetchone()
if row:
    pwd = row[1]
    # Un hash SHA-256 fait 64 caractères hex — si ce n'est pas le cas, c'est du clair
    if len(pwd) != 64:
        curseur.execute(
            "UPDATE admin SET password = ? WHERE username = 'admin'",
            (hash_password(pwd),)
        )

# Migration : ajouter les colonnes manquantes si la DB existait déjà
for colonne_sql in [
    "ALTER TABLE lois ADD COLUMN categorie TEXT DEFAULT ''",
    "ALTER TABLE lois ADD COLUMN pdf TEXT",
    "ALTER TABLE decrets ADD COLUMN categorie TEXT DEFAULT ''",
]:
    try:
        curseur.execute(colonne_sql)
    except Exception:
        pass  # colonne déjà présente

lois_exemples = [
    ("Constitution du Bénin",  "Constitution", "Droit constitutionnel", "Révisée en 2019",
     "Texte fondamental organisant les institutions de la République du Bénin.", None),
    ("Code pénal",             "Code",         "Droit pénal",           "2018",
     "Ensemble des règles définissant les infractions et les peines.",           None),
    ("Code du numérique",      "Code",         "Droit numérique",       "2017",
     "Cadre juridique du numérique au Bénin.",                                   None),
    ("Code foncier",           "Code",         "Droit foncier",         "2013",
     "Organisation de la propriété et de la gestion foncière.",                  None),
    ("Code du travail",        "Code",         "Droit du travail",      "1998",
     "Règles relatives aux relations de travail.",                                None),
]

if curseur.execute("SELECT COUNT(*) FROM lois").fetchone()[0] == 0:
    curseur.executemany("""
    INSERT INTO lois (titre, type, categorie, date, contenu, pdf)
    VALUES (?, ?, ?, ?, ?, ?)
    """, lois_exemples)

decrets_exemples = [
    ("Décret portant création de l'Agence du Numérique", "2022",
     "Création et organisation de l'Agence du Numérique."),
    ("Décret relatif à la fonction publique",            "2021",
     "Mesures d'application du statut général des agents publics."),
    ("Décret sur les marchés publics",                   "2020",
     "Règles relatives à la passation des marchés publics."),
]

if curseur.execute("SELECT COUNT(*) FROM decrets").fetchone()[0] == 0:
    curseur.executemany("""
    INSERT INTO decrets (titre, date, contenu)
    VALUES (?, ?, ?)
    """, decrets_exemples)

connexion.commit()
connexion.close()

print("Base de données initialisée avec succès.")

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import shutil
import hashlib
from datetime import datetime, timedelta

tentatives_echecs = {}
app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="jurisbenin_secret"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ─── ACCUEIL ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    nb_lois = curseur.execute(
        "SELECT COUNT(*) FROM textes WHERE nature != 'Décret'"
    ).fetchone()[0]
    nb_decrets = curseur.execute(
        "SELECT COUNT(*) FROM textes WHERE nature = 'Décret'"
    ).fetchone()[0]
    dernieres_lois = curseur.execute(
        "SELECT * FROM textes WHERE nature != 'Décret' ORDER BY id DESC LIMIT 3"
    ).fetchall()
    derniers_decrets = curseur.execute(
        "SELECT * FROM textes WHERE nature = 'Décret' ORDER BY id DESC LIMIT 3"
    ).fetchall()

    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "nb_lois": nb_lois,
            "nb_decrets": nb_decrets,
            "dernieres_lois": dernieres_lois,
            "derniers_decrets": derniers_decrets
        }
    )


# ─── LOIS ────────────────────────────────────────────────────────────────

@app.get("/lois", response_class=HTMLResponse)
def lois(
    request: Request,
    recherche: str = "",
    categorie: str = "",
    page: int = 1
):
    par_page = 10
    offset = (page - 1) * par_page

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    categories = curseur.execute(
        """
        SELECT DISTINCT categorie FROM textes
        WHERE nature != 'Décret' AND categorie IS NOT NULL AND categorie != ''
        ORDER BY categorie
        """
    ).fetchall()
    categories = [c["categorie"] for c in categories]

    total = curseur.execute(
        """
        SELECT COUNT(*) FROM textes
        WHERE nature != 'Décret'
        AND (titre LIKE ? OR contenu LIKE ?)
        AND (? = '' OR categorie = ?)
        """,
        (f"%{recherche}%", f"%{recherche}%", categorie, categorie)
    ).fetchone()[0]

    total_pages = max(1, (total + par_page - 1) // par_page)

    curseur.execute(
        """
        SELECT * FROM textes
        WHERE nature != 'Décret'
        AND (titre LIKE ? OR contenu LIKE ?)
        AND (? = '' OR categorie = ?)
        LIMIT ? OFFSET ?
        """,
        (f"%{recherche}%", f"%{recherche}%", categorie, categorie, par_page, offset)
    )

    lois_benin = curseur.fetchall()
    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="lois.html",
        context={
            "lois": lois_benin,
            "recherche": recherche,
            "categorie": categorie,
            "page": page,
            "total_pages": total_pages,
            "categories": categories
        }
    )


@app.get("/loi/{id}", response_class=HTMLResponse)
def loi_detail(request: Request, id: int):
    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM textes WHERE id = ?", (id,))
    loi = curseur.fetchone()

    if loi is None:
        connexion.close()
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=404
        )

    # Recommandations : même catégorie OU même nature, hors texte actuel
    similaires = curseur.execute(
        """
        SELECT * FROM textes
        WHERE id != ?
        AND (
            (categorie = ? AND categorie != '')
            OR nature = ?
        )
        ORDER BY RANDOM()
        LIMIT 3
        """,
        (id, loi["categorie"], loi["nature"])
    ).fetchall()

    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="loi_detail.html",
        context={
            "id": loi["id"],
            "titre": loi["titre"],
            "type": loi["nature"],
            "categorie": loi["categorie"],
            "numero": loi["numero"],
            "date": loi["date"],
            "contenu": loi["contenu"],
            "pdf": loi["pdf"],
            "admin": request.session.get("admin"),
            "similaires": similaires
        }
    )


@app.post("/admin")
def ajouter_loi(
    request: Request,
    titre: str = Form(...),
    type: str = Form(...),
    categorie: str = Form(""),
    numero: str = Form(""),
    date: str = Form(...),
    contenu: str = Form(""),
    pdf: UploadFile = File(None)
):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    nom_pdf = None
    if pdf and pdf.filename:
        nom_pdf = pdf.filename
        with open(f"static/pdf/{nom_pdf}", "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    connexion = sqlite3.connect("jurisbenin.db")
    curseur = connexion.cursor()
    curseur.execute(
        """
        INSERT INTO textes (titre, nature, categorie, numero, date, contenu, pdf)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (titre, type, categorie, numero, date, contenu, nom_pdf)
    )
    connexion.commit()
    connexion.close()

    request.session["message"] = "Loi ajoutée avec succès ✅"
    return RedirectResponse(url="/admin", status_code=303)


# ─── DÉCRETS ─────────────────────────────────────────────────────────────

@app.get("/decrets", response_class=HTMLResponse)
def decrets(request: Request, page: int = 1, recherche: str = "", type: str = ""):
    par_page = 10
    offset = (page - 1) * par_page

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    total = curseur.execute(
        """
        SELECT COUNT(*) FROM textes
        WHERE nature = 'Décret'
        AND (titre LIKE ? OR contenu LIKE ?)
        AND (? = '' OR categorie = ?)
        """,
        (f"%{recherche}%", f"%{recherche}%", type, type)
    ).fetchone()[0]
    total_pages = max(1, (total + par_page - 1) // par_page)

    curseur.execute(
        """
        SELECT * FROM textes
        WHERE nature = 'Décret'
        AND (titre LIKE ? OR contenu LIKE ?)
        AND (? = '' OR categorie = ?)
        LIMIT ? OFFSET ?
        """,
        (f"%{recherche}%", f"%{recherche}%", type, type, par_page, offset)
    )
    decrets_benin = curseur.fetchall()
    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="decrets.html",
        context={
            "decrets": decrets_benin,
            "page": page,
            "total_pages": total_pages,
            "recherche": recherche,
            "type": type
        }
    )


@app.get("/decret/{id}", response_class=HTMLResponse)
def decret_detail(request: Request, id: int):
    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM textes WHERE id = ?", (id,))
    decret = curseur.fetchone()

    if decret is None:
        connexion.close()
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=404
        )

    # Recommandations
    similaires = curseur.execute(
        """
        SELECT * FROM textes
        WHERE id != ?
        AND (
            (categorie = ? AND categorie != '')
            OR nature = ?
        )
        ORDER BY RANDOM()
        LIMIT 3
        """,
        (id, decret["categorie"], decret["nature"])
    ).fetchall()

    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="decret_detail.html",
        context={
            "id": decret["id"],
            "titre": decret["titre"],
            "categorie": decret["categorie"],
            "numero": decret["numero"],
            "date": decret["date"],
            "contenu": decret["contenu"],
            "pdf": decret["pdf"],
            "admin": request.session.get("admin"),
            "similaires": similaires
        }
    )


@app.post("/admin/decret")
def ajouter_decret(
    request: Request,
    titre: str = Form(...),
    categorie: str = Form(""),
    numero: str = Form(""),
    date: str = Form(...),
    contenu: str = Form(""),
    pdf: UploadFile = File(None)
):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    nom_pdf = None
    if pdf and pdf.filename:
        nom_pdf = pdf.filename
        with open(f"static/pdf/{nom_pdf}", "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    connexion = sqlite3.connect("jurisbenin.db")
    curseur = connexion.cursor()
    curseur.execute(
        """
        INSERT INTO textes (titre, nature, categorie, numero, date, contenu, pdf)
        VALUES (?, 'Décret', ?, ?, ?, ?, ?)
        """,
        (titre, categorie, numero, date, contenu, nom_pdf)
    )
    connexion.commit()
    connexion.close()

    request.session["message"] = "Décret ajouté avec succès ✅"
    return RedirectResponse(url="/admin", status_code=303)


# ─── ADMIN ───────────────────────────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    nb_lois = curseur.execute(
        "SELECT COUNT(*) FROM textes WHERE nature != 'Décret'"
    ).fetchone()[0]
    nb_decrets = curseur.execute(
        "SELECT COUNT(*) FROM textes WHERE nature = 'Décret'"
    ).fetchone()[0]
    lois = curseur.execute(
        "SELECT * FROM textes WHERE nature != 'Décret' ORDER BY id DESC"
    ).fetchall()
    decrets = curseur.execute(
        "SELECT * FROM textes WHERE nature = 'Décret' ORDER BY id DESC"
    ).fetchall()

    connexion.close()

    message = request.session.pop("message", None)

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "nb_lois": nb_lois,
            "nb_decrets": nb_decrets,
            "total": nb_lois + nb_decrets,
            "lois": lois,
            "decrets": decrets,
            "message": message
        }
    )


@app.get("/modifier/{id}", response_class=HTMLResponse)
def modifier_loi(request: Request, id: int):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM textes WHERE id = ?", (id,))
    loi = curseur.fetchone()
    connexion.close()

    if loi is None:
        return templates.TemplateResponse(
            request=request, name="404.html", context={}, status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="modifier.html",
        context={
            "id": loi["id"],
            "titre": loi["titre"],
            "type": loi["nature"],
            "categorie": loi["categorie"],
            "numero": loi["numero"],
            "date": loi["date"],
            "contenu": loi["contenu"],
            "pdf": loi["pdf"]
        }
    )


@app.post("/modifier/{id}")
def enregistrer_modification(
    request: Request,
    id: int,
    titre: str = Form(...),
    type: str = Form(...),
    categorie: str = Form(""),
    numero: str = Form(""),
    date: str = Form(...),
    contenu: str = Form(""),
    pdf: UploadFile = File(None)
):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    nom_pdf = curseur.execute(
        "SELECT pdf FROM textes WHERE id = ?", (id,)
    ).fetchone()["pdf"]

    if pdf and pdf.filename:
        nom_pdf = pdf.filename
        with open(f"static/pdf/{nom_pdf}", "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    curseur.execute(
        """
        UPDATE textes
        SET titre = ?, nature = ?, categorie = ?, numero = ?, date = ?, contenu = ?, pdf = ?
        WHERE id = ?
        """,
        (titre, type, categorie, numero, date, contenu, nom_pdf, id)
    )
    connexion.commit()
    connexion.close()

    request.session["message"] = "Loi modifiée avec succès ✅"
    return RedirectResponse(url="/admin", status_code=303)


@app.get("/modifier-decret/{id}", response_class=HTMLResponse)
def modifier_decret(request: Request, id: int):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM textes WHERE id = ?", (id,))
    decret = curseur.fetchone()
    connexion.close()

    if decret is None:
        return templates.TemplateResponse(
            request=request, name="404.html", context={}, status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="modifier_decret.html",
        context={
            "id": decret["id"],
            "titre": decret["titre"],
            "categorie": decret["categorie"],
            "numero": decret["numero"],
            "date": decret["date"],
            "contenu": decret["contenu"],
            "pdf": decret["pdf"]
        }
    )


@app.post("/modifier-decret/{id}")
def enregistrer_modification_decret(
    request: Request,
    id: int,
    titre: str = Form(...),
    categorie: str = Form(""),
    numero: str = Form(""),
    date: str = Form(...),
    contenu: str = Form(""),
    pdf: UploadFile = File(None)
):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    nom_pdf = curseur.execute(
        "SELECT pdf FROM textes WHERE id = ?", (id,)
    ).fetchone()["pdf"]

    if pdf and pdf.filename:
        nom_pdf = pdf.filename
        with open(f"static/pdf/{nom_pdf}", "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    curseur.execute(
        "UPDATE textes SET titre = ?, categorie = ?, numero = ?, date = ?, contenu = ?, pdf = ? WHERE id = ?",
        (titre, categorie, numero, date, contenu, nom_pdf, id)
    )
    connexion.commit()
    connexion.close()

    request.session["message"] = "Décret modifié avec succès ✅"
    return RedirectResponse(url="/admin", status_code=303)


@app.get("/supprimer/{id}")
def supprimer_loi(request: Request, id: int):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM textes WHERE id = ?", (id,))
    connexion.commit()
    connexion.close()

    request.session["message"] = "Loi supprimée ✅"
    return RedirectResponse(url="/admin", status_code=303)


@app.get("/supprimer-decret/{id}")
def supprimer_decret(request: Request, id: int):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM textes WHERE id = ?", (id,))
    connexion.commit()
    connexion.close()

    request.session["message"] = "Décret supprimé ✅"
    return RedirectResponse(url="/admin", status_code=303)
# ─── JURISPRUDENCE ───────────────────────────────────────────────────────

@app.get("/jurisprudences", response_class=HTMLResponse)
def jurisprudences(
    request: Request,
    recherche: str = "",
    juridiction: str = "",
    matiere: str = "",
    page: int = 1
):
    par_page = 10
    offset = (page - 1) * par_page

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    # Listes pour les filtres
    juridictions = curseur.execute(
        "SELECT DISTINCT juridiction FROM jurisprudences ORDER BY juridiction"
    ).fetchall()
    juridictions = [j["juridiction"] for j in juridictions]

    matieres = curseur.execute(
        "SELECT DISTINCT matiere FROM jurisprudences WHERE matiere != '' ORDER BY matiere"
    ).fetchall()
    matieres = [m["matiere"] for m in matieres]

    # Construction de la requête
    conditions = ["1=1"]
    params = []

    if recherche:
        conditions.append("(titre LIKE ? OR resume LIKE ? OR decision LIKE ? OR parties LIKE ?)")
        params.extend([f"%{recherche}%"] * 4)

    if juridiction:
        conditions.append("juridiction = ?")
        params.append(juridiction)

    if matiere:
        conditions.append("matiere = ?")
        params.append(matiere)

    where = "WHERE " + " AND ".join(conditions)

    total = curseur.execute(
        f"SELECT COUNT(*) FROM jurisprudences {where}", params
    ).fetchone()[0]

    total_pages = max(1, (total + par_page - 1) // par_page)

    resultats = curseur.execute(
        f"SELECT * FROM jurisprudences {where} ORDER BY date DESC LIMIT ? OFFSET ?",
        params + [par_page, offset]
    ).fetchall()

    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="jurisprudences.html",
        context={
            "jurisprudences": resultats,
            "recherche": recherche,
            "juridiction": juridiction,
            "matiere": matiere,
            "juridictions": juridictions,
            "matieres": matieres,
            "page": page,
            "total_pages": total_pages,
            "total": total
        }
    )


@app.get("/jurisprudence/{id}", response_class=HTMLResponse)
def jurisprudence_detail(request: Request, id: int):
    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    curseur.execute("SELECT * FROM jurisprudences WHERE id = ?", (id,))
    juris = curseur.fetchone()

    if juris is None:
        connexion.close()
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=404
        )

    # Textes de lois cités (IDs séparés par des virgules)
    textes_cites = []
    if juris["textes_cites"]:
        ids = [i.strip() for i in juris["textes_cites"].split(",") if i.strip().isdigit()]
        if ids:
            placeholders = ",".join("?" * len(ids))
            textes_cites = curseur.execute(
                f"SELECT * FROM textes WHERE id IN ({placeholders})", ids
            ).fetchall()

    # Décisions similaires (même juridiction ou même matière)
    similaires = curseur.execute(
        """
        SELECT * FROM jurisprudences
        WHERE id != ?
        AND (juridiction = ? OR (matiere = ? AND matiere != ''))
        ORDER BY RANDOM()
        LIMIT 3
        """,
        (id, juris["juridiction"], juris["matiere"])
    ).fetchall()

    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="jurisprudence_detail.html",
        context={
            "juris": juris,
            "textes_cites": textes_cites,
            "similaires": similaires,
            "admin": request.session.get("admin")
        }
    )


@app.post("/admin/jurisprudence")
def ajouter_jurisprudence(
    request: Request,
    titre: str = Form(...),
    juridiction: str = Form(...),
    chambre: str = Form(""),
    numero_affaire: str = Form(""),
    date: str = Form(...),
    parties: str = Form(""),
    matiere: str = Form(""),
    resume: str = Form(""),
    decision: str = Form(...),
    textes_cites: str = Form(""),
    pdf: UploadFile = File(None)
):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    nom_pdf = None
    if pdf and pdf.filename:
        nom_pdf = pdf.filename
        with open(f"static/pdf/{nom_pdf}", "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    connexion = sqlite3.connect("jurisbenin.db")
    curseur = connexion.cursor()
    curseur.execute(
        """
        INSERT INTO jurisprudences
        (titre, juridiction, chambre, numero_affaire, date, parties, matiere, resume, decision, textes_cites, pdf)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (titre, juridiction, chambre, numero_affaire, date, parties, matiere, resume, decision, textes_cites, nom_pdf)
    )
    connexion.commit()
    connexion.close()

    return RedirectResponse(url="/jurisprudences", status_code=303)


@app.get("/modifier-jurisprudence/{id}", response_class=HTMLResponse)
def modifier_jurisprudence(request: Request, id: int):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM jurisprudences WHERE id = ?", (id,))
    juris = curseur.fetchone()
    connexion.close()

    if juris is None:
        return templates.TemplateResponse(
            request=request, name="404.html", context={}, status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="modifier_jurisprudence.html",
        context={"juris": juris}
    )


@app.post("/modifier-jurisprudence/{id}")
def enregistrer_modification_jurisprudence(
    request: Request,
    id: int,
    titre: str = Form(...),
    juridiction: str = Form(...),
    chambre: str = Form(""),
    numero_affaire: str = Form(""),
    date: str = Form(...),
    parties: str = Form(""),
    matiere: str = Form(""),
    resume: str = Form(""),
    decision: str = Form(...),
    textes_cites: str = Form(""),
    pdf: UploadFile = File(None)
):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    nom_pdf = curseur.execute(
        "SELECT pdf FROM jurisprudences WHERE id = ?", (id,)
    ).fetchone()["pdf"]

    if pdf and pdf.filename:
        nom_pdf = pdf.filename
        with open(f"static/pdf/{nom_pdf}", "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    curseur.execute(
        """
        UPDATE jurisprudences
        SET titre = ?, juridiction = ?, chambre = ?, numero_affaire = ?,
            date = ?, parties = ?, matiere = ?, resume = ?,
            decision = ?, textes_cites = ?, pdf = ?
        WHERE id = ?
        """,
        (titre, juridiction, chambre, numero_affaire, date, parties,
         matiere, resume, decision, textes_cites, nom_pdf, id)
    )
    connexion.commit()
    connexion.close()

    return RedirectResponse(url=f"/jurisprudence/{id}", status_code=303)


@app.get("/supprimer-jurisprudence/{id}")
def supprimer_jurisprudence(request: Request, id: int):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=303)

    connexion = sqlite3.connect("jurisbenin.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM jurisprudences WHERE id = ?", (id,))
    connexion.commit()
    connexion.close()

    return RedirectResponse(url="/jurisprudences", status_code=303)
# ─── RECHERCHE AVANCÉE ───────────────────────────────────────────────────

@app.get("/recherche", response_class=HTMLResponse)
def recherche(
    request: Request,
    q: str = "",
    nature: str = "",
    categorie: str = "",
    numero: str = "",
    date_debut: str = "",
    date_fin: str = "",
    page: int = 1
):
    par_page = 10
    offset = (page - 1) * par_page

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    # Liste des natures distinctes pour le menu déroulant
    natures = curseur.execute(
        "SELECT DISTINCT nature FROM textes ORDER BY nature"
    ).fetchall()
    natures = [n["nature"] for n in natures]

    # Liste des catégories distinctes
    categories = curseur.execute(
        "SELECT DISTINCT categorie FROM textes WHERE categorie IS NOT NULL AND categorie != '' ORDER BY categorie"
    ).fetchall()
    categories = [c["categorie"] for c in categories]

    # Construction dynamique de la requête
    conditions = []
    params = []

    if q:
        conditions.append("(titre LIKE ? OR contenu LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])

    if nature:
        conditions.append("nature = ?")
        params.append(nature)

    if categorie:
        conditions.append("categorie = ?")
        params.append(categorie)

    if numero:
        conditions.append("numero LIKE ?")
        params.append(f"%{numero}%")

    if date_debut:
        conditions.append("date >= ?")
        params.append(date_debut)

    if date_fin:
        conditions.append("date <= ?")
        params.append(date_fin)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    total = curseur.execute(
        f"SELECT COUNT(*) FROM textes {where}", params
    ).fetchone()[0]

    total_pages = max(1, (total + par_page - 1) // par_page)

    resultats = curseur.execute(
        f"SELECT * FROM textes {where} ORDER BY date DESC LIMIT ? OFFSET ?",
        params + [par_page, offset]
    ).fetchall()

    connexion.close()

    return templates.TemplateResponse(
        request=request,
        name="recherche.html",
        context={
            "resultats": resultats,
            "q": q,
            "nature": nature,
            "categorie": categorie,
            "numero": numero,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "natures": natures,
            "categories": categories,
            "page": page,
            "total_pages": total_pages,
            "total": total
        }
    )
# ─── LOGIN / LOGOUT ──────────────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    now = datetime.now()
    ip = request.client.host
    print(f"IP: {ip}, tentatives: {tentatives_echecs}")

    # Vérifier si l'IP est bloquée
    if ip in tentatives_echecs:
        donnees = tentatives_echecs[ip]
        if donnees["compteur"] >= 3:
            if now < donnees["bloque_jusqu"]:
                temps_restant = int((donnees["bloque_jusqu"] - now).total_seconds() / 60) + 1
                return templates.TemplateResponse(
                    request=request,
                    name="login.html",
                    context={"erreur": f"Trop de tentatives. Réessayez dans {temps_restant} minute(s)."}
                )
            else:
                tentatives_echecs.pop(ip)

    connexion = sqlite3.connect("jurisbenin.db")
    connexion.row_factory = sqlite3.Row
    curseur = connexion.cursor()

    hashed = hash_password(password)
    curseur.execute(
        "SELECT * FROM admin WHERE username = ? AND password = ?",
        (username, hashed)
    )
    admin_user = curseur.fetchone()
    connexion.close()

    if admin_user:
        tentatives_echecs.pop(ip, None)
        request.session["admin"] = True
        return RedirectResponse(url="/admin", status_code=303)

    # Enregistrer l'échec
    if ip not in tentatives_echecs:
        tentatives_echecs[ip] = {"compteur": 0, "bloque_jusqu": now + timedelta(days=999)}
    tentatives_echecs[ip]["compteur"] += 1

    compteur = tentatives_echecs[ip]["compteur"]

    if compteur >= 3:
        tentatives_echecs[ip]["bloque_jusqu"] = now + timedelta(minutes=5)
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"erreur": "Trop de tentatives. Réessayez dans 5 minute(s)."}
        )

    restantes = 3 - compteur
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"erreur": f"Identifiants incorrects. {restantes} tentative(s) restante(s)."}
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/test")
def test():
    return {"message": "ça marche"}
from routes.auth import router as auth_router

app.include_router(auth_router)
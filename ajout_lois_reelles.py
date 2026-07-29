import sqlite3

connexion = sqlite3.connect("jurisbenin.db")
curseur = connexion.cursor()

lois = [
    {
        "titre": "Constitution de la République du Bénin",
        "nature": "Constitution",
        "categorie": "Droit constitutionnel",
        "numero": "du 11 décembre 1990",
        "date": "1990",
        "contenu": """La Constitution de la République du Bénin a été adoptée par référendum le 2 décembre 1990 et promulguée le 11 décembre 1990. Elle a été révisée par la loi n°2019-40 du 07 novembre 2019.

TITRE PREMIER — DE L'ÉTAT ET DE LA SOUVERAINETÉ
Article 1 : Le Bénin est une République indépendante et souveraine. La capitale est Porto-Novo.
Article 2 : La devise de la République du Bénin est : Fraternité — Justice — Travail.
Article 3 : La souveraineté nationale appartient au peuple. Aucune fraction du peuple, aucun individu ne peut s'en attribuer l'exercice.

TITRE II — DES DROITS ET DEVOIRS DE LA PERSONNE HUMAINE
Article 8 : La personne humaine est sacrée et inviolable. L'État a l'obligation absolue de la respecter et de la protéger.
Article 19 : Tout individu a droit à la liberté et à la sécurité. Nul ne peut être arrêté ou détenu arbitrairement.
Article 26 : L'État assure à tous l'égalité devant la loi sans distinction d'origine, de race, de sexe, de religion, d'opinion politique ou de position sociale.

TITRE III — DU POUVOIR DE L'ÉTAT
Article 35 : Le Président de la République est le Chef de l'État. Il est élu au suffrage universel direct pour un mandat de cinq ans renouvelable une seule fois.
Article 79 : Le Parlement est composé d'une seule Assemblée dénommée Assemblée Nationale."""
    },
    {
        "titre": "Code pénal de la République du Bénin",
        "nature": "Code",
        "categorie": "Droit pénal",
        "numero": "2018-16",
        "date": "2018",
        "contenu": """Loi n°2018-16 du 28 décembre 2018 portant Code pénal en République du Bénin.

LIVRE PREMIER — DES INFRACTIONS ET DES PEINES EN GÉNÉRAL

TITRE I — DE LA LOI PÉNALE
Article 1 : Nul ne peut être puni pour un crime, un délit ou une contravention dont les éléments ne sont pas définis par la loi, ni pour une peine qui n'y est pas prévue.

TITRE II — DES PEINES
Article 14 : Les peines applicables aux personnes physiques sont : l'emprisonnement, l'amende, le travail d'intérêt général, la confiscation, l'interdiction de certains droits.
Article 15 : La peine d'emprisonnement est prononcée pour une durée déterminée. Elle ne peut excéder trente ans en matière correctionnelle.

LIVRE DEUXIÈME — DES INFRACTIONS ET DE LEURS PEINES

TITRE I — DES ATTEINTES AUX PERSONNES
Article 118 : L'homicide volontaire est qualifié meurtre. Il est puni de dix à vingt ans d'emprisonnement.
Article 119 : Le meurtre commis avec préméditation est qualifié assassinat. Il est puni de vingt à trente ans d'emprisonnement.

TITRE II — DES ATTEINTES AUX BIENS
Article 463 : Le vol est la soustraction frauduleuse de la chose d'autrui. Il est puni d'un à cinq ans d'emprisonnement et d'une amende."""
    },
    {
        "titre": "Code du travail de la République du Bénin",
        "nature": "Code",
        "categorie": "Droit du travail",
        "numero": "98-004",
        "date": "1998",
        "contenu": """Loi n°98-004 du 27 janvier 1998 portant Code du travail en République du Bénin.

TITRE PREMIER — DISPOSITIONS GÉNÉRALES
Article 1 : Le présent code s'applique aux travailleurs et aux employeurs exerçant leurs activités professionnelles sur le territoire de la République du Bénin.
Article 2 : Est considéré comme travailleur, quels que soient son sexe et sa nationalité, toute personne qui s'est engagée à mettre son activité professionnelle moyennant rémunération.

TITRE II — DU CONTRAT DE TRAVAIL
Article 6 : Le contrat de travail est une convention par laquelle une personne s'engage à mettre son activité à la disposition d'une autre, sous la subordination de laquelle elle se place, moyennant rémunération.
Article 10 : Le contrat de travail peut être conclu pour une durée indéterminée ou pour une durée déterminée.

TITRE III — DES CONDITIONS DE TRAVAIL
Article 141 : La durée légale du travail est fixée à quarante heures par semaine pour toutes les entreprises.
Article 148 : Tout travailleur a droit à un repos hebdomadaire d'au moins vingt-quatre heures consécutives.

TITRE IV — DU SALAIRE
Article 207 : Le salaire minimum interprofessionnel garanti (SMIG) est fixé par décret pris en Conseil des ministres après avis de la Commission nationale du travail."""
    },
    {
        "titre": "Code foncier et domanial de la République du Bénin",
        "nature": "Code",
        "categorie": "Droit foncier",
        "numero": "2013-01",
        "date": "2013",
        "contenu": """Loi n°2013-01 du 14 janvier 2013 portant Code foncier et domanial en République du Bénin.

TITRE PREMIER — DES PRINCIPES GÉNÉRAUX
Article 1 : Le présent code régit la propriété foncière, les droits réels immobiliers et le domaine de l'État et des collectivités territoriales en République du Bénin.
Article 3 : La propriété foncière est le droit de jouir et de disposer d'une terre de manière exclusive et absolue, sous les restrictions établies par la loi.

TITRE II — DES DROITS FONCIERS
Article 15 : Toute personne physique ou morale peut acquérir des droits fonciers au Bénin, sous réserve des restrictions prévues par la loi.
Article 22 : Le certificat foncier est le document qui constate la détention paisible et publique d'une parcelle de terre par une personne.

TITRE III — DU DOMAINE DE L'ÉTAT
Article 98 : Le domaine de l'État comprend le domaine public et le domaine privé.
Article 99 : Le domaine public de l'État est constitué de tous les biens affectés à l'usage du public ou à un service public.

TITRE IV — DU RÉGIME DES TERRES RURALES
Article 154 : Les terres rurales sont régies par les droits fonciers locaux reconnus et sécurisés par le présent code."""
    },
    {
        "titre": "Code du numérique de la République du Bénin",
        "nature": "Code",
        "categorie": "Droit numérique",
        "numero": "2017-20",
        "date": "2017",
        "contenu": """Loi n°2017-20 du 20 avril 2018 portant Code du numérique en République du Bénin.

TITRE PREMIER — DISPOSITIONS GÉNÉRALES
Article 1 : Le présent code fixe le cadre juridique applicable aux activités numériques en République du Bénin.
Article 2 : Les dispositions du présent code s'appliquent à toute personne physique ou morale qui utilise, fournit ou exploite des services numériques sur le territoire béninois.

TITRE II — DES COMMUNICATIONS ÉLECTRONIQUES
Article 20 : Les opérateurs de réseaux de communications électroniques sont soumis à un régime d'autorisation délivré par l'Autorité de régulation des communications électroniques et de la poste (ARCEP).

TITRE III — DU COMMERCE ÉLECTRONIQUE
Article 85 : Toute offre de biens ou services faite par voie électronique doit comporter certaines mentions obligatoires permettant l'identification du prestataire.
Article 90 : Le contrat électronique est conclu dès lors que le destinataire de l'offre a envoyé son acceptation.

TITRE IV — DE LA PROTECTION DES DONNÉES PERSONNELLES
Article 120 : Toute personne physique dispose d'un droit d'accès, de rectification et de suppression des données personnelles la concernant.
Article 125 : Le traitement des données sensibles est interdit sauf exceptions prévues par la loi."""
    },
    {
        "titre": "Code de procédure pénale de la République du Bénin",
        "nature": "Code",
        "categorie": "Droit pénal",
        "numero": "2012-15",
        "date": "2012",
        "contenu": """Loi n°2012-15 du 18 mars 2013 portant Code de procédure pénale en République du Bénin.

TITRE PREMIER — DE L'ACTION PUBLIQUE ET DE L'ACTION CIVILE
Article 1 : L'action publique pour l'application des peines est mise en mouvement et exercée par les magistrats ou fonctionnaires auxquels elle est confiée par la loi.
Article 2 : L'action civile en réparation du dommage causé par un crime, un délit ou une contravention appartient à tous ceux qui ont personnellement souffert du dommage.

TITRE II — DE LA POLICE JUDICIAIRE
Article 14 : La police judiciaire est exercée sous la direction du procureur de la République par les officiers de police judiciaire.
Article 16 : Sont officiers de police judiciaire : les officiers et sous-officiers de la police nationale et de la gendarmerie nationale ayant la qualité d'OPJ.

TITRE III — DES JURIDICTIONS D'INSTRUCTION
Article 68 : Le juge d'instruction ne peut informer qu'en vertu d'un réquisitoire du procureur de la République.
Article 100 : Le juge d'instruction peut décerner un mandat de comparution, un mandat d'amener ou un mandat d'arrêt.

TITRE IV — DES JURIDICTIONS DE JUGEMENT
Article 190 : Le tribunal de première instance connaît de tous les délits et contraventions."""
    },
    {
        "titre": "Loi organique sur la Cour constitutionnelle",
        "nature": "Loi organique",
        "categorie": "Droit constitutionnel",
        "numero": "91-009",
        "date": "1991",
        "contenu": """Loi n°91-009 du 04 mars 1991 portant loi organique sur la Cour constitutionnelle, modifiée par la loi n°2019-43 du 15 novembre 2019.

TITRE PREMIER — DE L'ORGANISATION DE LA COUR CONSTITUTIONNELLE
Article 1 : La Cour constitutionnelle est la plus haute juridiction de l'État en matière constitutionnelle. Elle est juge de la constitutionnalité de la loi et garantit les droits fondamentaux de la personne humaine et les libertés publiques.
Article 2 : La Cour constitutionnelle est composée de sept membres dont quatre nommés par le Bureau de l'Assemblée Nationale et trois par le Président de la République pour un mandat de cinq ans renouvelable une seule fois.

TITRE II — DES ATTRIBUTIONS DE LA COUR
Article 22 : La Cour constitutionnelle statue obligatoirement sur la constitutionnalité des lois organiques avant leur promulgation.
Article 23 : La Cour constitutionnelle reçoit le serment du Président de la République et constate les résultats des élections présidentielles.

TITRE III — DE LA PROCÉDURE
Article 40 : Les décisions de la Cour constitutionnelle ne sont susceptibles d'aucun recours. Elles s'imposent aux pouvoirs publics et à toutes les autorités civiles, militaires et juridictionnelles."""
    },
    {
        "titre": "Loi organique sur la Cour suprême",
        "nature": "Loi organique",
        "categorie": "Droit constitutionnel",
        "numero": "2004-07",
        "date": "2004",
        "contenu": """Loi n°2004-07 du 23 octobre 2007 portant composition, organisation, fonctionnement et attributions de la Cour suprême.

TITRE PREMIER — DE LA COMPOSITION ET DE L'ORGANISATION
Article 1 : La Cour suprême est la plus haute juridiction de l'État en matière judiciaire et administrative. Elle assure l'unité de la jurisprudence nationale.
Article 3 : La Cour suprême comprend : la Chambre judiciaire, la Chambre administrative et la Chambre des comptes.
Article 5 : Les membres de la Cour suprême sont nommés par le Président de la République sur proposition du ministre de la Justice après avis du Conseil supérieur de la magistrature.

TITRE II — DES ATTRIBUTIONS
Article 20 : La Chambre judiciaire connaît des pourvois en cassation formés contre les décisions rendues en dernier ressort par les juridictions civiles, commerciales et pénales.
Article 35 : La Chambre administrative statue sur les recours en annulation pour excès de pouvoir formés contre les actes administratifs.
Article 48 : La Chambre des comptes assure le contrôle et le jugement des comptes publics.

TITRE III — DE LA PROCÉDURE
Article 60 : Le délai de pourvoi en cassation est de deux mois à compter de la signification de la décision attaquée."""
    }
]

# Insertion dans la base
inseres = 0
for loi in lois:
    # Vérifier si le texte existe déjà (par numéro)
    existant = curseur.execute(
        "SELECT id FROM textes WHERE numero = ?", (loi["numero"],)
    ).fetchone()

    if not existant:
        curseur.execute(
            """
            INSERT INTO textes (titre, nature, categorie, numero, date, contenu, pdf)
            VALUES (?, ?, ?, ?, ?, ?, NULL)
            """,
            (loi["titre"], loi["nature"], loi["categorie"],
             loi["numero"], loi["date"], loi["contenu"])
        )
        inseres += 1
        print(f"✅ Inséré : {loi['titre']}")
    else:
        print(f"⚠️  Déjà existant : {loi['titre']}")

connexion.commit()
connexion.close()

print(f"\n{inseres} loi(s) insérée(s) avec succès.")

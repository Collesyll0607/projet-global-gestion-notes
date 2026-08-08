"""
=============================================================================
PROJET GLOBAL : Générateur du Jeu de Données Officiel (360 Étudiants, 4 Ans)
Génère les fichiers CSV et SQLite d'alimentation d'après le PowerPoint du Groupe 1
  - 360 Étudiants
  - 4 Années Académiques (2022-2023, 2023-2024, 2024-2025, 2025-2026) -> 8 Semestres
  - 1347 Évaluations & Compositions
  - 12 Matières & 10 Professeurs
=============================================================================
"""

import pandas as pd
import numpy as np
import random
import datetime
import os
import sqlite3

def generate_full_dataset():
    random.seed(42)
    np.random.seed(42)
    
    print("=== [1/4] Génération des Filières et Niveaux ===")
    filieres = [
        {"id_filiere": 1, "nom_filiere": "Data Engineering"},
        {"id_filiere": 2, "nom_filiere": "Génie Logiciel"},
        {"id_filiere": 3, "nom_filiere": "Intelligence Artificielle"},
        {"id_filiere": 4, "nom_filiere": "Cybersécurité"}
    ]
    
    niveaux = [
        {"id_niveau": 1, "nom_niveau": "Licence 1"},
        {"id_niveau": 2, "nom_niveau": "Licence 2"},
        {"id_niveau": 3, "nom_niveau": "Licence 3"},
        {"id_niveau": 4, "nom_niveau": "Master 1"},
        {"id_niveau": 5, "nom_niveau": "Master 2"}
    ]

    print("=== [2/4] Génération des 10 Professeurs et 12 Matières ===")
    professeurs = [
        {"id_prof": 101, "nom": "Diallo", "prenom": "Mamadou", "departement": "Big Data & Cloud", "genre": "Masculin", "email": "mamadou.diallo@univ.sn"},
        {"id_prof": 102, "nom": "Sow", "prenom": "Aïssatou", "departement": "Intelligence Artificielle", "genre": "Féminin", "email": "aissatou.sow@univ.sn"},
        {"id_prof": 103, "nom": "Ndiaye", "prenom": "Cheikh", "departement": "Génie Logiciel", "genre": "Masculin", "email": "cheikh.ndiaye@univ.sn"},
        {"id_prof": 104, "nom": "Diop", "prenom": "Fatou", "departement": "Base de Données", "genre": "Féminin", "email": "fatou.diop@univ.sn"},
        {"id_prof": 105, "nom": "Faye", "prenom": "Ousmane", "departement": "Cybersécurité", "genre": "Masculin", "email": "ousmane.faye@univ.sn"},
        {"id_prof": 106, "nom": "Kane", "prenom": "Babacar", "departement": "Statistiques & Data", "genre": "Masculin", "email": "babacar.kane@univ.sn"},
        {"id_prof": 107, "nom": "Cissé", "prenom": "Aminata", "departement": "Génie Logiciel", "genre": "Féminin", "email": "aminata.cisse@univ.sn"},
        {"id_prof": 108, "nom": "Seck", "prenom": "Moussa", "departement": "Big Data & Cloud", "genre": "Masculin", "email": "moussa.seck@univ.sn"},
        {"id_prof": 109, "nom": "Ba", "prenom": "Mariama", "departement": "Base de Données", "genre": "Féminin", "email": "mariama.ba@univ.sn"},
        {"id_prof": 110, "nom": "Gaye", "prenom": "Ibrahima", "departement": "Intelligence Artificielle", "genre": "Masculin", "email": "ibrahima.gaye@univ.sn"}
    ]

    matieres = [
        {"id_matiere": 201, "nom_matiere": "Bases de Données Relationnelles (SQL)", "coefficient": 4.0},
        {"id_matiere": 202, "nom_matiere": "Bases de Données NoSQL (MongoDB)", "coefficient": 3.0},
        {"id_matiere": 203, "nom_matiere": "Big Data & Hadoop/Spark", "coefficient": 4.0},
        {"id_matiere": 204, "nom_matiere": "Algorithmique & Python Advanced", "coefficient": 3.5},
        {"id_matiere": 205, "nom_matiere": "Data Warehousing & ETL (SSIS)", "coefficient": 4.0},
        {"id_matiere": 206, "nom_matiere": "Machine Learning & Deep Learning", "coefficient": 4.0},
        {"id_matiere": 207, "nom_matiere": "Architecture Microservices & Cloud", "coefficient": 3.0},
        {"id_matiere": 208, "nom_matiere": "Sécurité des Systèmes d'Information", "coefficient": 3.0},
        {"id_matiere": 209, "nom_matiere": "Statistiques Inférentielles", "coefficient": 3.0},
        {"id_matiere": 210, "nom_matiere": "Business Intelligence & Power BI", "coefficient": 3.5},
        {"id_matiere": 211, "nom_matiere": "DevOps & Docker/Kubernetes", "coefficient": 3.0},
        {"id_matiere": 212, "nom_matiere": "Gouvernance des Données & DPO", "coefficient": 2.5}
    ]

    print("=== [3/4] Génération des 360 Étudiants ===")
    noms_senegal = ["Fall", "Ba", "Gaye", "Cissé", "Sarr", "Seck", "Kane", "Sy", "Camara", "Mendy", "Diallo", "Ndiaye", "Diop", "Faye", "Sow", "Touré", "Samb", "Badji", "Badiane", "Dramé"]
    prenoms_senegal = ["Ibrahima", "Aminata", "Moussa", "Mariama", "Modou", "Khadija", "Babacar", "Oumar", "Awa", "Jean", "Fatou", "Cheikh", "Mamadou", "Aïssatou", "Abdoulaye", "Binta", "Pape", "Rokhaya", "Saliou", "Adama"]
    villes = ["Dakar", "Thiès", "Saint-Louis", "Ziguinchor", "Rufisque", "Kaolack", "Mbour", "Touba"]

    etudiants = []
    student_id = 1001
    for i in range(360):
        nom = random.choice(noms_senegal)
        prenom = random.choice(prenoms_senegal)
        filiere = random.choice(filieres)
        niveau = random.choice(niveaux)
        annee_birth = random.randint(1998, 2005)
        month_birth = random.randint(1, 12)
        day_birth = random.randint(1, 28)
        dob = f"{annee_birth:04d}-{month_birth:02d}-{day_birth:02d}"
        email = f"{prenom.lower()}.{nom.lower()}{i+1}@student.sn"
        adresse = f"{random.choice(villes)}, Quartier {random.randint(1, 15)}"
        
        etudiants.append({
            "id_etudiant": student_id,
            "nom": nom,
            "prenom": prenom,
            "date_naissance": dob,
            "email": email,
            "adresse": adresse,
            "id_niveau": niveau["id_niveau"],
            "id_filiere": filiere["id_filiere"],
            "nom_filiere": filiere["nom_filiere"],
            "nom_niveau": niveau["nom_niveau"]
        })
        student_id += 1

    print("=== [4/4] Génération des 1347 Compositions & Évaluations sur 4 Années (8 Semestres) ===")
    dates_evaluations = [
        ("2022-2023", "S1", "2023-01-15"),
        ("2022-2023", "S2", "2023-06-20"),
        ("2023-2024", "S1", "2024-01-15"),
        ("2023-2024", "S2", "2024-06-20"),
        ("2024-2025", "S1", "2025-01-15"),
        ("2024-2025", "S2", "2025-06-20"),
        ("2025-2026", "S1", "2026-01-15"),
        ("2025-2026", "S2", "2026-06-20")
    ]

    compositions = []
    target_count = 1347
    eval_id = 1
    
    # Génération distribuée des 1347 enregistrements
    while len(compositions) < target_count:
        etud = random.choice(etudiants)
        mat = random.choice(matieres)
        annee_acad, sem, d_eval = random.choice(dates_evaluations)
        
        # Éviter les doublons exacts (id_etudiant, id_matiere, annee_academique, semestre)
        pair_key = (etud["id_etudiant"], mat["id_matiere"], annee_acad, sem)
        if any(c["id_etudiant"] == etud["id_etudiant"] and c["id_matiere"] == mat["id_matiere"] and c["annee_academique"] == annee_acad and c["semestre"] == sem for c in compositions):
            continue
            
        # Distribution réaliste des notes (moyenne autour de 13.5, min 4, max 20)
        note = round(min(20.0, max(4.0, np.random.normal(13.8, 3.2))), 2)
        prof = random.choice(professeurs)

        compositions.append({
            "eval_id": eval_id,
            "id_etudiant": etud["id_etudiant"],
            "nom_etudiant": f"{etud['prenom']} {etud['nom']}",
            "filiere": etud["nom_filiere"],
            "niveau": etud["nom_niveau"],
            "id_matiere": mat["id_matiere"],
            "nom_matiere": mat["nom_matiere"],
            "coefficient": mat["coefficient"],
            "id_prof": prof["id_prof"],
            "nom_prof": f"{prof['prenom']} {prof['nom']}",
            "note": note,
            "annee_academique": annee_acad,
            "semestre": sem,
            "date_evaluation": d_eval
        })
        eval_id += 1

    print(f"   [OK] Généré : {len(etudiants)} Étudiants | {len(compositions)} Compositions | {len(professeurs)} Professeurs | {len(matieres)} Matières")

    # Export des datasets CSV & JSON
    base_dir = os.path.dirname(__file__)
    dataset_dir = os.path.join(base_dir, "dataset")
    os.makedirs(dataset_dir, exist_ok=True)
    
    df_etudiants = pd.DataFrame(etudiants)
    df_compositions = pd.DataFrame(compositions)
    df_matieres = pd.DataFrame(matieres)
    df_professeurs = pd.DataFrame(professeurs)

    df_etudiants.to_csv(os.path.join(dataset_dir, "etudiants_360.csv"), index=False, encoding="utf-8")
    df_compositions.to_csv(os.path.join(dataset_dir, "compositions_1347.csv"), index=False, encoding="utf-8")
    df_matieres.to_csv(os.path.join(dataset_dir, "matieres_12.csv"), index=False, encoding="utf-8")
    df_professeurs.to_csv(os.path.join(dataset_dir, "professeurs_10.csv"), index=False, encoding="utf-8")

    print(f"=== [Export CSV Terminé dans {dataset_dir}] ===")

if __name__ == "__main__":
    generate_full_dataset()

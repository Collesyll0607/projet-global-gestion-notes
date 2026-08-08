"""
=============================================================================
PROJET GLOBAL : Pipeline ETL (Extract, Transform, Load) en Python
Alimentation du Data Warehouse avec le jeu de données officiel du Groupe 1 :
  - 360 Étudiants
  - 1347 Compositions sur 4 Années Académiques (8 Semestres)
  - 12 Matières & 10 Professeurs
=============================================================================
"""

import pandas as pd
import sqlite3
import datetime
import os

def run_etl():
    print("=== DÉBUT DU PIPELINE ETL : DATASET (360 ÉTUDIANTS / 1347 EVALS) -> DATA WAREHOUSE ===")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)
    dataset_dir = os.path.join(project_dir, "dataset")
    
    # Vérification et génération si besoin
    if not os.path.exists(os.path.join(dataset_dir, "etudiants_360.csv")):
        from generate_dataset import generate_full_dataset
        generate_full_dataset()
        
    df_etudiants = pd.read_csv(os.path.join(dataset_dir, "etudiants_360.csv"))
    df_compositions = pd.read_csv(os.path.join(dataset_dir, "compositions_1347.csv"))
    df_matieres = pd.read_csv(os.path.join(dataset_dir, "matieres_12.csv"))
    df_professeurs = pd.read_csv(os.path.join(dataset_dir, "professeurs_10.csv"))
    
    dw_db_path = os.path.join(base_dir, "data_warehouse.db")
    conn_dw = sqlite3.connect(dw_db_path)
    cursor_dw = conn_dw.cursor()
    
    # 1. Chargement des schémas DW si pas créés
    star_schema_path = os.path.join(base_dir, "01_star_schema.sql")
    with open(star_schema_path, "r", encoding="utf-8") as f:
        cursor_dw.executescript(f.read())
        
    print("[1/4] Chargement des Dimensions (360 Étudiants, 12 Matières, 10 Profs)...")
    
    # Dim_Filiere
    filieres_unique = df_etudiants[["id_filiere", "nom_filiere"]].drop_duplicates()
    for _, row in filieres_unique.iterrows():
        cursor_dw.execute("INSERT OR REPLACE INTO Dim_Filiere (sk_filiere, id_filiere_source, nom_filiere) VALUES (?, ?, ?)",
                          (int(row['id_filiere']), int(row['id_filiere']), row['nom_filiere']))
        
    # Dim_Niveau
    niveaux_unique = df_etudiants[["id_niveau", "nom_niveau"]].drop_duplicates()
    for _, row in niveaux_unique.iterrows():
        cursor_dw.execute("INSERT OR REPLACE INTO Dim_Niveau (sk_niveau, id_niveau_source, nom_niveau) VALUES (?, ?, ?)",
                          (int(row['id_niveau']), int(row['id_niveau']), row['nom_niveau']))
        
    # Dim_Etudiant (360 Étudiants)
    for _, row in df_etudiants.iterrows():
        nom_complet = f"{row['prenom']} {row['nom']}"
        cursor_dw.execute("INSERT OR REPLACE INTO Dim_Etudiant (sk_etudiant, id_etudiant_source, nom, prenom, nom_complet, email, tranche_age) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (int(row['id_etudiant']), int(row['id_etudiant']), row['nom'], row['prenom'], nom_complet, row['email'], "20-25 ans"))

    # Dim_Matiere (12 Matières)
    for _, row in df_matieres.iterrows():
        cursor_dw.execute("INSERT OR REPLACE INTO Dim_Matiere (sk_matiere, id_matiere_source, nom_matiere, coefficient) VALUES (?, ?, ?, ?)",
                          (int(row['id_matiere']), int(row['id_matiere']), row['nom_matiere'], float(row['coefficient'])))

    # Dim_Professeur (10 Professeurs)
    for _, row in df_professeurs.iterrows():
        nom_complet_prof = f"{row['prenom']} {row['nom']}"
        cursor_dw.execute("INSERT OR REPLACE INTO Dim_Professeur (sk_professeur, id_prof_source, nom_complet_prof, departement, genre) VALUES (?, ?, ?, ?, ?)",
                          (int(row['id_prof']), int(row['id_prof']), nom_complet_prof, row['departement'], row['genre']))

    print("[2/4] Génération de la Dimension Temps (8 Périodes / 4 Années Académiques)...")
    dates_eval = df_compositions["date_evaluation"].unique()
    for d_str in dates_eval:
        dt = datetime.datetime.strptime(d_str, "%Y-%m-%d")
        sk_temps = int(dt.strftime("%Y%m%d"))
        cursor_dw.execute("""
            INSERT OR REPLACE INTO Dim_Temps (sk_temps, date_complete, annee, semestre, trimestre, mois, nom_mois, jour, jour_semaine)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sk_temps, d_str, dt.year, 1 if dt.month <= 6 else 2, 1 if dt.month <= 3 else (2 if dt.month <= 6 else 3), dt.month, dt.strftime("%B"), dt.day, dt.strftime("%A")))

    print("[3/4] Transposition et Chargement de 1347 Faits dans Fact_Composition...")
    fact_id = 1
    for _, row in df_compositions.iterrows():
        sk_etudiant = int(row['id_etudiant'])
        sk_matiere = int(row['id_matiere'])
        
        # Lookups
        etud_info = df_etudiants[df_etudiants['id_etudiant'] == sk_etudiant].iloc[0]
        sk_filiere = int(etud_info['id_filiere'])
        sk_niveau = int(etud_info['id_niveau'])
        sk_professeur = int(row['id_prof'])
        
        date_str = str(row['date_evaluation'])
        sk_temps = int(datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d"))
        
        note = float(row['note'])
        coeff = float(row['coefficient'])
        note_ponderee = round(note * coeff, 2)
        est_admis = 1 if note >= 10.0 else 0
        points_manquants = round(max(0.0, 10.0 - note), 2)
        
        cursor_dw.execute("""
            INSERT OR REPLACE INTO Fact_Composition (
                fact_id, sk_etudiant, sk_matiere, sk_filiere, sk_niveau, sk_professeur, sk_temps,
                note, coefficient, note_ponderee, est_admis, points_manquants_admissibilite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fact_id, sk_etudiant, sk_matiere, sk_filiere, sk_niveau, sk_professeur, sk_temps,
              note, coeff, note_ponderee, est_admis, points_manquants))
        fact_id += 1

    conn_dw.commit()
    conn_dw.close()
    
    print(f"=== [ETL SUCCÈS] {fact_id - 1} Évaluations chargées dans le Data Warehouse (data_warehouse.db) ! ===")

if __name__ == "__main__":
    run_etl()

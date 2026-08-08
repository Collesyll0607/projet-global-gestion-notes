"""
=============================================================================
PROJET GLOBAL : Script Orchestrateur Master Tout-En-Un (End-to-End Pipeline)
Exécution : python run_project_global_master_pipeline.py

Ce script exécute l'ensemble de la chaîne en 1 seul clic :
  1. Chargement/Initialisation de la base SQL relationnelle
  2. Exécution du pipeline ETL (Extraction -> DW Fact_Composition)
  3. Lancement automatique du Tableau de Bord Pédagogique Streamlit !
=============================================================================
"""

import os
import subprocess
import sqlite3
import sys

def main():
    print("=================================================================")
    print("  EXECUTION DU PIPELINE MAITRE TOUT-EN-UN (PROJET GLOBAL)       ")
    print("=================================================================")
    
    base_dir = os.path.dirname(__file__)
    
    # 1. Initialisation SQL
    print("\n[ETAPE 1/3] Initialisation de la Base de Donnees SQL Relationnelle...")
    schema_sql = os.path.join(base_dir, "sql", "01_schema_sql.sql")
    data_sql = os.path.join(base_dir, "sql", "02_data_loading.sql")
    oltp_db = os.path.join(base_dir, "data_warehouse", "oltp_source.db")
    
    conn = sqlite3.connect(oltp_db)
    cursor = conn.cursor()
    with open(schema_sql, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    with open(data_sql, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()
    print("   [OK] Base SQL chargee avec succes (Tables: Appartenance, Composition, Suivie, Enseignement).")
    
    # 2. Pipeline ETL Data Warehouse
    print("\n[ETAPE 2/3] Execution du Pipeline ETL vers le Data Warehouse...")
    etl_script = os.path.join(base_dir, "data_warehouse", "02_etl_pipeline.py")
    subprocess.run([sys.executable, etl_script])
    
    # 3. Lancement Dashboard Streamlit
    print("\n[ETAPE 3/3] Lancement du Tableau de Bord Streamlit Pedagogique...")
    dashboard_script = os.path.join(base_dir, "dashboard", "app_streamlit.py")
    cmd = f"\"{sys.executable}\" -m streamlit run \"{dashboard_script}\""
    
    print("\n=================================================================")
    print("      PIPELINE GLOBAL TERMINE AVEC SUCCES ! OUVERTURE STREAMLIT...")
    print("=================================================================")
    
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\nArret du tableau de bord.")

if __name__ == "__main__":
    main()

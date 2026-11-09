> 🌐 **Démo Interactive Déployée en Ligne :** [**https://collesyll0607.github.io/projet-global-gestion-notes/**](https://collesyll0607.github.io/projet-global-gestion-notes/)
>
> 👩‍💻 **Portfolio de l'Auteure (Collé Syll) :** [https://collesyll0607.github.io/](https://collesyll0607.github.io/)

---

# 🎓 Projet Global : Système Décisionnel de Gestion des Notes des Étudiants

[![GitHub User](https://img.shields.io/badge/GitHub-Collesyll0607-blue?logo=github)](https://github.com/Collesyll0607)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%2FSQL-green?logo=sqlite)](https://sqlite.org/)

---

## 📌 Présentation du Projet
Système d'information décisionnel complet de gestion des notes et performances académiques des étudiants.
Conçu d'après le **Modèle Logique de Données (MLD)** officiel et validé pour une volumétrie de **360 Étudiants**, **4 Années Académiques (8 Semestres)** et **1347 Évaluations**.

---

## 🏛️ Architecture & Modélisation

- **Diagrammes Draw.io** :
  - `mcd_projet_global.drawio` : Modèle Conceptuel de Données.
  - `mld_projet_global.drawio` : Modèle Logique de Données (Nomenclatures nominales).
- **Formes Nominales des Tables** : `Appartenance`, `Inscription`, `Suivie`, `Composition`, `Enseignement`.
- **Entrepôt de Données (Data Warehouse en étoile)** : Table de fait `Fact_Composition` et 6 dimensions (`Dim_Etudiant`, `Dim_Matiere`, `Dim_Filiere`, `Dim_Niveau`, `Dim_Professeur`, `Dim_Temps`).

---

## 🚀 Démarrage Rapide (1 Seule Commande)

```bash
python run_project_global_master_pipeline.py
```

Ce script exécute l'intégralité du pipeline en 1 clic :
1. Initialisation de la base SQL.
2. Exécution de l'ETL vers le Data Warehouse.
3. Ouverture du Tableau de Bord Streamlit.

---

## 👤 Auteur
- **GitHub** : [@Collesyll0607](https://github.com/Collesyll0607)


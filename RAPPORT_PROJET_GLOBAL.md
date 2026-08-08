# RAPPORT DE PROJET GLOBAL : Système Décisionnel de Gestion des Notes des Étudiants

**Discipline :** Data Engineering & Entrepôt de Données  
**Auteur :** Groupe 1 (Certification Data Engineering)  
**Taille du Jeu de Données :** 360 Étudiants, 4 Années Académiques (8 Semestres), 1347 Évaluations, 12 Matières, 10 Enseignants  
**Fichiers Schémas Draw.io :** `mcd_projet_global.drawio` et `mld_projet_global.drawio`  
**Date de Soutenance :** Février 2026  
**Statut :** Projet Complètement Finalisé  

---

## 1. Contexte et Objectifs du Projet

Ce projet a pour objectif de concevoir et de déployer un système d'information décisionnel complet dédié au suivi des performances académiques des étudiants. Le projet s'appuie sur une architecture hybride **SQL (MySQL) / NoSQL (MongoDB)**, un **Entrepôt de Données (SQL Server / Data Warehouse en schéma en étoile)** et un **Tableau de Bord web interactif Streamlit**.

### 1.1. Volumétrie Officielle du Jeu de Données
- **360 Étudiants** répartis sur 4 filières (*Data Engineering*, *Génie Logiciel*, *Intelligence Artificielle*, *Cybersécurité*).
- **4 Années Académiques** (2022-2023, 2023-2024, 2024-2025, 2025-2026) soit **8 Semestres d'évaluation (S1 & S2)**.
- **1347 Inscriptions & Compositions / Évaluations**.
- **12 Matières & 10 Enseignants**.

---

## 2. Modélisation MCD & MLD (Draw.io)

### 2.1. Noms des Tables (Formes Nominales)
Les tables et associations sont nommées selon les normes nominales :
- `Appartenance` (Nouveau nom pour Appartenir)
- `Inscription` (Association d'orientation/inscription)
- `Suivie` (Inscriptions aux modules)
- `Composition` (Table des épreuves et des notes)
- `Enseignement` (Affectations des enseignants)

---

## 3. Architecture du Pipeline ETL & Data Warehouse

```
  +------------------+         +------------------+
  | Base Source SQL  |         | Base NoSQL Mongo |
  +------------------+         +------------------+
           |                            |
           +--------------+-------------+
                          |
                          v
          +-------------------------------+
          | Pipeline ETL Python / SSIS    |
          +-------------------------------+
                          |
                          v
          +-------------------------------+
          |  Entrepôt de Données (DW)     | (Fact_Composition & 6 Dimensions)
          +-------------------------------+
                          |
                          v
          +-------------------------------+
          | Tableau de Bord Streamlit     | (360 Étudiants / 1347 Évaluations)
          +-------------------------------+
```

- **Table de Fait** : `Fact_Composition` (`fact_id`, `sk_etudiant`, `sk_matiere`, `sk_filiere`, `sk_niveau`, `sk_professeur`, `sk_temps`, `note`, `coefficient`, `note_ponderee`, `est_admis`).
- **Dimensions** : `Dim_Etudiant` (360 enregistrements), `Dim_Matiere` (12 cours), `Dim_Filiere`, `Dim_Niveau`, `Dim_Professeur` (10 enseignants), `Dim_Temps` (8 périodes académiques).
- **Pipeline ETL Python (`data_warehouse/02_etl_pipeline.py`)** : Traitement automatique d'extraction des CSV, calcul des surrogate keys et chargement dans `data_warehouse.db`.

---

## 4. Restitution sur Tableau de Bord Streamlit

- **Filtres Dynamiques** : Filtrage par Année Académique, Semestre, Filière, Niveau et barre de recherche par nom d'étudiant.
- **KPIs Pédagogiques** : Taux de réussite global, moyenne générale pondérée, nombre total d'évaluations (1347).
- **Visualisations Plotly / Streamlit** : Moyenne des notes par filière et classement des matières.
- **Classement Général** : Tableau interactif avec calcul instantané des moyennes pondérées par étudiant.

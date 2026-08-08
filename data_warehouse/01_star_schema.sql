-- =============================================================================
-- PROJET GLOBAL : Modélisation et Création du Data Warehouse (Schéma en Étoile)
-- Table de fait : Fact_Composition (Faits des notes et évaluations)
-- Compatible avec SQLite / PostgreSQL / MySQL / SQL Server
-- =============================================================================

-- Suppression préalable des tables DW
DROP TABLE IF EXISTS Fact_Composition;
DROP TABLE IF EXISTS Dim_Etudiant;
DROP TABLE IF EXISTS Dim_Matiere;
DROP TABLE IF EXISTS Dim_Filiere;
DROP TABLE IF EXISTS Dim_Niveau;
DROP TABLE IF EXISTS Dim_Professeur;
DROP TABLE IF EXISTS Dim_Temps;

-- 1. Table de Dimension : Dim_Filiere
CREATE TABLE Dim_Filiere (
    sk_filiere INT PRIMARY KEY,
    id_filiere_source INT NOT NULL,
    nom_filiere VARCHAR(100) NOT NULL
);

-- 2. Table de Dimension : Dim_Niveau
CREATE TABLE Dim_Niveau (
    sk_niveau INT PRIMARY KEY,
    id_niveau_source INT NOT NULL,
    nom_niveau VARCHAR(50) NOT NULL
);

-- 3. Table de Dimension : Dim_Etudiant
CREATE TABLE Dim_Etudiant (
    sk_etudiant INT PRIMARY KEY,
    id_etudiant_source INT NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    nom_complet VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    tranche_age VARCHAR(20)
);

-- 4. Table de Dimension : Dim_Matiere
CREATE TABLE Dim_Matiere (
    sk_matiere INT PRIMARY KEY,
    id_matiere_source INT NOT NULL,
    nom_matiere VARCHAR(100) NOT NULL,
    coefficient DECIMAL(3,1) NOT NULL
);

-- 5. Table de Dimension : Dim_Professeur
CREATE TABLE Dim_Professeur (
    sk_professeur INT PRIMARY KEY,
    id_prof_source INT NOT NULL,
    nom_complet_prof VARCHAR(100) NOT NULL,
    departement VARCHAR(100),
    genre VARCHAR(10)
);

-- 6. Table de Dimension : Dim_Temps
CREATE TABLE Dim_Temps (
    sk_temps INT PRIMARY KEY,
    date_complete DATE NOT NULL,
    annee INT NOT NULL,
    semestre INT NOT NULL,
    trimestre INT NOT NULL,
    mois INT NOT NULL,
    nom_mois VARCHAR(20) NOT NULL,
    jour INT NOT NULL,
    jour_semaine VARCHAR(20) NOT NULL
);

-- 7. Table de Fait Central : Fact_Composition
CREATE TABLE Fact_Composition (
    fact_id INT PRIMARY KEY,
    sk_etudiant INT NOT NULL,
    sk_matiere INT NOT NULL,
    sk_filiere INT NOT NULL,
    sk_niveau INT NOT NULL,
    sk_professeur INT NOT NULL,
    sk_temps INT NOT NULL,
    
    note DECIMAL(4,2) NOT NULL,
    coefficient DECIMAL(3,1) NOT NULL,
    note_ponderee DECIMAL(6,2) NOT NULL,
    est_admis INT NOT NULL,
    points_manquants_admissibilite DECIMAL(4,2) NOT NULL,

    CONSTRAINT fk_fact_etudiant FOREIGN KEY (sk_etudiant) REFERENCES Dim_Etudiant(sk_etudiant),
    CONSTRAINT fk_fact_matiere FOREIGN KEY (sk_matiere) REFERENCES Dim_Matiere(sk_matiere),
    CONSTRAINT fk_fact_filiere FOREIGN KEY (sk_filiere) REFERENCES Dim_Filiere(sk_filiere),
    CONSTRAINT fk_fact_niveau FOREIGN KEY (sk_niveau) REFERENCES Dim_Niveau(sk_niveau),
    CONSTRAINT fk_fact_professeur FOREIGN KEY (sk_professeur) REFERENCES Dim_Professeur(sk_professeur),
    CONSTRAINT fk_fact_temps FOREIGN KEY (sk_temps) REFERENCES Dim_Temps(sk_temps)
);

CREATE INDEX idx_dw_fact_etudiant ON Fact_Composition(sk_etudiant);
CREATE INDEX idx_dw_fact_matiere ON Fact_Composition(sk_matiere);
CREATE INDEX idx_dw_fact_filiere ON Fact_Composition(sk_filiere);
CREATE INDEX idx_dw_fact_niveau ON Fact_Composition(sk_niveau);
CREATE INDEX idx_dw_fact_temps ON Fact_Composition(sk_temps);

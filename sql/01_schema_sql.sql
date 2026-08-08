-- =============================================================================
-- PROJET GLOBAL : Système de Gestion des Notes des Étudiants
-- Script DDL de Création de la Base de Données SQL Relationnelle
-- Noms des tables (Formes Nominales : Appartenance, Suivie, Composition, Enseignement)
-- Compatible avec SQLite / PostgreSQL / MySQL
-- =============================================================================

-- Suppression préalable des tables si elles existent
DROP TABLE IF EXISTS Enseignement;
DROP TABLE IF EXISTS Composition;
DROP TABLE IF EXISTS Suivie;
DROP TABLE IF EXISTS Professeur;
DROP TABLE IF EXISTS Matiere;
DROP TABLE IF EXISTS Etudiant;
DROP TABLE IF EXISTS Appartenance;
DROP TABLE IF EXISTS Niveau;
DROP TABLE IF EXISTS Filiere;

-- 1. Table Filiere
CREATE TABLE Filiere (
    id_filiere INT PRIMARY KEY,
    nom_filiere VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Table Niveau
CREATE TABLE Niveau (
    id_niveau INT PRIMARY KEY,
    nom_niveau VARCHAR(50) NOT NULL UNIQUE
);

-- 3. Table Appartenance (Relation N-N entre Niveau et Filiere)
CREATE TABLE Appartenance (
    id_niveau INT NOT NULL,
    id_filiere INT NOT NULL,
    CONSTRAINT pk_appartenance PRIMARY KEY (id_niveau, id_filiere),
    CONSTRAINT fk_appartenance_niveau FOREIGN KEY (id_niveau) REFERENCES Niveau(id_niveau) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_appartenance_filiere FOREIGN KEY (id_filiere) REFERENCES Filiere(id_filiere) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 4. Table Etudiant
CREATE TABLE Etudiant (
    id_etudiant INT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    date_naissance DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    adresse VARCHAR(255),
    id_niveau INT NOT NULL,
    id_filiere INT NOT NULL,
    CONSTRAINT fk_etudiant_niveau FOREIGN KEY (id_niveau) REFERENCES Niveau(id_niveau) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_etudiant_filiere FOREIGN KEY (id_filiere) REFERENCES Filiere(id_filiere) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 5. Table Matiere
CREATE TABLE Matiere (
    id_matiere INT PRIMARY KEY,
    nom_matiere VARCHAR(100) NOT NULL UNIQUE,
    coefficient DECIMAL(3,1) NOT NULL CHECK (coefficient > 0)
);

-- 6. Table Professeur
CREATE TABLE Professeur (
    id_prof INT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    departement VARCHAR(100) NOT NULL,
    genre VARCHAR(10) CHECK (genre IN ('Masculin', 'Féminin', 'M', 'F')),
    email VARCHAR(100) UNIQUE NOT NULL
);

-- 7. Table Suivie (Inscriptions des étudiants aux matières)
CREATE TABLE Suivie (
    id_etudiant INT NOT NULL,
    id_matiere INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    CONSTRAINT pk_suivie PRIMARY KEY (id_etudiant, id_matiere),
    CONSTRAINT fk_suivie_etudiant FOREIGN KEY (id_etudiant) REFERENCES Etudiant(id_etudiant) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_suivie_matiere FOREIGN KEY (id_matiere) REFERENCES Matiere(id_matiere) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 8. Table Composition (Notes obtenues par les étudiants dans les matières)
CREATE TABLE Composition (
    id_etudiant INT NOT NULL,
    id_matiere INT NOT NULL,
    note DECIMAL(4,2) NOT NULL CHECK (note >= 0.00 AND note <= 20.00),
    date_debut DATE NOT NULL,
    date_fin DATE,
    CONSTRAINT pk_composition PRIMARY KEY (id_etudiant, id_matiere),
    CONSTRAINT fk_composition_etudiant FOREIGN KEY (id_etudiant) REFERENCES Etudiant(id_etudiant) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_composition_matiere FOREIGN KEY (id_matiere) REFERENCES Matiere(id_matiere) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 9. Table Enseignement (Attribution des cours aux professeurs par niveau)
CREATE TABLE Enseignement (
    id_niveau INT NOT NULL,
    id_matiere INT NOT NULL,
    id_prof INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    CONSTRAINT pk_enseignement PRIMARY KEY (id_niveau, id_matiere, id_prof),
    CONSTRAINT fk_enseignement_niveau FOREIGN KEY (id_niveau) REFERENCES Niveau(id_niveau) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_enseignement_matiere FOREIGN KEY (id_matiere) REFERENCES Matiere(id_matiere) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_enseignement_prof FOREIGN KEY (id_prof) REFERENCES Professeur(id_prof) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Index pour optimiser les performances des requêtes décisionnelles
CREATE INDEX idx_etudiant_filiere_niveau ON Etudiant(id_filiere, id_niveau);
CREATE INDEX idx_composition_note ON Composition(note);
CREATE INDEX idx_enseignement_prof ON Enseignement(id_prof);

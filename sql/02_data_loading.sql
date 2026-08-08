-- =============================================================================
-- PROJET GLOBAL : Chargement des données (SQL DML)
-- Noms des tables révisés (Formes Nominales : Appartenance, Suivie, Composition, Enseignement)
-- =============================================================================

-- 1. Insertion dans Filiere
INSERT INTO Filiere (id_filiere, nom_filiere) VALUES
(1, 'Data Engineering'),
(2, 'Génie Logiciel'),
(3, 'Intelligence Artificielle'),
(4, 'Cybersécurité');

-- 2. Insertion dans Niveau
INSERT INTO Niveau (id_niveau, nom_niveau) VALUES
(1, 'Licence 1'),
(2, 'Licence 2'),
(3, 'Licence 3'),
(4, 'Master 1'),
(5, 'Master 2');

-- 3. Insertion dans Appartenance
INSERT INTO Appartenance (id_niveau, id_filiere) VALUES
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
(1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
(3, 3), (4, 3), (5, 3),
(3, 4), (4, 4), (5, 4);

-- 4. Insertion dans Professeur
INSERT INTO Professeur (id_prof, nom, prenom, departement, genre, email) VALUES
(101, 'Diallo', 'Mamadou', 'Informatique & Big Data', 'M', 'mamadou.diallo@univ-edu.sn'),
(102, 'Sow', 'Aïssatou', 'Intelligence Artificielle', 'F', 'aissatou.sow@univ-edu.sn'),
(103, 'Ndiaye', 'Cheikh', 'Génie Logiciel', 'M', 'cheikh.ndiaye@univ-edu.sn'),
(104, 'Diop', 'Fatou', 'Base de Données & Data', 'F', 'fatou.diop@univ-edu.sn'),
(105, 'Faye', 'Ousmane', 'Cybersécurité & Réseaux', 'M', 'ousmane.faye@univ-edu.sn');

-- 5. Insertion dans Matiere
INSERT INTO Matiere (id_matiere, nom_matiere, coefficient) VALUES
(201, 'Bases de Données Relationnelles (SQL)', 4.0),
(202, 'Bases de Données NoSQL (MongoDB)', 3.0),
(203, 'Big Data & Hadoop/Spark', 4.0),
(204, 'Algorithmique & Python', 3.5),
(205, 'Data Warehousing & ETL', 4.0),
(206, 'Machine Learning & Deep Learning', 4.0),
(207, 'Architecture Microservices', 3.0),
(208, 'Sécurité des SI', 3.0);

-- 6. Insertion dans Etudiant
INSERT INTO Etudiant (id_etudiant, nom, prenom, date_naissance, email, adresse, id_niveau, id_filiere) VALUES
(1001, 'Fall', 'Ibrahima', '2001-03-15', 'ibrahima.fall@student.sn', 'Dakar, Plateau', 4, 1),
(1002, 'Ba', 'Aminata', '2002-07-22', 'aminata.ba@student.sn', 'Dakar, Mermoz', 4, 1),
(1003, 'Gaye', 'Moussa', '2000-11-10', 'moussa.gaye@student.sn', 'Thiès, Center', 5, 1),
(1004, 'Cissé', 'Mariama', '2002-01-05', 'mariama.cisse@student.sn', 'Dakar, Almadies', 3, 2),
(1005, 'Sarr', 'Modou', '2001-09-18', 'modou.sarr@student.sn', 'Saint-Louis', 4, 2),
(1006, 'Seck', 'Khadija', '2003-04-12', 'khadija.seck@student.sn', 'Dakar, Ouakam', 4, 3),
(1007, 'Kane', 'Babacar', '2000-08-30', 'babacar.kane@student.sn', 'Dakar, Yoff', 5, 3),
(1008, 'Sy', 'Oumar', '2002-12-01', 'oumar.sy@student.sn', 'Rufisque', 3, 4),
(1009, 'Camara', 'Awa', '2001-06-14', 'awa.camara@student.sn', 'Dakar, Fann', 4, 1),
(1010, 'Mendy', 'Jean', '2002-02-28', 'jean.mendy@student.sn', 'Ziguinchor', 3, 2);

-- 7. Insertion dans Enseignement
INSERT INTO Enseignement (id_niveau, id_matiere, id_prof, date_debut, date_fin) VALUES
(4, 201, 104, '2025-10-01', '2026-02-15'),
(4, 202, 104, '2025-10-01', '2026-02-15'),
(4, 203, 101, '2025-10-01', '2026-02-15'),
(4, 205, 101, '2025-10-01', '2026-02-15'),
(3, 204, 102, '2025-10-01', '2026-02-15'),
(5, 206, 102, '2025-10-01', '2026-02-15'),
(3, 207, 103, '2025-10-01', '2026-02-15'),
(4, 207, 103, '2025-10-01', '2026-02-15'),
(3, 208, 105, '2025-10-01', '2026-02-15');

-- 8. Insertion dans Suivie
INSERT INTO Suivie (id_etudiant, id_matiere, date_debut, date_fin) VALUES
(1001, 201, '2025-10-01', '2026-02-15'),
(1001, 202, '2025-10-01', '2026-02-15'),
(1001, 203, '2025-10-01', '2026-02-15'),
(1001, 205, '2025-10-01', '2026-02-15'),

(1002, 201, '2025-10-01', '2026-02-15'),
(1002, 202, '2025-10-01', '2026-02-15'),
(1002, 203, '2025-10-01', '2026-02-15'),
(1002, 205, '2025-10-01', '2026-02-15'),

(1003, 203, '2025-10-01', '2026-02-15'),
(1003, 205, '2025-10-01', '2026-02-15'),
(1003, 206, '2025-10-01', '2026-02-15'),

(1004, 204, '2025-10-01', '2026-02-15'),
(1004, 207, '2025-10-01', '2026-02-15'),

(1005, 201, '2025-10-01', '2026-02-15'),
(1005, 207, '2025-10-01', '2026-02-15'),

(1006, 204, '2025-10-01', '2026-02-15'),
(1006, 206, '2025-10-01', '2026-02-15'),

(1007, 206, '2025-10-01', '2026-02-15'),

(1008, 208, '2025-10-01', '2026-02-15'),

(1009, 201, '2025-10-01', '2026-02-15'),
(1009, 202, '2025-10-01', '2026-02-15'),
(1009, 203, '2025-10-01', '2026-02-15'),

(1010, 204, '2025-10-01', '2026-02-15');

-- 9. Insertion dans Composition
INSERT INTO Composition (id_etudiant, id_matiere, note, date_debut, date_fin) VALUES
(1001, 201, 16.50, '2026-01-10', '2026-01-10'),
(1001, 202, 17.00, '2026-01-12', '2026-01-12'),
(1001, 203, 15.50, '2026-01-15', '2026-01-15'),
(1001, 205, 18.00, '2026-01-20', '2026-01-20'),

(1002, 201, 14.00, '2026-01-10', '2026-01-10'),
(1002, 202, 15.50, '2026-01-12', '2026-01-12'),
(1002, 203, 13.00, '2026-01-15', '2026-01-15'),
(1002, 205, 16.00, '2026-01-20', '2026-01-20'),

(1003, 203, 18.50, '2026-01-15', '2026-01-15'),
(1003, 205, 19.00, '2026-01-20', '2026-01-20'),
(1003, 206, 17.50, '2026-01-22', '2026-01-22'),

(1004, 204, 12.00, '2026-01-11', '2026-01-11'),
(1004, 207, 11.50, '2026-01-18', '2026-01-18'),

(1005, 201, 09.50, '2026-01-10', '2026-01-10'),
(1005, 207, 13.00, '2026-01-18', '2026-01-18'),

(1006, 204, 16.00, '2026-01-11', '2026-01-11'),
(1006, 206, 15.00, '2026-01-22', '2026-01-22'),

(1007, 206, 17.00, '2026-01-22', '2026-01-22'),

(1008, 208, 14.50, '2026-01-19', '2026-01-19'),

(1009, 201, 11.00, '2026-01-10', '2026-01-10'),
(1009, 202, 13.50, '2026-01-12', '2026-01-12'),
(1009, 203, 10.00, '2026-01-15', '2026-01-15'),

(1010, 204, 08.50, '2026-01-11', '2026-01-11');

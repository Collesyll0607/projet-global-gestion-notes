-- =============================================================================
-- PROJET GLOBAL : Requêtes d'Analyse SQL et Rapports Décisionnels
-- Noms des tables révisés (Composition, Enseignement)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- REQUÊTE 1 : Moyenne générale pondérée par étudiant avec filière et niveau
-- -----------------------------------------------------------------------------
SELECT 
    e.id_etudiant,
    e.nom,
    e.prenom,
    f.nom_filiere,
    n.nom_niveau,
    ROUND(SUM(c.note * m.coefficient) / SUM(m.coefficient), 2) AS moyenne_generale,
    COUNT(c.id_matiere) AS nombre_matieres_composees,
    CASE 
        WHEN (SUM(c.note * m.coefficient) / SUM(m.coefficient)) >= 16 THEN 'Très Bien'
        WHEN (SUM(c.note * m.coefficient) / SUM(m.coefficient)) >= 14 THEN 'Bien'
        WHEN (SUM(c.note * m.coefficient) / SUM(m.coefficient)) >= 12 THEN 'Assez Bien'
        WHEN (SUM(c.note * m.coefficient) / SUM(m.coefficient)) >= 10 THEN 'Passable'
        ELSE 'Ajourné'
    END AS mention
FROM Etudiant e
JOIN Filiere f ON e.id_filiere = f.id_filiere
JOIN Niveau n ON e.id_niveau = n.id_niveau
JOIN Composition c ON e.id_etudiant = c.id_etudiant
JOIN Matiere m ON c.id_matiere = m.id_matiere
GROUP BY e.id_etudiant, e.nom, e.prenom, f.nom_filiere, n.nom_niveau
ORDER BY moyenne_generale DESC;


-- -----------------------------------------------------------------------------
-- REQUÊTE 2 : Identification des cours avec les meilleures et pires moyennes
-- -----------------------------------------------------------------------------
SELECT 
    m.id_matiere,
    m.nom_matiere,
    m.coefficient,
    COUNT(c.id_etudiant) AS nombre_etudiants,
    ROUND(AVG(c.note), 2) AS note_moyenne,
    MIN(c.note) AS note_minimale,
    MAX(c.note) AS note_maximale,
    ROUND(STDDEV(c.note), 2) AS ecart_type
FROM Matiere m
JOIN Composition c ON m.id_matiere = c.id_matiere
GROUP BY m.id_matiere, m.nom_matiere, m.coefficient
ORDER BY note_moyenne DESC;


-- -----------------------------------------------------------------------------
-- REQUÊTE 3 : Taux de réussite (moyenne >= 10) par Filière et par Niveau
-- -----------------------------------------------------------------------------
WITH MoyennesEtudiants AS (
    SELECT 
        e.id_etudiant,
        e.id_filiere,
        e.id_niveau,
        SUM(c.note * m.coefficient) / SUM(m.coefficient) AS gpa
    FROM Etudiant e
    JOIN Composition c ON e.id_etudiant = c.id_etudiant
    JOIN Matiere m ON c.id_matiere = m.id_matiere
    GROUP BY e.id_etudiant, e.id_filiere, e.id_niveau
)
SELECT 
    f.nom_filiere,
    n.nom_niveau,
    COUNT(m.id_etudiant) AS total_etudiants,
    SUM(CASE WHEN m.gpa >= 10 THEN 1 ELSE 0 END) AS admis,
    SUM(CASE WHEN m.gpa < 10 THEN 1 ELSE 0 END) AS ajournes,
    ROUND( (SUM(CASE WHEN m.gpa >= 10 THEN 1 ELSE 0 END) * 100.0) / COUNT(m.id_etudiant), 2) AS taux_reussite_pct
FROM MoyennesEtudiants m
JOIN Filiere f ON m.id_filiere = f.id_filiere
JOIN Niveau n ON m.id_niveau = n.id_niveau
GROUP BY f.nom_filiere, n.nom_niveau
ORDER BY taux_reussite_pct DESC;


-- -----------------------------------------------------------------------------
-- REQUÊTE 4 : Rang des étudiants par classe (Filière + Niveau) (Window Function)
-- -----------------------------------------------------------------------------
WITH StudentAverages AS (
    SELECT 
        e.id_etudiant,
        e.nom,
        e.prenom,
        f.nom_filiere,
        n.nom_niveau,
        ROUND(SUM(c.note * m.coefficient) / SUM(m.coefficient), 2) AS moyenne
    FROM Etudiant e
    JOIN Filiere f ON e.id_filiere = f.id_filiere
    JOIN Niveau n ON e.id_niveau = n.id_niveau
    JOIN Composition c ON e.id_etudiant = c.id_etudiant
    JOIN Matiere m ON c.id_matiere = m.id_matiere
    GROUP BY e.id_etudiant, e.nom, e.prenom, f.nom_filiere, n.nom_niveau
)
SELECT 
    nom_filiere,
    nom_niveau,
    DENSE_RANK() OVER (PARTITION BY nom_filiere, nom_niveau ORDER BY moyenne DESC) AS rang_classe,
    nom,
    prenom,
    moyenne
FROM StudentAverages
ORDER BY nom_filiere, nom_niveau, rang_classe;


-- -----------------------------------------------------------------------------
-- REQUÊTE 5 : Charge d'enseignement par professeur et matières dispensées
-- -----------------------------------------------------------------------------
SELECT 
    p.id_prof,
    p.nom,
    p.prenom,
    p.departement,
    COUNT(DISTINCT ens.id_matiere) AS nombre_matieres_enseignees,
    COUNT(DISTINCT ens.id_niveau) AS nombre_niveaux_couverts,
    STRING_AGG(DISTINCT m.nom_matiere, ', ') AS matieres_list
FROM Professeur p
JOIN Enseignement ens ON p.id_prof = ens.id_prof
JOIN Matiere m ON ens.id_matiere = m.id_matiere
GROUP BY p.id_prof, p.nom, p.prenom, p.departement
ORDER BY nombre_matieres_enseignees DESC;

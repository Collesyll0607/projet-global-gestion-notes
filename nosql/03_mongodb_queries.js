// =============================================================================
// PROJET GLOBAL : Requêtes d'Analyse NoSQL & Aggregation Pipelines MongoDB
// =============================================================================

use notes_etudiants_db;

// -----------------------------------------------------------------------------
// REQUÊTE 1 : Calcul de la moyenne générale pondérée de chaque étudiant
// -----------------------------------------------------------------------------
db.etudiants.aggregate([
  { $unwind: "$evaluations" },
  {
    $group: {
      _id: "$id_etudiant",
      nom: { $first: "$nom" },
      prenom: { $first: "$prenom" },
      filiere: { $first: "$filiere.nom_filiere" },
      niveau: { $first: "$niveau.nom_niveau" },
      totalPoints: { $sum: { $multiply: ["$evaluations.note", "$evaluations.coefficient"] } },
      totalCoeff: { $sum: "$evaluations.coefficient" }
    }
  },
  {
    $project: {
      id_etudiant: "$_id",
      nom_complet: { $concat: ["$prenom", " ", "$nom"] },
      filiere: 1,
      niveau: 1,
      moyenne_generale: { $round: [{ $divide: ["$totalPoints", "$totalCoeff"] }, 2] }
    }
  },
  { $sort: { moyenne_generale: -1 } }
]);


// -----------------------------------------------------------------------------
// REQUÊTE 2 : Analyse des performances par Matière (Note moyenne, min, max)
// -----------------------------------------------------------------------------
db.etudiants.aggregate([
  { $unwind: "$evaluations" },
  {
    $group: {
      _id: "$evaluations.id_matiere",
      nom_matiere: { $first: "$evaluations.nom_matiere" },
      nombre_evaluations: { $sum: 1 },
      moyenne_matiere: { $avg: "$evaluations.note" },
      note_min: { $min: "$evaluations.note" },
      note_max: { $max: "$evaluations.note" }
    }
  },
  {
    $project: {
      id_matiere: "$_id",
      nom_matiere: 1,
      nombre_evaluations: 1,
      moyenne_matiere: { $round: ["$moyenne_matiere", 2] },
      note_min: 1,
      note_max: 1
    }
  },
  { $sort: { moyenne_matiere: -1 } }
]);


// -----------------------------------------------------------------------------
// REQUÊTE 3 : Taux d'admission par Filière
// -----------------------------------------------------------------------------
db.etudiants.aggregate([
  { $unwind: "$evaluations" },
  {
    $group: {
      _id: "$id_etudiant",
      filiere: { $first: "$filiere.nom_filiere" },
      totalPoints: { $sum: { $multiply: ["$evaluations.note", "$evaluations.coefficient"] } },
      totalCoeff: { $sum: "$evaluations.coefficient" }
    }
  },
  {
    $project: {
      filiere: 1,
      moyenne: { $divide: ["$totalPoints", "$totalCoeff"] },
      estAdmis: { $cond: [ { $gte: [{ $divide: ["$totalPoints", "$totalCoeff"] }, 10] }, 1, 0 ] }
    }
  },
  {
    $group: {
      _id: "$filiere",
      totalEtudiants: { $sum: 1 },
      totalAdmis: { $sum: "$estAdmis" }
    }
  },
  {
    $project: {
      filiere: "$_id",
      totalEtudiants: 1,
      totalAdmis: 1,
      tauxReussitePct: { $round: [{ $multiply: [{ $divide: ["$totalAdmis", "$totalEtudiants"] }, 100] }, 2] }
    }
  }
]);

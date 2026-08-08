// =============================================================================
// PROJET GLOBAL : Modélisation et Implémentation NoSQL MongoDB
// Document Schema Validation & Index Creation
// =============================================================================

// Utilisation de la base de données notes_etudiants_db
use notes_etudiants_db;

// 1. Création de la collection 'etudiants' avec validation de schéma JSON
db.createCollection("etudiants", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id_etudiant", "nom", "prenom", "email", "filiere", "niveau", "evaluations"],
      properties: {
        id_etudiant: { bsonType: "int", description: "Identifiant unique de l'étudiant" },
        nom: { bsonType: "string", description: "Nom de famille" },
        prenom: { bsonType: "string", description: "Prénom" },
        date_naissance: { bsonType: "string", description: "Date de naissance (YYYY-MM-DD)" },
        email: { bsonType: "string", description: "Email universitaire" },
        adresse: { bsonType: "string" },
        filiere: {
          bsonType: "object",
          required: ["id_filiere", "nom_filiere"],
          properties: {
            id_filiere: { bsonType: "int" },
            nom_filiere: { bsonType: "string" }
          }
        },
        niveau: {
          bsonType: "object",
          required: ["id_niveau", "nom_niveau"],
          properties: {
            id_niveau: { bsonType: "int" },
            nom_niveau: { bsonType: "string" }
          }
        },
        evaluations: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["id_matiere", "nom_matiere", "coefficient", "note"],
            properties: {
              id_matiere: { bsonType: "int" },
              nom_matiere: { bsonType: "string" },
              coefficient: { bsonType: ["double", "int"] },
              note: { bsonType: ["double", "int"], minimum: 0, maximum: 20 },
              professeur: {
                bsonType: "object",
                properties: {
                  id_prof: { bsonType: "int" },
                  nom_prof: { bsonType: "string" }
                }
              },
              date_evaluation: { bsonType: "string" }
            }
          }
        }
      }
    }
  }
});

// Indexation recommandée pour accélérer les requêtes d'agrégation
db.etudiants.createIndex({ "id_etudiant": 1 }, { unique: true });
db.etudiants.createIndex({ "filiere.nom_filiere": 1, "niveau.nom_niveau": 1 });
db.etudiants.createIndex({ "evaluations.note": 1 });
db.etudiants.createIndex({ "evaluations.id_matiere": 1 });

print("Collections et Index MongoDB créés avec succès !");

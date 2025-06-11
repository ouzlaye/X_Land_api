{
  "citoyen": {
    "nom": "Ndiaye",
    "prenom": "Fatou",
    "telephone": "771234567"
  },
  "coordonnees": {
    "A": [248800.0, 1637400.0],
    "B": [248820.0, 1637400.0],
    "C": [248820.0, 1637420.0],
    "D": [248800.0, 1637420.0]
  },
  "documents": ["piece_identite.pdf", "justificatif.png"]
}

🔗 2. Demande de NICAD (par X-Road)

POST /api/citizenRequest/{id}/demandeNICAD

Retourne :
nicad si accepté

motifRefus si rejeté


✅ 3. Validation de la délibération
POST /api/citizenRequest/{id}/validerDeliberation
Précondition : statut = nicad_valide

Génère :
deliberation_pdf

Changement de statut → deliberation_validee


🏛️ 4. Demande d’acte foncier à la DGID
POST /api/citizenRequest/{id}/demandeActe
Payload :

json
{
  "typeActe": "bail_habitation"
}
Types possibles :

"bail_habitation"

"bail_agricole"

"titre_foncier"

Retourne :

acte.numero

acte.pdf

statut = titre_cree


🔍 5. Suivi d'une demande complète
GET /api/citizenRequest/{id}
Retourne toutes les infos citoyennes, coordonnées, NICAD, délibération, acte DGID, et statut du dossier.

🧪 Cas de test recommandé
Créer une demande citoyenne

Appeler /demandeNICAD → obtenir un nicad

Appeler /validerDeliberation → vérifier deliberation_pdf

Appeler /demandeActe avec un typeActe → obtenir un acte final

Appeler /citizenRequest/{id} pour suivre le dossier complet

Tous les statuts intermédiaires sont visibles dans le fichier citizen_requests.json. Les documents sont générés dans le dossier documents/.

🗃️ Fichiers produits
citizen_requests.json → base des demandes

xroad_logs.json → journal des appels simulés (mairie ↔ cadastre / DGID)

documents/deliberations/ → PDF de délibération

documents/actes/ → PDF de notification d’acte DGID

🧩 À intégrer côté frontend
L’interface peut afficher :

Le statut de la demande (ex : nicad_valide, titre_cree)

Les documents PDF (liens à télécharger)

Les messages en cas de refus du cadastre

L’ID de la demande pour permettre le suivi via /citizenRequest/{id}

🚀 Extensions possibles
Authentification citoyen / agent

Simulations de délais / notifications

Visualisation cartographique avec NICAD

RFC – Intégration du paiement mobile HOLO dans openIMIS Comores (Lot 10 – Paiements mobiles AMG)

Version: 1.0 (Proposition)
Destinataires: UTGAM, Équipes openIMIS, MSO/HOLO (TagPay)
Auteur: UTGAM/openIMIS Comores – Équipe Intégration Paiement
Statut: Draft RFC technique
Date: YYYY-MM-DD

**1. Contexte Fonctionnel**
- Rôle du paiement mobile dans l’AMG: le paiement mobile permet l’encaissement des cotisations des bénéficiaires AMG, l’automatisation de la validation comptable et l’activation des droits d’assurance santé dans openIMIS.
- Processus UTGAM/openIMIS: affiliation du bénéficiaire → génération de facture/cotisation → initiation du paiement → réception de notification → validation de la transaction → activation des droits → archivage et traçabilité.
- Rôle de HOLO (plateforme MSO – TagPay): HOLO agit comme passerelle de paiement mobile (session, authentification PIN + SMS OTP, exécution de la transaction, redirections, notifications serveur à serveur) et supporte la conformité et la sécurité (IP whitelist, signatures).

**2. Objectifs du Lot**
- Intégrer le flux HOLO de bout en bout dans openIMIS, couvrant: Initiation → Redirection → Authentification → Notification → Validation → Activation des droits.
- Assurer conformité financière, sécurité et traçabilité: SLA, logs, double journalisation, prévention de doublons, réconciliation quotidienne.
- Respecter les spécifications UTGAM et HOLO: endpoints, paramètres obligatoires, statuts, scénarios utilisateurs.

2.1. Configuration fournie (ENV DEV)
- Domaine applicatif: `https://dev.amg.km`
- Méthode d’authentification HOLO: `SMS` (PIN + OTP)
- Merchant ID HOLO (16 chiffres): `2449462108576891`
- URLs de redirection et callback (DEV):
  - `Notify URL`: `https://dev.amg.km/payment/notify`
  - `Accept URL`: `https://dev.amg.km/payment/accept?purchaseref=<ref>`
  - `Decline URL`: `https://dev.amg.km/payment/decline?purchaseref=<ref>`
  - `Cancel URL`: `https://dev.amg.km/payment/cancel?purchaseref=<ref>`
- Notify Email: à compléter par UTGAM
- Legal Info URL: à compléter par UTGAM
- IP Whitelist HOLO: inclure `3.6.76.175` (+ liste officielle MSO)

**3. Scénarios Utilisateurs (PM-HOLO-1 à PM-HOLO-6)**
- PM-HOLO-1: UTGAM initie un paiement HOLO depuis openIMIS.
  - Déclenchement via portail UTGAM/openIMIS sur une facture active.
  - openIMIS crée une session HOLO et prépare les paramètres de redirection.
- PM-HOLO-2: Le bénéficiaire est redirigé vers la page HOLO.
  - Redirection automatique/manuel (bouton « Payer avec HOLO ») avec `merchantid`, `sessionid`, `amount`, `currency`, `purchaseref`, `accepturl`, `cancelurl`, `declineurl`.
- PM-HOLO-3: Authentification (PIN + SMS OTP).
  - Le bénéficiaire saisit son PIN mobile et valide un OTP reçu par SMS.
- PM-HOLO-4: HOLO notifie openIMIS via Notify URL.
  - Notification serveur à serveur, contenant l’ID de transaction, le statut et les montants.
- PM-HOLO-5: openIMIS valide et met à jour la facture.
  - Vérifie l’intégrité (signature/hash, IP whitelist), enregistre paiement, met la facture au statut « Payée ».
- PM-HOLO-6: Activation des droits AMG.
  - openIMIS active automatiquement les droits du bénéficiaire et journalise l’événement.

**4. Architecture d’Intégration**
- 4.1. Flux HOLO complet
  - openIMIS → Session request HOLO
  - HOLO → Session ID
  - openIMIS → Redirection client + paramètres (`merchantid`, `sessionid`, `amount`, `currency`, `purchaseref`, `accepturl`, `cancelurl`, `declineurl`)
  - HOLO → Page d’authentification (PIN + OTP SMS)
  - HOLO → Execute transaction
  - HOLO → Notify URL (serveur UTGAM/openIMIS)
  - openIMIS → Vérification optionnelle (endpoint `GET /payment/status` ou `POST /payment/verify`)
  - openIMIS → Enregistrement + activation des droits
- 4.2. Schéma UML / BPMN (texte et PlantUML – à compléter en annexe)
  - Conditions de fin: ACCEPT (succès), DECLINE (refus), CANCEL (annulation), TIMEOUT (expiration), erreurs d’authentification (PIN/OTP).
  - Séquence (PlantUML – exemple):

```
@startuml
actor Beneficiaire as B
participant openIMIS as OI
participant HOLO as H

OI -> H: POST /session (initiation)
H --> OI: 200 {sessionid}
OI -> B: Redirect to H with params
B -> H: PIN + SMS OTP
H -> H: Execute transaction
H -> OI: POST Notify {status, ref_trans, amount_paid}
OI -> H: (optionnel) Verify
OI -> OI: Update facture, Activate rights
OI -> B: Redirect Accept/Decline/Cancel
@enduml
```

**5. Spécification API**
- 5.1. API openIMIS (côté UTGAM)
  - `POST /payment/initiate`
    - Rôle: créer une session HOLO et préparer la redirection.
    - Entrée (JSON): `{ "beneficiaryId": string, "invoiceId": string }`
    - Sortie (JSON): `{ "redirectUrl": string, "sessionid": string, "purchaseref": string }`
  - `POST /payment/notify`
    - Rôle: point de notification HOLO (serveur à serveur).
    - Entrée (JSON): voir 6.2 (payload HOLO); inclut signature/hash.
    - Sortie (JSON): `{ "ack": true }` avec code HTTP 200.
  - `GET /payment/status?ref=<purchaseref>`
    - Rôle: consulter le statut d’une transaction.
    - Sortie (JSON): `{ "status": "success|decline|cancel|timeout|error", "ref_trans": string, "amount_paid": number, "timestamp": string }`
  - Optionnel: `POST /payment/verify`
    - Rôle: vérifier la transaction auprès de HOLO si supporté.
    - Entrée: `{ "ref_trans": string }` ; Sortie: état consolidé.
- 5.2. Paramètres HOLO obligatoires (document HOLO)
  - `sessionid`: ID de session renvoyé par HOLO.
  - `merchantid` (16 digits): identifiant marchand HOLO.
  - `amount`: montant en KMF.
  - `currency`: code ISO TagPay: `174` pour KMF.
  - `purchaseref`: référence unique AMG (générée par openIMIS).
  - `description`: description lisible de l’achat/cotisation.
  - `accepturl`: URL de redirection en cas de succès.
  - `cancelurl`: URL de redirection en cas d’annulation.
  - `declineurl`: URL de redirection en cas de refus.
- 5.3. Règles de sécurité
  - IP whitelist: autoriser uniquement les IP HOLO (ex: `3.6.76.175`) sur `POST /payment/notify`.
  - Hash / signature: exiger une signature HMAC (clé partagée HOLO↔UTGAM) ou signature TagPay si prévue.
  - Protocole HTTPS: toutes les URLs publiques et callbacks sur TLS 1.2+.
  - Validation MerchantID + IP: vérifier `merchantid` (16 chiffres) et l’adresse IP source.

**6. Modèle de Données**
- 6.1. Données envoyées à HOLO
  - `amount`: Montant AMG (source: openIMIS facture/cotisation).
  - `purchaseref`: Référence unique AMG (source: openIMIS).
  - `merchantid`: ID marchand HOLO (source: Fournisseur/MSO).
  - `sessionid`: Session HOLO (source: HOLO `POST /session`).
  - `accepturl`, `cancelurl`, `declineurl`: URLs AMG sécurisées (source: Dev openIMIS/UTGAM).
  - `currency`: `174` (KMF – Comores).
  - `description`: ex: « Cotisation AMG – facture #XYZ ».
- 6.2. Données reçues de HOLO (Notify)
  - `ref_trans`: Identifiant unique HOLO de la transaction.
  - `amount_paid`: Montant effectivement payé.
  - `timestamp`: Date/heure de transaction (UTC ISO 8601).
  - `status`: `success|decline|cancel|timeout|error`.
  - Optionnels (si fournis): `msisdn`, `currency`, `purchaseref`, `merchantid`, `signature`.

**7. Workflow détaillé**
- 7.1. Initiation
  - Acteur: openIMIS.
  - API utilisée: `POST /payment/initiate` (vers HOLO: `POST /session`).
  - Paramètres: `beneficiaryId`, `invoiceId`.
  - JSON (exemple sortie):
    ```json
    {
      "redirectUrl": "https://holo.example.com/pay?...",
      "sessionid": "S1234567890",
      "purchaseref": "AMG-INV-2025-000123"
    }
    ```
  - Gestion d’erreurs: facture introuvable, montant à 0, bénéficiaire inactif → HTTP 400/422.
- 7.2. Redirection vers HOLO
  - Acteur: openIMIS → bénéficiaire.
  - API utilisée: redirection HTML GET/POST.
  - Paramètres: `merchantid`, `sessionid`, `amount`, `currency`, `purchaseref`, `description`, `accepturl`, `cancelurl`, `declineurl`.
  - HTML (exemple): voir 11.2.
  - Erreurs: paramètres manquants → message utilisateur, retour à openIMIS.
- 7.3. Authentification (PIN + OTP)
  - Acteur: HOLO, bénéficiaire.
  - API utilisée: page HOLO; PIN + SMS OTP.
  - Paramètres: gérés par HOLO.
  - Erreurs: `SMS OTP failed`, `PIN incorrect` → statuts spécifiques.
- 7.4. Exécution de la transaction
  - Acteur: HOLO.
  - API utilisée: core TagPay/HOLO.
  - Paramètres: internes HOLO.
  - Erreurs: TIMEOUT, solde insuffisant, réseau indisponible.
- 7.5. Notification HOLO (Notify URL)
  - Acteur: HOLO → openIMIS.
  - API utilisée: `POST /payment/notify` (UTGAM/openIMIS).
  - Paramètres (JSON): voir 11.3.
  - Erreurs: signature invalide, IP non autorisée → HTTP 403; payload incomplet → 422.
- 7.6. Vérification (optionnelle)
  - Acteur: openIMIS.
  - API utilisée: `GET /payment/status` ou `POST /payment/verify` (si disponible côté HOLO).
  - Paramètres: `ref_trans` ou `purchaseref`.
  - Erreurs: divergence montants → alerte comptable, statut « en litige ».
- 7.7. Activation des droits AMG
  - Acteur: openIMIS.
  - API utilisée: logique interne openIMIS pour activer droits.
  - Paramètres: facture → contrat/affiliation.
  - Erreurs: base de données indisponible → retry + file d’attente.

**8. Gestion des Statuts HOLO**
- Statuts HOLO et logique openIMIS:
  - `ACCEPT`/`success`: paiement enregistré, facture « Payée », droits activés.
  - `DECLINE`/`fail`: transaction abandonnée, facture inchangée, journalisation.
  - `CANCEL`: annulation volontaire utilisateur, facture inchangée.
  - `TIMEOUT`: expiration; possibilité de relancer; facture inchangée.
  - `SMS OTP failed`: authentification échoue; facture inchangée.
  - `PIN incorrect`: authentification échoue; facture inchangée.
- Fallback comptable UTGAM (erreur technique): passage en traitement manuel, rapprochement différé, documentation des écarts.

**9. Sécurité**
- Signature HOLO: vérifier la signature jointe (HMAC ou mécanisme TagPay) sur `POST /payment/notify`.
- Signature côté openIMIS: signer les requêtes critiques vers HOLO (si applicable).
- Whitelist IP: autoriser l’IP HOLO `3.6.76.175` (et la liste officielle MSO) sur le firewall/API.
- Logs + double journalisation: tracer tous les événements dans openIMIS et un journal comptable secondaire.
- SLA: définir temps de réponse, disponibilité, fenêtres de maintenance.
- Protection contre la duplication: dédupliquer sur `purchaseref` + `ref_trans` avec verrouillage idempotent.
- Réconciliation financière: extraction journalière des transactions HOLO et rapprochement avec openIMIS; rapport des écarts.

**10. Tests Fonctionnels et Techniques**
- 10.1 Tests unitaires: validation de création de session, génération `purchaseref`, parsing de Notify, vérification de signatures.
- 10.2 Tests d’intégration: parcours complet mocké HOLO; notifications avec IP et signature; activation des droits.
- 10.3 Tests de montée en charge: simulateur de 100–500 paiements/h; latence; robustesse.
- 10.4 Tests de sécurité: attaques de relecture, IP non whitelist, payload altéré, TLS strict.
- 10.5 Scénarios E2E HOLO: PM-HOLO-1→6 avec jeux de données réalistes.

**11. Exemples Concrets**
- 11.1 Exemple de requête session HOLO (initiation)
  ```http
  POST https://holo.example.com/api/session
  Content-Type: application/json

  {
    "merchantid": "2449462108576891",
    "currency": 174,
    "amount": 5000,
    "purchaseref": "AMG-INV-2025-000123",
    "description": "Cotisation AMG – facture #000123"
  }
  ```
- 11.2 Exemple de redirection HTML
  ```html
  <form action="https://holo.example.com/pay" method="post">
    <input type="hidden" name="merchantid" value="2449462108576891" />
    <input type="hidden" name="sessionid" value="S1234567890" />
    <input type="hidden" name="amount" value="5000" />
    <input type="hidden" name="currency" value="174" />
    <input type="hidden" name="purchaseref" value="AMG-INV-2025-000123" />
    <input type="hidden" name="description" value="Cotisation AMG – facture #000123" />
    <input type="hidden" name="accepturl" value="https://dev.amg.km/payment/accept" />
    <input type="hidden" name="cancelurl" value="https://dev.amg.km/payment/cancel" />
    <input type="hidden" name="declineurl" value="https://dev.amg.km/payment/decline" />
    <button type="submit">Payer avec HOLO</button>
  </form>
  ```
- 11.3 Exemple JSON de notification HOLO
  ```json
  {
    "ref_trans": "HTAG-2025-00004567",
    "purchaseref": "AMG-INV-2025-000123",
    "merchantid": "2449462108576891",
    "amount_paid": 5000,
    "currency": 174,
    "status": "success",
    "timestamp": "2025-11-20T14:05:12Z",
    "signature": "b64-hmac-sha256"
  }
  ```
- 11.4 Exemple de réponse openIMIS (Notify)
  ```json
  { "ack": true }
  ```
- 11.5 Exemple d’erreur et correction comptable
  - Cas: `status=success` mais montant divergeant.
  - Action: marquer « en litige », déclencher vérification, journaliser écart, corriger via procédure comptable UTGAM.

**12. Annexes**
- Capture HOLO « Online / Configuration Marchand »: à intégrer (image fournie par MSO/HOLO).
- Contenus exacts des URLs (Notify/Accept/Decline/Cancel): à confirmer par UTGAM; recommandations:
  - Environnement DEV (`dev.amg.km`):
    - `Notify URL`: `https://dev.amg.km/payment/notify`
    - `Accept URL`: `https://dev.amg.km/payment/accept?purchaseref=<ref>`
    - `Decline URL`: `https://dev.amg.km/payment/decline?purchaseref=<ref>`
    - `Cancel URL`: `https://dev.amg.km/payment/cancel?purchaseref=<ref>`
- Règles HOLO Merchant: inclure contraintes `merchantid` (16 chiffres), sécurité, formats.
- Modèles SMS AMG (annexe UTGAM): textes d’OTP et confirmations.
- Schéma complet (UML/BPMN): à intégrer (PlantUML/diagramme fourni).

—
Notes de mise en œuvre:
- Environnements: prévoir `TEST` et `PROD` avec clés/signatures distinctes.
- Observabilité: dashboards de taux de succès, temps de traitement, erreurs.
- Idempotence: toutes les écritures côté `POST /payment/notify` idempotentes par `ref_trans` + `purchaseref`.
- Conformité: archivage légal, traçabilité RGPD locale, rétention selon politique UTGAM.
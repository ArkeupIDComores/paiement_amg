# openimis-be-amg-payment_py

Module backend openIMIS pour l’intégration paiement AMG via HOLO/TagPay.

## Objet
- Fournir un module conforme à la nomenclature `openimis-be-<module>_py` pouvant être installé en mode editable dans l’assemblage openIMIS backend.
- Réutilise les vues existantes de l’app `payments` (AMG) et expose des URLs compatibles.

## Installation (développement)
1. Placer ce répertoire à côté de `openimis-be_py` (pas dedans) [wiki].
2. Installer en mode editable:
   - `pip install -e ../openimis-be-amg-payment_py/`
3. Ajouter le module dans les extensions backend (selon votre configuration openIMIS).

## Contenu
- `amg_payment/` : paquet Python du module, avec `apps.py` et `urls.py`.
- `pyproject.toml` : packaging minimal pour installation.

## Intégration
- Les URLs du module proxy vers les vues existantes afin d’éviter toute duplication.
- À terme, les vues/templates pourront être déplacés dans ce module pour une intégration complète.

## Notes
- Ce module est un squelette d’adaptation pour faciliter l’intégration dans l’écosystème openIMIS.
- L’IP whitelist et le MerchantID restent configurés côté environnement.
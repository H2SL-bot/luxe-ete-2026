# Lieux fermés — événements fantômes à ne jamais republier

Un lieu peut fermer pour travaux plusieurs années. L'événement garde une date future :
ni la purge ni validate.py ne le voient. Seule la vérification web l'attrape.

| Lieu | Statut | Constaté | Conséquence |
|---|---|---|---|
| Jumeirah Burj Al Arab (Dubaï) — et ses tables, dont Al Muntaha | Fermé pour restauration depuis le 15/04/2026, réouverture visée octobre 2027 | 11/08/2026 (page Al Muntaha en 404, page hôtel : « the restoration of Jumeirah Burj Al Arab ») | Événement « Réveillon du Nouvel An — gala Al Muntaha » du 31/12/2026 RETIRÉ du site |

## Règle
Si un vérificateur rend `fiable=false` parce que le lieu est fermé, en travaux ou
définitivement clos à la date de l'événement :
1. Retirer l'ÉVÉNEMENT du site, pas seulement son séjour — la voie d'invitation
   d'un événement impossible est plus nuisible que l'absence de fiche.
2. Inscrire le lieu dans ce tableau, avec la date du constat et la preuve.
3. Ne jamais recréer d'événement dans ce lieu avant la date de réouverture annoncée,
   et seulement après re-vérification.

"""
Reproductibilité : chaque script écrit, à côté de ses résultats, une fiche d'environnement (date, commande,
versions de Python, PyTorch, pandas, matplotlib, système, commit git). La fonction est celle du traitement
des données (dépôt outil-saisi, paquet `traitement`), pour que les fiches des deux dépôts aient la même forme.
"""
from traitement.reproductibilite import ecrire_environnement  # noqa: F401

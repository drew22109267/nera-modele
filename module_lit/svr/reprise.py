r"""
Reprise après une coupure : les bancs longs (banc des choix, banc des paramètres, triage) enregistrent chaque
résultat dès qu'il est calculé ; relancés, ils relisent ce qui est déjà fait et ne calculent que le reste.

Quand un résultat enregistré est-il encore valable ?
----------------------------------------------------
Chaque résultat est rangé sous une SIGNATURE qui réunit tout ce dont il dépend :
    · les données lues (contenu de la série ou des passages) ;
    · les options de la commande (service, horizons, τ, pas, --rapide…) ;
    · le code : le texte de tous les fichiers Python du calcul (script, paquet svr, paquet triage).
Si l'un d'eux change (nouvelle saisie, autre option, correction du code), la signature change et rien de
l'ancien calcul n'est repris : on ne mélange jamais deux versions. `--recommencer` efface la reprise du banc.

Les fichiers vont dans resultats/reprise/<banc>/ (jamais sur GitHub, comme tout resultats/). Chaque écriture
passe par un fichier temporaire renommé ensuite : une coupure pendant l'écriture ne laisse pas de fichier
à moitié écrit (le renommage est atomique).
"""
from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

import torch


def empreinte(*parties) -> str:
    """Empreinte SHA-1 de tout ce qu'on lui donne (textes, nombres, tableaux pandas, chemins de fichiers)."""
    h = hashlib.sha1()
    for p in parties:
        if isinstance(p, Path):
            fichiers = sorted(p.rglob("*.py")) if p.is_dir() else [p]
            for f in fichiers:
                if "__pycache__" not in f.parts:
                    h.update(f.name.encode()); h.update(f.read_bytes())
        elif hasattr(p, "to_csv"):                          # DataFrame / Series : son contenu complet
            h.update(p.to_csv().encode())
        else:
            h.update(repr(p).encode())
    return h.hexdigest()


class Reprise:
    """
    Mémoire des résultats d'un banc.
        r = Reprise(dossier, signature)
        resultat = r.calculer(cle, lambda: calcul_long())     # relu s'il existe, sinon calculé puis enregistré
    """

    def __init__(self, dossier: Path, signature: str, recommencer: bool = False,
                 adopter: bool = False, signature_donnees: str | None = None):
        """
        adopter : garder les résultats enregistrés même si le CODE a changé, à condition que les données et les
        options soient les mêmes (signature_donnees). À n'utiliser que si la modification ne touche pas ce qui
        est enregistré : par exemple un banc qui enregistre ses PRÉVISIONS et dont seuls les tests statistiques,
        calculés après lecture, ont changé. Une ancienne marque sans partie « données » est acceptée avec un
        avertissement (marques écrites avant cette option).
        """
        self.dossier = Path(dossier)
        if recommencer and self.dossier.exists():
            shutil.rmtree(self.dossier)
        self.dossier.mkdir(parents=True, exist_ok=True)
        self.signature = signature
        self.repris = self.calcules = 0
        # Une autre signature dans le dossier : ancien calcul (données, options ou code différents), on l'efface.
        marque = self.dossier / "signature.txt"
        nouvelle = f"{signature}\n{signature_donnees or ''}"
        lignes = marque.read_text(encoding="utf-8").split("\n") if marque.exists() else []
        if not lignes or lignes[0].strip() != signature:
            ancienne_donnees = lignes[1].strip() if len(lignes) > 1 else ""
            garder = adopter and lignes and (not ancienne_donnees or ancienne_donnees == signature_donnees)
            if garder:
                print(f"  (reprise : code modifié, {len(list(self.dossier.glob('*.pt')))} résultat(s) gardé(s) "
                      "sur demande ; données et options " + ("identiques)" if ancienne_donnees else "non vérifiables, ancienne marque)"),
                      flush=True)
            else:
                for f in self.dossier.glob("*.pt"):
                    f.unlink()
            marque.write_text(nouvelle, encoding="utf-8")
        elif len(lignes) < 2 and signature_donnees:
            marque.write_text(nouvelle, encoding="utf-8")

    def _chemin(self, cle) -> Path:
        return self.dossier / f"{hashlib.sha1(repr(cle).encode()).hexdigest()[:20]}.pt"

    def existe(self, cle) -> bool:
        return self._chemin(cle).exists()

    def lire(self, cle):
        # weights_only=False : fichiers écrits par ce même programme sur cet ordinateur (résultats, pas de modèle tiers).
        return torch.load(self._chemin(cle), weights_only=False)["valeur"]

    def ecrire(self, cle, valeur) -> None:
        chemin = self._chemin(cle)
        temporaire = chemin.with_suffix(".tmp")
        torch.save({"cle": repr(cle), "valeur": valeur}, temporaire)
        os.replace(temporaire, chemin)

    def calculer(self, cle, fonction):
        if self.existe(cle):
            try:
                valeur = self.lire(cle)
                self.repris += 1
                return valeur
            except Exception:                                  # fichier illisible : on refait le calcul
                pass
        valeur = fonction()
        try:
            self.ecrire(cle, valeur)
        except Exception as erreur:                             # objet impossible à enregistrer : on continue sans
            print(f"  (reprise : résultat non enregistré, {type(erreur).__name__} : {erreur})", flush=True)
        self.calcules += 1
        return valeur

    def bilan(self) -> str:
        return f"reprise : {self.repris} résultat(s) relu(s), {self.calcules} calculé(s) — {self.dossier}"

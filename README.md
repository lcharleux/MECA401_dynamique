# MECA401 — Mécanique dynamique

Cours web en MyST Markdown et notebooks, construit avec Jupyter Book 2.

## Consulter localement

Avec Python, Node.js et les dépendances de `requirements.txt` installés :

```sh
make build
make serve
```

Ouvrir <http://localhost:3000>. Pour travailler avec rechargement automatique :

```sh
make preview
```

Ne pas ouvrir directement les fichiers HTML avec `file://`.

## Structure

- `myst.yml` configure le livre et son sommaire.
- `src/index.md` est la page d’accueil.
- `src/dynamique/` accueille les chapitres du cours.
- `src/notebooks/` accueille les notebooks Jupyter.
- `src/assets/` et `src/styles/` regroupent les ressources du site.

## Publication automatique sur GitHub Pages

Le workflow `.github/workflows/pages.yml` construit et publie le cours à chaque
push sur `main`. Dans les réglages **Pages** du dépôt, choisir **GitHub Actions**
comme source de déploiement.

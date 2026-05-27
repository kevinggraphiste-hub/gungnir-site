# gungnir_site

Site marketing officiel de Gungnir — édité par Scarlet Wolf.

Statique pur (HTML + CSS + JS vanilla), palette propre à l'écosystème
Gungnir (scarlet/bronze/cream/anthracite, polices Cinzel + Cormorant
Garamond + JetBrains Mono).

## Arborescence

```
gungnir_site/
├── src/
│   ├── partials/
│   │   ├── head.html       # <head> commun (templated)
│   │   ├── header.html     # <header> + nav commune (templated)
│   │   └── footer.html     # <footer> commun (templated)
│   └── pages/
│       ├── index.html      # body de la home
│       ├── souverainete.html
│       ├── technique.html
│       ├── installation.html
│       ├── prix.html
│       ├── guide.html
│       ├── a-propos.html
│       ├── contact.html
│       └── contact.head.html  # <style> inline spécifique au form
├── build.py                # assemble src/ → racine + pages/ (HTML statique)
├── index.html              # SORTIE générée — ne pas éditer à la main
├── pages/*.html            # SORTIE générée — ne pas éditer à la main
├── assets/{css,js,img}/
└── README.md
```

## Workflow

Toute modification se fait dans `src/` (partials + pages + métadonnées
dans `build.py`). Avant chaque commit :

```bash
python3 build.py    # regénère index.html et pages/*.html
git status          # vérifier les fichiers modifiés
```

## Aperçu local

```bash
python3 -m http.server 8080
# puis http://localhost:8080
```

## Déploiement

Auto-deploy via GitHub Actions à chaque push `main` : SSH sur le VPS,
`git pull`, Nginx sert le HTML statique directement. Pas de build distant.

## Contenu

Le contenu est aligné sur le brief stratégique 2026-05-08 :
- Triptyque narratif **Éveil / Conscience / Souveraineté**
- Plans tarifaires **Personal / Standard / Compliance**
- Live publique **28 mai 2026 chez Renaud Dékode**
- Aucune comparaison frontale Hermes/Cowork/Cursor/Devin
- Licences mentionnées : **BSL** (Gungnir), **Apache 2.0** (SpearCode),
  **MIT** (Munnin)
- Trial 14 jours, 4 modèles OpenRouter free, sans carte bancaire

## TODO si on étoffe plus tard

- [ ] Logo Gungnir vectoriel à intégrer dans `assets/img/`
- [ ] Photos / captures app dans le hero ou la section live
- [ ] Brancher Calendly sur le bouton "Réservons trente minutes"
- [ ] Remplacer le `mailto:` du formulaire contact par un endpoint
      backend (si on veut des analytics ou anti-spam plus solide)
- [ ] Page legale (CGU/CGV/mentions légales/RGPD) — à demander à un juriste
- [ ] Sitemap.xml + robots.txt si SEO sérieux
- [ ] OG image + meta Twitter pour le partage social

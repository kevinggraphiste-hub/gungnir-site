# gungnir_site

Site marketing officiel de Gungnir — édité par Scarlet Wolf.

Statique pur (HTML + CSS + JS vanilla), palette propre à l'écosystème
Gungnir (scarlet/bronze/cream/anthracite, polices Cinzel + Cormorant
Garamond + JetBrains Mono).

## Arborescence

```
gungnir_site/
├── index.html              # Landing
├── pages/
│   ├── souverainete.html   # DA souveraine (BSL, on-prem, audit)
│   ├── prix.html           # Personal / Standard / Compliance
│   ├── guide.html          # Guide d'utilisation
│   ├── a-propos.html       # Vision Scarlet Wolf + live 28 mai
│   └── contact.html        # Form mailto + démo 30 min
├── assets/
│   ├── css/style.css       # CSS partagé
│   ├── js/main.js          # Menu mobile + reveal scroll
│   └── img/                # (vide — à alimenter avec photos / mockups)
└── README.md
```

## Aperçu local

Ouvrir simplement `index.html` dans le navigateur, ou démarrer un serveur
statique :

```bash
cd gungnir_site
python3 -m http.server 8080
# puis http://localhost:8080
```

## Déploiement

Site 100% statique, pas de PHP, pas de build. Trois options selon le besoin :

### A. IONOS FTP
Uploader le dossier complet via FileZilla dans le `htdocs` du domaine
cible (un sous-domaine type `site.scarletwolf.cloud` ou un futur
domaine dédié — voir aussi B/C ci-dessous).

### B. Cloudflare Pages / Netlify / Vercel
Drag & drop du dossier complet — déploiement immédiat avec HTTPS automatique.

### C. Sous-domaine côté Hostinger (cohérent avec gungnir.scarletwolf.cloud)
Upload via FTP ou git push si le repo est branché.

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

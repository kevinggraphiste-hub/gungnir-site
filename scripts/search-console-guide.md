# Guide express — Search Console + Bing Webmaster

À faire **après** le cutover Nginx (étape 6) et le push (sinon les pages ne
sont pas encore servies depuis l'apex). Compte ~10 min total.

## 1. Google Search Console (5 min)

### Créer la propriété domaine

1. Aller sur https://search.google.com/search-console/welcome
2. Cliquer "Domaine" (gauche, pas "Préfixe d'URL")
3. Taper `scarletwolf.cloud` → Continuer
4. Google donne un **TXT DNS** à ajouter chez ton registrar du domaine
   (probablement Cloudflare ou Hostinger selon où le DNS de
   `scarletwolf.cloud` est hébergé)

   Exemple type :
   ```
   Type:  TXT
   Nom:   @
   Valeur: google-site-verification=xxxxxxxxxxxxxxxxxxxxxxx
   ```

5. Ajouter le TXT, attendre ~5 min, cliquer "Valider" dans GSC
6. Une fois validé : Sitemaps (menu gauche)
7. Coller `sitemap.xml` → Envoyer

### Demander l'indexation des pages clés

Toujours dans GSC, menu gauche "Inspection d'URL" :

1. Coller `https://scarletwolf.cloud/` → Demander l'indexation
2. Idem pour `/prix`, `/contact`, `/a-propos`, `/souverainete`

GSC fait ~1 par minute, donc fais-en 5 et reviens plus tard.

## 2. Bing Webmaster Tools (3 min)

1. https://www.bing.com/webmasters/
2. Se connecter (compte Microsoft, ou réutiliser Google via "Connect from GSC")
3. Si "Import from GSC" est proposé : oui, tout est automatique
4. Sinon : Add a site → `https://scarletwolf.cloud` → vérifier (CNAME, TXT
   ou fichier HTML — choisir TXT, copier la valeur, ajouter au DNS comme
   pour GSC)
5. Sitemaps → Add sitemap → `https://scarletwolf.cloud/sitemap.xml`

## 3. Validation des Rich Results (2 min)

1. https://search.google.com/test/rich-results
2. Coller `https://scarletwolf.cloud/prix`
   → doit détecter le **FAQPage** (4 questions, anti-action-manuelle)
3. Coller `https://scarletwolf.cloud/`
   → doit détecter **SoftwareApplication** et **Event** (live 28 mai 2026)
4. Coller `https://scarletwolf.cloud/installation`
   → doit détecter **HowTo** (3 étapes)
5. Coller `https://scarletwolf.cloud/a-propos`
   → doit détecter **Person** (Kevin G., LinkedIn/X/YouTube)

Si erreurs : me les coller, j'adapte les schemas.

## 4. Test du rendu OG (1 min)

1. https://www.opengraph.xyz/
2. Coller `https://scarletwolf.cloud/`
3. Vérifier le rendu sur les onglets Facebook / LinkedIn / Twitter
   → image 1200×630 (lance rouge + "GUNGNIR" + tagline + url scarlet) doit
   apparaître propre

Si l'image est moche : on peut générer une OG différente par page plus tard
(le brief contient les og:title/og:description par page, prêts).

## 5. Suivi indexation (4 semaines)

Chaque lundi pendant 4 semaines, dans Google :
```
site:scarletwolf.cloud
```

Cible :
- Semaine 1 : 1-3 résultats (homepage + sitemap soumis)
- Semaine 2 : 4-6
- Semaine 4 : 8 (toutes les pages)

Si stagne à <4 à 3 semaines : me le dire, on regarde le `robots.txt` et les
crawl errors dans GSC.

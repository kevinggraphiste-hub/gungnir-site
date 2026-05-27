# Cutover Nginx — bascule apex sur Gungnir

Une seule action manuelle nécessaire en SSH pour terminer la refonte SEO.
Toute la prep (HTML, config Nginx, certs supposés OK) est dans le repo.

## Prérequis

- SSH au VPS `31.97.116.142` avec sudo
- Certificats Let's Encrypt déjà émis pour `scarletwolf.cloud` et
  `site.scarletwolf.cloud` (vérifier : les deux répondent en HTTPS aujourd'hui)
- Le commit `02d17ec` (étape 5 clean URLs) en local **mais non encore poussé**

## Plan

```
AVANT cutover :
  scarletwolf.cloud       → site Automation (à archiver)
  site.scarletwolf.cloud  → Gungnir (HTML actuel, liens /pages/*.html)

APRÈS cutover :
  scarletwolf.cloud       → Gungnir (clean URLs)
  site.scarletwolf.cloud  → 301 → scarletwolf.cloud
```

## Étapes

### 1. SSH dans le VPS

```bash
ssh <user>@31.97.116.142
```

### 2. Repérer la conf Nginx actuelle

```bash
ls /etc/nginx/sites-enabled/
ls /etc/nginx/sites-available/
sudo nginx -T 2>&1 | grep -E 'server_name|root|ssl_certificate ' | head -40
```

Note :
- Le chemin du clone gungnir-site sur le VPS (probablement
  `/var/www/gungnir-site` ou similaire). C'est ce qui est servi à
  `site.scarletwolf.cloud` aujourd'hui.
- Le chemin du site Automation actuel (à archiver).

### 3. Backup ancienne conf et ancien site

```bash
DATE=$(date +%Y-%m-%d)
sudo cp -a /etc/nginx/sites-available /etc/nginx/sites-available.bak-$DATE
sudo cp -a /etc/nginx/sites-enabled   /etc/nginx/sites-enabled.bak-$DATE

# Archive de l'ancien site Automation (chemin à adapter)
sudo tar czf /root/backup-automation-$DATE.tar.gz /var/www/scarletwolf-automation
```

### 4. Mettre à jour le repo Gungnir sur le VPS

Sur la machine locale d'abord, pousser le commit étape 5 :

```bash
# (en local, depuis ~/Projets/gungnir_site)
git push origin main
```

Le workflow GitHub Actions va SSH et faire `git reset --hard origin/main`.
Vérifier que la nouvelle version est arrivée :

```bash
# (sur le VPS, dans le clone)
cd <ROOT_GUNGNIR_SITE>
git log -1 --format='%h %s'   # doit afficher 02d17ec ou plus récent
ls index.html pages/          # doit lister tous les .html
```

### 5. Installer la nouvelle conf Nginx

```bash
# Copier la nouvelle conf depuis le repo
sudo cp <ROOT_GUNGNIR_SITE>/nginx/scarletwolf.conf /etc/nginx/sites-available/scarletwolf.cloud

# Adapter les 3 placeholders au VPS :
sudo nano /etc/nginx/sites-available/scarletwolf.cloud
#   - root <ROOT>  → chemin réel du clone gungnir-site
#   - chemins des certs Let's Encrypt si différents
```

### 6. Désactiver l'ancienne conf, activer la nouvelle

```bash
# Désactiver les anciens vhosts (ils sont sauvegardés)
sudo rm /etc/nginx/sites-enabled/scarletwolf.cloud*      # ancien Automation
sudo rm /etc/nginx/sites-enabled/site.scarletwolf.cloud* # ancien Gungnir

# Activer le nouveau (un seul fichier gère les 3 vhosts)
sudo ln -sf /etc/nginx/sites-available/scarletwolf.cloud /etc/nginx/sites-enabled/scarletwolf.cloud
```

### 7. Tester puis recharger

```bash
sudo nginx -t          # DOIT dire "syntax is ok" et "test is successful"
sudo systemctl reload nginx
```

### 8. Vérifier le résultat

```bash
# Apex sert Gungnir
curl -sI https://scarletwolf.cloud/ | grep -E 'HTTP|Server'
# Doit retourner 200

# Clean URLs OK
curl -sI https://scarletwolf.cloud/contact | grep -E 'HTTP'
# Doit retourner 200 (sert /pages/contact.html en interne)

# Anciennes URLs .html → 301
curl -sI https://scarletwolf.cloud/pages/contact.html | grep -E 'HTTP|Location'
# Doit retourner 301 + Location: /contact

# Sub-domain → 301 apex
curl -sI https://site.scarletwolf.cloud/ | grep -E 'HTTP|Location'
# Doit retourner 301 + Location: https://scarletwolf.cloud/

# www → 301 apex
curl -sI https://www.scarletwolf.cloud/ | grep -E 'HTTP|Location'
# Doit retourner 301 + Location: https://scarletwolf.cloud/
```

Lancer aussi le script complet :

```bash
bash <ROOT_GUNGNIR_SITE>/scripts/verify.sh
```

## Rollback en cas de pépin

```bash
# 1. Restaurer la conf
sudo rm /etc/nginx/sites-enabled/scarletwolf.cloud
sudo cp -a /etc/nginx/sites-enabled.bak-$DATE/. /etc/nginx/sites-enabled/

# 2. Tester + reload
sudo nginx -t && sudo systemctl reload nginx

# 3. Côté repo, revert le commit clean-urls
cd <local repo>
git revert 02d17ec
git push origin main
```

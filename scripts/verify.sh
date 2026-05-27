#!/usr/bin/env bash
# Vérifications post-cutover scarletwolf.cloud.
# Exit code 0 = tout OK, !=0 = au moins un check a échoué.

set -u
ORIGIN="https://scarletwolf.cloud"
SUB="https://site.scarletwolf.cloud"
WWW="https://www.scarletwolf.cloud"
FAIL=0

check() {
    local name="$1"
    local expected="$2"
    local actual="$3"
    if [[ "$actual" == *"$expected"* ]]; then
        printf "  ✓ %s\n" "$name"
    else
        printf "  ✗ %s — attendu '%s', obtenu : %s\n" "$name" "$expected" "$actual"
        FAIL=$((FAIL + 1))
    fi
}

echo "== Foundation files =="
check "robots.txt 200"   "200" "$(curl -sI "$ORIGIN/robots.txt" | head -1)"
check "robots déclare le sitemap" "Sitemap: $ORIGIN/sitemap.xml" "$(curl -s "$ORIGIN/robots.txt" | grep -i Sitemap:)"
check "sitemap.xml 200"  "200" "$(curl -sI "$ORIGIN/sitemap.xml" | head -1)"
check "sitemap XML valide" '<?xml' "$(curl -s "$ORIGIN/sitemap.xml" | head -1)"
check "llms.txt 200"     "200" "$(curl -sI "$ORIGIN/llms.txt" | head -1)"

echo
echo "== Pages clean URLs (200) =="
for path in / /souverainete /technique /prix /installation /guide /a-propos /contact; do
    code=$(curl -sI "$ORIGIN$path" | head -1)
    check "GET $path" "200" "$code"
done

echo
echo "== Heads complets =="
for path in / /souverainete /technique /prix /installation /guide /a-propos /contact; do
    html=$(curl -s "$ORIGIN$path")
    title=$(echo "$html" | grep -oE '<title>[^<]+</title>' | head -1)
    desc=$(echo "$html" | grep -oE '<meta name="description"[^>]*>' | head -1)
    canon=$(echo "$html" | grep -oE 'rel="canonical"[^>]*>' | head -1)
    jsonld_count=$(echo "$html" | grep -c 'application/ld+json')
    check "$path title"        "<title>" "$title"
    check "$path description"  "name=\"description\"" "$desc"
    check "$path canonical"    "rel=\"canonical\"" "$canon"
    check "$path JSON-LD ≥ 1"  "1" "$([[ $jsonld_count -ge 1 ]] && echo 1 || echo 0)"
done

echo
echo "== Redirections =="
loc=$(curl -sI "$SUB/" | grep -i '^location:' | tr -d '\r')
check "site. → 301 vers apex" "Location: $ORIGIN/" "$loc"
loc=$(curl -sI "$SUB/contact" | grep -i '^location:' | tr -d '\r')
check "site./contact → 301 apex/contact" "Location: $ORIGIN/contact" "$loc"
loc=$(curl -sI "$WWW/" | grep -i '^location:' | tr -d '\r')
check "www. → 301 vers apex" "Location: $ORIGIN/" "$loc"
loc=$(curl -sI "$ORIGIN/pages/contact.html" | grep -i '^location:' | tr -d '\r')
check "apex/pages/contact.html → 301 /contact" "Location: /contact" "$loc"
loc=$(curl -sI "$ORIGIN/index.html" | grep -i '^location:' | tr -d '\r')
check "apex/index.html → 301 /" "Location: /" "$loc"

echo
echo "== Assets =="
check "favicon.svg 200"      "200" "$(curl -sI "$ORIGIN/favicon.svg" | head -1)"
check "favicon.ico 200"      "200" "$(curl -sI "$ORIGIN/favicon.ico" | head -1)"
check "apple-touch-icon 200" "200" "$(curl -sI "$ORIGIN/apple-touch-icon.png" | head -1)"
check "og default 200"       "200" "$(curl -sI "$ORIGIN/assets/img/og/default.jpg" | head -1)"

echo
if [[ $FAIL -eq 0 ]]; then
    echo "✅ Tous les checks passent."
else
    echo "❌ $FAIL check(s) en échec."
fi
exit $FAIL

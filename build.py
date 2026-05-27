#!/usr/bin/env python3
"""Assemble static HTML pages from src/partials + src/pages.

Sortie commitée en racine (index.html) et pages/ (autres). Le déploiement
SSH reste un simple `git pull` sur le VPS, pas de build distant.
"""

from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PARTIALS = SRC / "partials"
PAGES_SRC = SRC / "pages"


NAV = [
    ("index",        "Accueil",                False),
    ("souverainete", "Souveraineté",           False),
    ("technique",    "Technique",              False),
    ("installation", "Installation",           False),
    ("prix",         "Tarifs",                 False),
    ("guide",        "Guide",                  False),
    ("a-propos",     "À propos",               False),
    ("contact",      "Démo&nbsp;30&nbsp;min",  True),   # bouton CTA
]


DEFAULT_TAGLINE = "L'assistant IA qui apprend votre métier."
ALT_TAGLINE     = "L'IA qui s'éveille à votre métier."
DEFAULT_LOC     = " · Suisse / France"
COMMA_LOC       = ", Suisse / France"

PAGES = [
    {
        "slug": "index",
        "title": "Gungnir : l'assistant IA qui apprend votre métier · Scarlet Wolf",
        "description": "Gungnir, l'assistant IA privé qui apprend votre métier et s'en souvient. Hébergé en Europe, à vous, sans engagement. Essai 14 jours, démo 30 min.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": COMMA_LOC,
        "dest": "index.html",
        "at_root": True,
    },
    {
        "slug": "souverainete",
        "title": "Souveraineté · Vos données restent les vôtres · Gungnir",
        "description": "Vos données restent en Europe, à vous, jamais revendues, jamais utilisées pour entraîner d'autres IA. Effacement garanti sous 24 h. Option 100 % chez vous.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/souverainete.html",
        "at_root": False,
    },
    {
        "slug": "technique",
        "title": "Technique · Architecture, plugins, stack · Gungnir",
        "description": "Le détail technique de Gungnir : architecture cognitive Soul/Skill/Personnalité, conscience vectorielle v4, 11 plugins, stack souveraine (Ollama, Qdrant, OpenRouter, Forge), self-host Docker, sécurité et licences.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/technique.html",
        "at_root": False,
    },
    {
        "slug": "installation",
        "title": "Installation · Gungnir",
        "description": "Installer Gungnir : essai cloud immédiat ou self-hosted Docker en une commande. Guide complet pas à pas.",
        "footer_tagline":  ALT_TAGLINE,
        "footer_location": COMMA_LOC,
        "dest": "pages/installation.html",
        "at_root": False,
    },
    {
        "slug": "prix",
        "title": "Tarifs · Cloud souverain ou Forteresse · Gungnir",
        "description": "Deux façons : Cloud souverain (hébergé pour vous en Europe) ou Forteresse (100 % chez vous, rien ne sort). Gratuit des deux côtés. Essai 14 jours sans carte.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/prix.html",
        "at_root": False,
    },
    {
        "slug": "guide",
        "title": "Guide de démarrage · Gungnir · Scarlet Wolf",
        "description": "Démarrer avec Gungnir en quatre étapes : choisir son point de départ, faire connaissance, activer la mémoire, brancher ses outils. Trente minutes suffisent.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/guide.html",
        "at_root": False,
    },
    {
        "slug": "a-propos",
        "title": "À propos · Gungnir · Scarlet Wolf",
        "description": "Scarlet Wolf · éditeur souverain de Gungnir. Notre vision, nos engagements, le live Renaud Dékode du 28 mai 2026.",
        "footer_tagline":  ALT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/a-propos.html",
        "at_root": False,
    },
    {
        "slug": "contact",
        "title": "Contact · Gungnir · Scarlet Wolf",
        "description": "Réservez une démo Gungnir de 30 minutes. Sans engagement, sans carte bancaire, sans formulaire de qualification.",
        "footer_tagline":  ALT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/contact.html",
        "at_root": False,
    },
]


def build_nav(active_slug: str, root: str, pages: str) -> str:
    lines = []
    for slug, label, is_cta in NAV:
        href = f"{root}index.html" if slug == "index" else f"{pages}{slug}.html"
        classes = []
        if slug == active_slug:
            classes.append("active")
        if is_cta:
            classes.append("btn btn--primary")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        style = ' style="padding: 10px 18px;"' if is_cta else ""
        lines.append(f'      <a href="{href}"{cls}{style}>{label}</a>')
    return "\n".join(lines)


def render(page: dict) -> str:
    slug = page["slug"]
    root = "" if page["at_root"] else "../"
    pages = "pages/" if page["at_root"] else ""

    head   = (PARTIALS / "head.html").read_text(encoding="utf-8")
    header = (PARTIALS / "header.html").read_text(encoding="utf-8")
    footer = (PARTIALS / "footer.html").read_text(encoding="utf-8")
    body   = (PAGES_SRC / f"{slug}.html").read_text(encoding="utf-8")

    extras_file = PAGES_SRC / f"{slug}.head.html"
    head_extras = "\n" + extras_file.read_text(encoding="utf-8").rstrip("\n") if extras_file.exists() else ""

    nav = build_nav(slug, root, pages)

    output = head + header + body + footer
    replacements = {
        "{{TITLE}}":           page["title"],
        "{{DESCRIPTION}}":     page["description"],
        "{{ROOT}}":            root,
        "{{PAGES}}":           pages,
        "{{HEAD_EXTRAS}}":     head_extras,
        "{{NAV_LINKS}}":       nav,
        "{{FOOTER_TAGLINE}}":  page["footer_tagline"],
        "{{FOOTER_LOCATION}}": page["footer_location"],
    }
    for k, v in replacements.items():
        output = output.replace(k, v)
    return output


def main():
    for page in PAGES:
        out = render(page)
        dest = ROOT / page["dest"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
        print(f"  built: {page['dest']}")


if __name__ == "__main__":
    main()

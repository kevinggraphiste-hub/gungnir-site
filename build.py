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
JSONLD_DIR = PARTIALS / "jsonld"

SITE_ORIGIN  = "https://scarletwolf.cloud"
DEFAULT_OG   = f"{SITE_ORIGIN}/assets/img/og/default.jpg"
DEFAULT_ALT  = "Gungnir, l'assistant IA souverain pour TPE/PME francophones"


NAV = [
    ("index",        "Accueil",                False),
    ("souverainete", "Souveraineté",           False),
    ("technique",    "Technique",              False),
    ("prix",         "Tarifs",                 False),
    ("guide",        "Guide",                  False),
    ("a-propos",     "À propos",               False),
    ("contact",      "Démo&nbsp;30&nbsp;min",  True),
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
        "og_title": "Gungnir · L'assistant IA qui apprend votre métier",
        "og_description": "Un assistant qui apprend votre métier et s'en souvient. Pas un chatbot qui oublie tout. Votre IA privée, hébergée en Europe.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": COMMA_LOC,
        "dest": "index.html",
        "at_root": True,
    },
    {
        "slug": "souverainete",
        "title": "Souveraineté · Vos données restent les vôtres · Gungnir",
        "description": "Vos données restent en Europe, à vous, jamais revendues, jamais utilisées pour entraîner d'autres IA. Effacement garanti sous 24 h. Option 100 % chez vous.",
        "og_title": "Souveraineté · Vos données restent les vôtres",
        "og_description": "Quatre engagements écrits : hébergement Europe, aucun entraînement de modèles tiers, code auditable, effacement sous 24 h. Mode Forteresse 100 % on-premise.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/souverainete.html",
        "at_root": False,
    },
    {
        "slug": "technique",
        "title": "Technique · Architecture, plugins, stack · Gungnir",
        "description": "Le détail technique de Gungnir v5 : architecture cognitive Soul/Skill/Personnalité, conscience vectorielle per-user (le game changer), 11 plugins, 14 providers LLM (8 natifs + 6 OpenAI-compatibles), stack souveraine Python/FastAPI/PostgreSQL/React, self-host Docker, BSL 1.1.",
        "og_title": "Technique · Architecture, conscience, plugins",
        "og_description": "Architecture full-stack FastAPI/React/PostgreSQL 16, conscience vectorielle per-user isolée et exportable, 14 providers LLM, 11 plugins, 100 % local possible via Ollama + Qdrant.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/technique.html",
        "at_root": False,
    },
    {
        "slug": "prix",
        "title": "Tarifs · Cloud souverain ou Forteresse · Gungnir",
        "description": "Deux façons : Cloud souverain (hébergé pour vous en Europe) ou Forteresse (100 % chez vous, rien ne sort). Gratuit des deux côtés. Essai 14 jours sans carte.",
        "og_title": "Tarifs · Cloud souverain ou Forteresse",
        "og_description": "Deux axes : Cloud souverain hébergé en Europe ou Forteresse 100 % on-premise. Six formules de l'essai gratuit 14 jours à la Compliance Edition. Sans engagement.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/prix.html",
        "at_root": False,
    },
    {
        "slug": "guide",
        "title": "Guide & installation · Gungnir · Scarlet Wolf",
        "description": "Démarrer avec Gungnir en quatre étapes : choisir son point de départ (Cloud, Docker clé en main, source), faire connaissance, activer la mémoire, brancher ses outils. Trente minutes suffisent.",
        "og_title": "Guide de démarrage & installation en 4 étapes",
        "og_description": "De « je découvre » à « il connaît mon métier » en 4 étapes. Cloud souverain ou Docker self-hosted, mémoire long terme, intégrations. Environ 30 minutes.",
        "footer_tagline":  DEFAULT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/guide.html",
        "at_root": False,
    },
    {
        "slug": "a-propos",
        "title": "À propos · Gungnir · Scarlet Wolf",
        "description": "Scarlet Wolf · éditeur souverain de Gungnir. Notre vision, nos engagements, le live Renaud Dékode du 28 mai 2026.",
        "og_title": "À propos · Scarlet Wolf, édition souveraine IA",
        "og_description": "Scarlet Wolf édite Gungnir, l'IA souveraine pour TPE/PME francophones. Trois engagements : auditabilité, isolation par client, pilotage humain mensuel.",
        "footer_tagline":  ALT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/a-propos.html",
        "at_root": False,
    },
    {
        "slug": "contact",
        "title": "Contact · Gungnir · Scarlet Wolf",
        "description": "Réservez une démo Gungnir de 30 minutes. Sans engagement, sans carte bancaire, sans formulaire de qualification.",
        "og_title": "Contact · Démo 30 min de Gungnir",
        "og_description": "Demandez une démo de 30 minutes de Gungnir. Pas de formulaire labyrinthique, pas de CB. Réponse humaine sous 24 h ouvrées. Email direct : contact@scarletwolf.cloud.",
        "footer_tagline":  ALT_TAGLINE,
        "footer_location": DEFAULT_LOC,
        "dest": "pages/contact.html",
        "at_root": False,
    },
]


def build_nav(active_slug: str) -> str:
    lines = []
    for slug, label, is_cta in NAV:
        href = CLEAN_URL[slug]
        classes = []
        if slug == active_slug:
            classes.append("active")
        if is_cta:
            classes.append("btn btn--primary")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        style = ' style="padding: 10px 18px;"' if is_cta else ""
        lines.append(f'      <a href="{href}"{cls}{style}>{label}</a>')
    return "\n".join(lines)


def read_optional(path: Path) -> str:
    """Returns file content prefixed with \\n, or '' if missing."""
    if not path.exists():
        return ""
    return "\n" + path.read_text(encoding="utf-8").rstrip("\n")


CLEAN_URL = {
    "index":        "/",
    "souverainete": "/souverainete",
    "technique":    "/technique",
    "prix":         "/prix",
    "guide":        "/guide",
    "a-propos":     "/a-propos",
    "contact":      "/contact",
}


def canonical_for(page: dict) -> str:
    return SITE_ORIGIN + CLEAN_URL[page["slug"]]


def render(page: dict) -> str:
    slug = page["slug"]

    head   = (PARTIALS / "head.html").read_text(encoding="utf-8")
    header = (PARTIALS / "header.html").read_text(encoding="utf-8")
    footer = (PARTIALS / "footer.html").read_text(encoding="utf-8")
    body   = (PAGES_SRC / f"{slug}.html").read_text(encoding="utf-8")

    head_extras = read_optional(PAGES_SRC / f"{slug}.head.html")
    jsonld_page = read_optional(JSONLD_DIR / f"{slug}.html")

    nav = build_nav(slug)

    output = head + header + body + footer
    replacements = {
        "{{TITLE}}":           page["title"],
        "{{DESCRIPTION}}":     page["description"],
        "{{CANONICAL}}":       canonical_for(page),
        "{{OG_TITLE}}":        page.get("og_title", page["title"]),
        "{{OG_DESCRIPTION}}":  page.get("og_description", page["description"]),
        "{{OG_IMAGE_URL}}":    page.get("og_image_url", DEFAULT_OG),
        "{{OG_IMAGE_ALT}}":    page.get("og_image_alt", DEFAULT_ALT),
        "{{HEAD_EXTRAS}}":     head_extras,
        "{{JSONLD_PAGE}}":     jsonld_page,
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

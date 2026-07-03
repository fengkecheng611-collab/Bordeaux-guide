# -*- coding: utf-8 -*-
"""
Edit original le-wok-du-coin.pdf preserving layout:
1. Cover: "Projet Pro-Act - Cuisine Sino-Locale" -> "IFC/Culture franco-chinoise à table"
2. Recipe pages: Remove BUDGET ESTIMÉ, shift DIFFICULTÉ/TEMPS up
3. Recipe 01 & 02: Replace Étapes de préparation with French translations
"""
import fitz

# ── Helpers ──
def rgb(hex_str):
    """Convert hex colour like '#c84f3b' to (r,g,b) 0-1"""
    h = hex_str.lstrip('#')
    return (int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255)

C_RED     = rgb('#c84f3b')
C_DARK    = rgb('#2b2520')
C_BROWN   = rgb('#6f6258')
C_TITLE   = rgb('#6f3d2e')
C_GREEN   = rgb('#4f7f67')
C_WHITE   = rgb('#fffaf2')
C_BG      = rgb('#ffffff')
C_COVER   = rgb('#874130')  # Cover background colour

FONT_BOLD = "Helvetica-Bold"
FONT_REG  = "Helvetica"

# ── Accented chars ──
a_  = '\xe0'
e_  = '\xe9'
c_  = '\xe7'
eg  = '\xe8'
ea  = '\xea'
ac  = '\xe2'
oc  = '\xf4'
uc  = '\xfb'
ug  = '\xf9'
ef_ = '\xef'
ee_ = '\xee'
E_  = '\xc9'
Eg_ = '\xc8'

doc = fitz.open(r'C:\Users\Lenovo\Desktop\le-wok-du-coin.pdf')

# ================================================================
# PAGE 0: COVER - Change "Projet Pro-Act" to "IFC/Culture..."
# ================================================================
page = doc[0]
# Redact the old text (slightly larger rect to ensure clean cover)
page.add_redact_annot(fitz.Rect(55, 755, 360, 780), fill=C_COVER)
page.apply_redactions()
# Insert new text
new_cover_text = f"IFC/Culture franco-chinoise {a_} table"
page.insert_text((62, 775), new_cover_text, fontname=FONT_REG, fontsize=10, color=C_WHITE)
print('Page 1 (cover): Replaced project name')

# ================================================================
# RECIPE DATA for right column (DIFFICULTÉ + TEMPS) and steps
# ================================================================

# Recipe info: (page_index, difficulty, temps_line1, temps_line2)
recipe_meta = {
    2:  (f"Facile",     "10 min + 55 min de", "cuisson"),   # Recipe 01
    3:  (f"Facile",     "15 min + 30 min de", "cuisson"),   # Recipe 02
    4:  (f"Facile",     "15 min + 12 min de", "cuisson"),   # Recipe 03
    5:  (f"Facile",     "10 min + 18 min de", "cuisson"),   # Recipe 04
    6:  (f"Tr{eg}s facile", "10 min + 8 min de",  "cuisson"),  # Recipe 05
    7:  (f"Facile",     "15 min + 18 min de", "cuisson"),   # Recipe 06
    8:  (f"Facile",     "12 min + 10 min de", "cuisson"),   # Recipe 07
    9:  (f"Moyenne",    "15 min + 20 min de", "cuisson"),   # Recipe 08
    10: (f"Tr{eg}s facile", "12 min + 12 min de", "cuisson"),  # Recipe 09
    11: (f"Tr{eg}s facile", "10 min + 10 min de", "cuisson"),  # Recipe 10
}

# ── New Étapes de préparation for Recipe 01 (Congee) ──
r01_steps = [
    f"1. Laver les travers de porc et les couper en morceaux de 3-4 cm. Rincer le riz et",
    f"le faire tremper dans l'eau claire pendant 30 min (le trempage donne un congee plus",
    f"onctueux, mais on peut sauter cette {e_}tape si l'on est press{e_}).",
    f"2. Mettre les travers dans une casserole avec un peu de gingembre, de ciboule, 1 c.",
    f"{a_} soupe de whisky, et couvrir d'eau. Porter {a_} {e_}bullition {a_} feu vif, {e_}cumer",
    f"la mousse, puis retirer les travers et les rincer {a_} l'eau ti{eg}de.",
    f"3. Dans une nouvelle eau, porter {a_} {e_}bullition puis r{e_}duire le feu. Laisser",
    f"mijoter les travers 20-30 min. Saler et poivrer (le bouillon doit {ea}tre un peu plus",
    f"sal{e_} qu'une soupe classique).",
    f"4. Dans un cuiseur {a_} riz, verser le riz {e_}goutt{e_} et le bouillon avec les travers",
    f"(1 vol. de riz pour 8-10 vol. de bouillon). Lancer le programme porridge 90 min.",
    f"Sans cuiseur {a_} riz : mettre le riz dans la casserole de bouillon, couvrir en",
    f"laissant le couvercle entrouvert, et mijoter 40 min {a_} feu tr{eg}s doux.",
    f"5. Quand les travers sont tendres et le riz bien {e_}clat{e_}, ajouter le gingembre",
    f"{e_}minc{e_} et bien m{e_}langer.",
    f"6. Hors du feu, parsemer de ciboule {e_}minc{e_}e. Quelques gouttes d'huile de",
    f"s{e_}same (facultatif). Laisser reposer 3 min. Attention : le congee est br{uc}lant.",
]

# ── New Étapes de préparation for Recipe 02 (Huangmenji) ──
r02_steps = [
    f"1. Laver les cuisses de poulet, couper en morceaux de 3 cm (garder l'os pour plus",
    f"de go{uc}t). Bien {e_}goutter. {E_}plucher et {e_}mincer l'oignon en petits d{e_}s.",
    f"2. M{e_}langer le poulet avec du sel, la f{e_}cule de ma{ef_}s, 1 c. {a_} soupe de whisky,",
    f"du poivre et l'oignon. Masser {a_} la main. Laisser mariner 10-15 min (pas plus). Le",
    f"whisky se trouve facilement en supermarch{e_}.",
    f"3. {E_}p{e_}piner le poivron et le couper en morceaux. {E_}plucher les pommes de terre,",
    f"les tailler en cubes (les garder dans l'eau). {E_}mincer le gingembre, l'ail et la",
    f"ciboule en tranches.",
    f"4. Chauffer l'huile dans une po{ea}le ou cocotte {a_} feu vif. Faire revenir le",
    f"gingembre, l'ail et la ciboule jusqu'{a_} ce qu'ils embaument. Ajouter le poulet",
    f"marin{e_} en d{e_}tachant bien les morceaux.",
    f"5. Faire dorer le poulet sur toutes les faces. Ajouter la sauce soja et une petite",
    f"pinc{e_}e de sucre (optionnel). Bien m{e_}langer pour enrober chaque morceau.",
    f"6. Ajouter les pommes de terre et faire revenir 1 min. Verser un demi-verre d'eau,",
    f"porter {a_} {e_}bullition, puis r{e_}duire le feu. Couvrir et mijoter 15 min.",
    f"7. Ajouter le poivron et poursuivre la cuisson 5 min, jusqu'{a_} ce que les pommes",
    f"de terre soient fondantes, le poulet bien cuit et la sauce r{e_}duite.",
    f"8. Go{uc}ter et ajuster l'assaisonnement. M{e_}langer et servir avec du riz.",
]

# ================================================================
# PROCESS ALL RECIPE PAGES (pages 2-11, 0-indexed)
# ================================================================

for pg in range(2, 12):
    page = doc[pg]
    diff, t1, t2 = recipe_meta[pg]

    # ── Remove BUDGET, shift DIFF/TEMPS up ──
    # Redact whole right-column info area
    page.add_redact_annot(fitz.Rect(415, 52, 535, 232), fill=C_BG)
    page.apply_redactions()

    # Insert DIFFICULTÉ (shifted up ~45pt from original y=129 to y=86)
    page.insert_text((418, 86), f"DIFFICULT{E_}", fontname=FONT_BOLD, fontsize=9, color=C_TITLE)
    page.insert_text((418, 101), diff, fontname=FONT_REG, fontsize=11, color=C_DARK)

    # Insert TEMPS (shifted up ~45pt from original y=184 to y=141)
    page.insert_text((418, 141), "TEMPS", fontname=FONT_BOLD, fontsize=9, color=C_TITLE)
    page.insert_text((418, 156), t1, fontname=FONT_REG, fontsize=11, color=C_DARK)
    page.insert_text((418, 171), t2, fontname=FONT_REG, fontsize=11, color=C_DARK)

    print(f'Page {pg+1}: Removed BUDGET ESTIME, shifted DIFF/TEMPS up')

    # ── Replace Étapes for Recipe 01 (page 2) and Recipe 02 (page 3) ──
    if pg == 2:  # Recipe 01
        # Redact old steps area (y=508 to y=635) and astuce (y=672 to y=725)
        page.add_redact_annot(fitz.Rect(60, 508, 530, 635), fill=C_BG)
        page.add_redact_annot(fitz.Rect(60, 672, 530, 725), fill=C_BG)
        page.apply_redactions()

        # Insert new steps at 9pt (smaller to fit longer text)
        y = 511
        for line in r01_steps:
            page.insert_text((68, y), line, fontname=FONT_REG, fontsize=9, color=C_DARK)
            y += 13.5  # line spacing

        # Re-insert astuce header and text (may need adjusting)
        page.insert_text((68, 675), f"Astuce {e_}tudiante", fontname=FONT_BOLD, fontsize=10, color=C_GREEN)
        astuce_text = (
            f"Pr{e_}pare une grande casserole et garde une portion au frigo. Le lendemain, "
            f"ajoute un peu d'eau et r{e_}chauffe doucement : le congee devient encore plus "
            f"cr{e_}meux."
        )
        page.insert_text((68, 694), astuce_text, fontname=FONT_REG, fontsize=9, color=C_DARK)
        print(f'Page {pg+1}: Replaced Etapes de preparation (Recipe 01)')

    elif pg == 3:  # Recipe 02
        # Redact old steps area (y=494 to y=606) and astuce (y=642 to y=695)
        page.add_redact_annot(fitz.Rect(60, 494, 530, 606), fill=C_BG)
        page.add_redact_annot(fitz.Rect(60, 642, 530, 695), fill=C_BG)
        page.apply_redactions()

        # Insert new steps at 9pt
        y = 497
        for line in r02_steps:
            page.insert_text((68, y), line, fontname=FONT_REG, fontsize=9, color=C_DARK)
            y += 13.5

        # Re-insert astuce
        page.insert_text((68, 645), f"Astuce {e_}tudiante", fontname=FONT_BOLD, fontsize=10, color=C_GREEN)
        astuce_text = (
            f"Si la sauce est trop liquide, {e_}crase deux morceaux de pomme de terre "
            f"dans la casserole : cela {e_}paissit naturellement sans farine."
        )
        page.insert_text((68, 664), astuce_text, fontname=FONT_REG, fontsize=9, color=C_DARK)
        print(f'Page {pg+1}: Replaced Etapes de preparation (Recipe 02)')

    # ── Review Recipes 03-10: minor text corrections if needed ──
    # The steps in the original are already well-adapted. No changes needed.
    # But we need to reapply redactions since they were removed.
    # Actually, only the right column was redacted - the steps area is untouched
    # for recipes 03-10, so no additional edits needed there.

# ================================================================
# SAVE
# ================================================================
output = r'C:\Users\Lenovo\Desktop\le-wok-du-coin-v2.pdf'
doc.save(output, garbage=4, deflate=True)
doc.close()
print(f'\nSaved to: {output}')
print('Done!')

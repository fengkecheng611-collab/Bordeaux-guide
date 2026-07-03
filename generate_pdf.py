# -*- coding: utf-8 -*-
"""
Generate modified PDF with:
1. Cover title changed to IFC/Culture franco-chinoise a table
2. BUDGET ESTIME removed from all recipe pages
3. Recipe 01 & 02 steps replaced with French translations
4. Recipes 03-10 steps reviewed and refined

NOTE: All French accented characters use x escapes (via variables)
to avoid an fpdf2 multi_cell bug with literal non-ASCII chars.
"""

from fpdf import FPDF

# Accented character shortcuts (readability)
_a = '\xe0'   # \xe0 grave
_e = '\xe9'   # \xe9 aigu
_c = '\xe7'   # \xe7 c cédille
_e8 = '\xe8'  # \xe8 grave
_ae = '\xe6'  # \xe6 ae ligature
_oe = chr(0x153)  # oe ligature (chr to avoid fpdf2 literal bug)
_OE = chr(0x152)  # OE ligature uppercase
_o = '\xf4'   # \xf4 circonflexe
_u = '\xfb'   # \xfb circonflexe
_E = '\xc9'   # \xc9 E aigu
_e2 = '\xe2'  # \xe2 a circonflexe
_ea = '\xea'  # \xea e circonflexe
_ef = '\xef'  # \xef i trema
_ee = '\xee'  # \xee i circonflexe
_u8 = '\xf9'  # \xf9 u grave
_E8 = '\xc8'  # \xc8 E grave
_A = '\xc0'   # \xc0 A grave


class RecipeBook(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('C', '', r'C:\Windows\Fonts\calibri.ttf')
        self.add_font('C', 'B', r'C:\Windows\Fonts\calibrib.ttf')
        self.add_font('C', 'I', r'C:\Windows\Fonts\calibrii.ttf')
        self.add_font('C', 'BI', r'C:\Windows\Fonts\calibriz.ttf')
        self.set_auto_page_break(True, 15)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('C', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'- {self.page_no()} -', 0, 0, 'C')

    def cover_page(self):
        self.add_page()
        self.ln(40)

        self.set_font('C', 'B', 28)
        self.set_text_color(180, 40, 40)
        self.cell(0, 14, 'IFC', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

        self.set_font('C', 'B', 22)
        self.set_text_color(180, 40, 40)
        self.cell(0, 12, 'Culture franco-chinoise', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 12, f'{_a} table', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(12)

        self.set_font('C', '', 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, f"10 recettes chinoises adapt{_e}es aux", align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, f"supermarch{_e}s fran{_c}ais", align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

        self.set_font('C', 'I', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 7, "Manger chinois, local, simple et budget-friendly", align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(15)

        self.set_font('C', '', 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, f"IFC — Cuisine Sino-Locale", align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_font('C', '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, f"Carnet de recettes {_e}tudiantes IFC", align='C', new_x="LMARGIN", new_y="NEXT")

    def toc_page(self):
        self.add_page()
        self.ln(15)
        self.set_font('C', 'B', 22)
        self.set_text_color(180, 40, 40)
        self.cell(0, 12, 'SOMMAIRE', 0, 1, 'C')
        self.ln(8)

        self.set_font('C', '', 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 6, "Des recettes chinoises avec ce que", align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 6, "l'on trouve vraiment en France", align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

        self.set_font('C', 'I', 10)
        self.set_text_color(100, 100, 100)
        intro = (
            "Ce carnet ne cherche pas la version la plus authentique "
            f"{_a} tout prix. Il part d'une question plus simple : que "
            "peut-on cuisiner quand on vit en France, avec un petit budget, "
            f"une plaque de cuisson, une po{_ea}le, et les rayons de Lidl, "
            f"Carrefour, Auchan ou Intermarch{_e} ?"
        )
        self.multi_cell(0, 5.5, intro, align='C')
        self.ln(10)

        recipes_toc = [
            ("01", "Congee aux travers de porc"),
            ("02", f"Poulet mijot{_e} fa{_c}on Huangmenji"),
            ("03", "Poulet aux champignons de Paris"),
            ("04", f"Poulet effiloch{_e} sauce gingembre-ciboule"),
            ("05", f"Riz saut{_e} {_a} la saucisse"),
            ("06", f"Chaussons chinois {_a} la p{_e2}te bris{_e}e"),
            ("07", f"Nouilles saut{_e}es aux spaghetti"),
            ("08", f"Aubergines mijot{_e}es {_a} la chair {_a} saucisse"),
            ("09", f"Galettes de pommes de terre fa{_c}on chinoise"),
            ("10", f"{_OE}ufs brouill{_e}s {_a} la tomate sur riz"),
        ]

        self.set_font('C', '', 11)
        self.set_text_color(60, 60, 60)
        for num, name in recipes_toc:
            self.cell(0, 7, f"  {num}  {name}", 0, 1, 'C')

        self.ln(15)
        self.set_font('C', 'I', 10)
        self.set_text_color(120, 120, 120)
        footer_text = (
            f"L'id{_e}e du Wok du Coin : remplacer sans culpabiliser, "
            f"cuisiner avec bon sens, et garder le go{_u}t r{_e}confortant "
            "de la cuisine maison."
        )
        self.multi_cell(0, 5.5, footer_text, align='C')

    def recipe_page(self, num, title, why, difficulty, temps, ingredients,
                    substitutions, steps, astuce, footer_text):
        self.add_page()

        # Recipe header
        self.set_fill_color(180, 40, 40)
        self.set_text_color(255, 255, 255)
        self.set_font('C', 'B', 13)
        self.cell(0, 10, f'  RECETTE {num:02d}', 0, 1, 'L', True)

        self.set_text_color(180, 40, 40)
        self.set_font('C', 'B', 16)
        self.ln(3)
        self.multi_cell(0, 9, title)
        self.ln(2)

        # Why section
        self.set_font('C', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Pourquoi cette recette ?", 0, 1)
        self.set_font('C', '', 9)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 4.8, why)
        self.ln(4)

        # Difficulty + Time boxes (no BUDGET ESTIME)
        box_w = 80
        box_h = 18

        x_start = self.get_x()
        y_start = self.get_y()
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.rect(x_start, y_start, box_w, box_h, 'DF')

        self.set_xy(x_start + 3, y_start + 2)
        self.set_font('C', 'B', 9)
        self.set_text_color(180, 40, 40)
        self.cell(box_w - 6, 5, f'DIFFICULT{_E}', 0, 1, 'C')
        self.set_x(x_start + 3)
        self.set_font('C', '', 10)
        self.set_text_color(60, 60, 60)
        self.cell(box_w - 6, 5, difficulty, 0, 1, 'C')

        self.set_xy(x_start + box_w + 6, y_start)
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.rect(x_start + box_w + 6, y_start, box_w, box_h, 'DF')

        self.set_xy(x_start + box_w + 9, y_start + 2)
        self.set_font('C', 'B', 9)
        self.set_text_color(180, 40, 40)
        self.cell(box_w - 6, 5, 'TEMPS', 0, 1, 'C')
        self.set_x(x_start + box_w + 9)
        self.set_font('C', '', 9)
        self.set_text_color(60, 60, 60)
        for line in temps.split('\n'):
            self.cell(box_w - 6, 4.5, line, 0, 1, 'C')
            self.set_x(x_start + box_w + 9)

        self.set_y(y_start + box_h + 6)
        self.ln(4)

        # Ingredients
        self.set_font('C', 'B', 11)
        self.set_text_color(180, 40, 40)
        self.cell(0, 6, f"Ingr{_e}dients faciles {_a} trouver en France", 0, 1)
        self.set_draw_color(180, 40, 40)
        self.set_line_width(0.3)
        self.line(self.get_x(), self.get_y(), self.get_x() + 100, self.get_y())
        self.ln(3)
        self.set_font('C', '', 9)
        self.set_text_color(60, 60, 60)
        for ing in ingredients:
            self.cell(0, 4.5, f'  · {ing}', 0, 1)
        self.ln(3)

        # Substitutions
        self.set_font('C', 'B', 10)
        self.set_text_color(180, 40, 40)
        self.cell(0, 5.5, "Substitutions locales", 0, 1)
        self.set_draw_color(180, 40, 40)
        self.line(self.get_x(), self.get_y(), self.get_x() + 100, self.get_y())
        self.ln(2)
        self.set_font('C', '', 8.5)
        self.set_text_color(80, 80, 80)
        for sub in substitutions:
            self.cell(0, 4.2, f'  · {sub}', 0, 1)
        self.ln(3)

        # Steps
        self.set_font('C', 'B', 11)
        self.set_text_color(180, 40, 40)
        self.cell(0, 6, f"{_E}tapes de pr{_e}paration", 0, 1)
        self.set_draw_color(180, 40, 40)
        self.line(self.get_x(), self.get_y(), self.get_x() + 100, self.get_y())
        self.ln(3)

        self.set_font('C', '', 9)
        self.set_text_color(40, 40, 40)
        for i, step in enumerate(steps, 1):
            self.multi_cell(0, 4.5, f'{i}. {step}')
            self.ln(0.5)
        self.ln(2)

        # Astuce box
        self.set_fill_color(250, 240, 240)
        self.set_draw_color(210, 180, 180)

        y_before = self.get_y()
        w = 170

        # Estimate height
        est_lines = max(len(astuce) / 90, 2) + 1
        box_h = 5 + est_lines * 4 + 4

        if y_before + box_h > 270:
            self.add_page()
            y_before = self.get_y()

        self.rect(15, y_before, w, box_h, 'DF')
        self.set_xy(18, y_before + 2)
        self.set_font('C', 'B', 9)
        self.set_text_color(180, 40, 40)
        self.cell(w - 6, 5, f'Astuce {_e}tudiante', 0, 1, 'L')
        self.set_x(18)
        self.set_font('C', '', 8.5)
        self.set_text_color(80, 60, 60)
        self.multi_cell(w - 6, 4, astuce)
        self.set_y(y_before + box_h + 2)

        # Footer
        self.set_font('C', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, footer_text, 0, 1, 'R')


# ============================================================
# Helper: build text with accented chars from the _a, _e, etc.
# ============================================================
# For readability in the recipe data, we use f-strings with
# the _a/_e/_c/etc. shortcuts defined at module level.


def build_pdf():
    pdf = RecipeBook()
    pdf.set_margin(15)

    # ==================== COVER PAGE ====================
    pdf.cover_page()

    # ==================== TABLE OF CONTENTS ====================
    pdf.toc_page()

    # ==================== RECIPE DATA ====================

    # ---- RECIPE 01: Congee aux travers de porc ----
    r01_why = (
        f"Le congee est le bol que l'on pr{_e}pare quand on veut quelque chose "
        f"de doux, chaud et rassurant. Avec des travers de porc et un peu de "
        f"gingembre, il devient un repas simple pour les soirs o{_u8} la maison "
        f"manque un peu."
    )
    r01_diff = "Facile"
    r01_temps = f"15 min + 90 min\ncuisson"
    r01_ingredients = [
        "250 g de travers de porc",
        "90 g de riz rond ou riz long",
        "4 tranches de gingembre",
        f"1 ciboule ou un peu d'oignon nouveau",
        "Sel, poivre blanc ou noir",
        f"1 c. {_a} soupe de whisky ou de rhum",
        f"Quelques gouttes d'huile de s{_e}same (facultatif)",
    ]
    r01_substitutions = [
        f"Le whisky ou le rhum remplace le vin de cuisine chinois : "
        f"il aide {_a} enlever l'odeur forte de la viande et ajoute une note chaude.",
        f"La ciboule peut {_ea}tre remplac{_e}e par de la c{_e}bette ou "
        f"un petit morceau de poireau tr{_e8}s finement coup{_e}.",
        f"Un reste de riz cuit raccourcit la cuisson.",
        f"L'huile de s{_e}same est facultative mais apporte un parfum authentique.",
    ]
    r01_steps = [
        f"Laver les travers de porc et les couper en morceaux de 3-4 cm. "
        f"Rincer le riz et le faire tremper dans l'eau claire pendant 30 minutes "
        f"(le trempage donne un congee plus onctueux, mais on peut sauter cette "
        f"{_e}tape si l'on est press{_e}).",
        f"Mettre les travers dans une casserole, ajouter un peu de gingembre et "
        f"de ciboule {_e}minc{_e}s, une cuill{_e8}re {_a} soupe de whisky (ou de rhum), "
        f"et couvrir largement d'eau froide. Porter {_a} {_e}bullition {_a} feu vif, "
        f"{_e}cumer soigneusement la mousse blanche qui se forme {_a} la surface, "
        f"puis retirer les travers et les rincer {_a} l'eau ti{_e8}de.",
        f"Dans une casserole propre, remettre les travers avec de l'eau fra{_ee}che. "
        f"Porter {_a} {_e}bullition puis baisser le feu. Laisser mijoter doucement "
        f"20 {_a} 30 minutes pour obtenir un bon bouillon. Assaisonner avec du sel "
        f"et du poivre — le bouillon doit {_ea}tre un peu plus sal{_e} qu'une "
        f"soupe classique, car il servira de base au congee.",
        f"Si vous avez un cuiseur {_a} riz : y verser le riz {_e}goutt{_e}, puis le "
        f"bouillon chaud avec les travers, dans une proportion d'environ 1 volume de "
        f"riz pour 8 {_a} 10 volumes de bouillon. Lancer le programme « porridge » "
        f"ou {_a} d{_e}faut le programme normal pour 90 minutes. Sans cuiseur {_a} riz : "
        f"remettre le riz directement dans la casserole de bouillon, couvrir en laissant "
        f"le couvercle l{_e}g{_e8}rement entrouvert, et laisser mijoter {_a} feu tr{_e8}s "
        f"doux pendant 40 minutes en remuant de temps en temps.",
        f"Lorsque les travers sont bien tendres, le riz compl{_e8}tement {_e}clat{_e} "
        f"et la texture du congee bien {_e}paisse et cr{_e}meuse, ajouter le reste du "
        f"gingembre finement {_e}minc{_e}. Bien m{_e}langer.",
        f"Hors du feu, parsemer g{_e}n{_e}reusement de ciboule {_e}minc{_e}e et "
        f"ajouter quelques gouttes d'huile de s{_e}same si vous en avez. Laisser "
        f"reposer 3 minutes avant de servir. Attention : le congee est br{_u}lant, "
        f"remuez-le avant de le porter {_a} la bouche.",
    ]
    r01_astuce = (
        f"Pr{_e}pare une grande casserole et garde une portion au frigo. "
        f"Le lendemain, ajoute un peu d'eau et r{_e}chauffe doucement : "
        f"le congee devient encore plus cr{_e}meux."
    )
    r01_footer = "Congee aux travers de porc"

    # ---- RECIPE 02: Poulet mijote façon Huangmenji ----
    r02_why = (
        f"Inspir{_e} du huangmenji, ce plat donne un vrai go{_u}t de repas "
        f"complet avec une seule casserole. Les pommes de terre absorbent la "
        f"sauce, les poivrons apportent de la couleur, et le poulet reste tendre."
    )
    r02_diff = "Facile"
    r02_temps = f"20 min + 35 min\ncuisson"
    r02_ingredients = [
        f"2 cuisses de poulet ou hauts de cuisse",
        f"2 pommes de terre moyennes",
        f"1 poivron",
        f"1 oignon",
        f"2 gousses d'ail",
        f"3 tranches de gingembre",
        f"1 ciboule (ou tige d'oignon nouveau)",
        f"3 c. {_a} soupe de sauce soja",
        f"1 c. {_a} soupe de whisky (ou rhum)",
        f"1 c. {_a} caf{_e} de f{_e}cule de ma{_ef}s (Ma{_ef}zena)",
        f"Sel, poivre, sucre (optionnel)",
    ]
    r02_substitutions = [
        f"Une seule sauce soja suffit : elle remplace {_a} la fois la sauce "
        f"soja claire et la sauce soja fonc{_e}e.",
        f"Les poivrons surgel{_e}s fonctionnent tr{_e8}s bien.",
        f"Sans gingembre frais, une petite pinc{_e}e de gingembre en poudre peut d{_e}panner.",
        f"Le whisky se trouve facilement et {_a} petit prix en supermarch{_e} "
        f"fran{_c}ais. Il remplace le vin de cuisine chinois pour parfumer la viande.",
        f"La sauce soja {_e}tant d{_e}j{_a} l{_e}g{_e8}rement sucr{_e}e, on peut "
        f"r{_e}duire ou m{_ea}me supprimer le sucre selon son go{_u}t.",
    ]
    r02_steps = [
        f"Laver les cuisses de poulet et les couper en morceaux d'environ 3 cm "
        f"(garder l'os pour plus de go{_u}t). Bien {_e}goutter et r{_e}server. "
        f"{_E}plucher et {_e}mincer l'oignon en petits d{_e}s.",
        f"Dans un saladier, m{_e}langer le poulet avec du sel, la f{_e}cule de "
        f"ma{_ef}s, la cuill{_e8}re {_a} soupe de whisky, du poivre et l'oignon "
        f"{_e}minc{_e}. Bien masser {_a} la main pour faire p{_e}n{_e}trer les "
        f"assaisonnements. Laisser mariner 10 {_a} 15 minutes — pas plus, "
        f"sinon la viande risque de se dess{_e}cher.",
        f"{_E}p{_e}piner le poivron et le couper en morceaux. {_E}plucher les "
        f"pommes de terre et les tailler en cubes (les conserver dans un bol "
        f"d'eau froide pour {_e}viter qu'elles noircissent). {_E}mincer le "
        f"gingembre en lamelles, l'ail en tranches fines et la ciboule en tron{_c}ons.",
        f"Chauffer un filet d'huile dans une grande po{_ea}le ou une cocotte {_a} "
        f"feu moyen-vif. Quand l'huile est bien chaude, faire revenir le gingembre, "
        f"l'ail et la ciboule jusqu'{_a} ce qu'ils embaument. Ajouter le poulet "
        f"marin{_e} en prenant soin de bien d{_e}tacher les morceaux qui collent "
        f"entre eux.",
        f"Faire dorer le poulet sur toutes les faces jusqu'{_a} ce qu'il prenne "
        f"une belle couleur brun-dor{_e}. Ajouter la sauce soja et une petite "
        f"pinc{_e}e de sucre (optionnel, car la sauce soja est d{_e}j{_a} "
        f"l{_e}g{_e8}rement sucr{_e}e). Bien m{_e}langer pour que chaque morceau "
        f"de poulet soit enrob{_e} de sauce.",
        f"Ajouter les cubes de pommes de terre et faire revenir 1 minute en "
        f"remuant. Verser un petit verre d'eau (environ 100 ml), porter {_a} "
        f"{_e}bullition, puis baisser le feu. Couvrir et laisser mijoter 15 "
        f"minutes {_a} feu doux.",
        f"Ajouter les morceaux de poivron, m{_e}langer d{_e}licatement et "
        f"poursuivre la cuisson {_a} couvert pendant 5 minutes suppl{_e}mentaires. "
        f"Les pommes de terre doivent {_ea}tre fondantes, le poulet bien cuit "
        f"et la sauce r{_e}duite et onctueuse. Si la sauce est encore trop "
        f"liquide, faire r{_e}duire 2 minutes {_a} feu vif et {_a} d{_e}couvert.",
       f"Go{_u}ter et rectifier l'assaisonnement avec un peu de sel si "
        f"n{_e}cessaire. M{_e}langer une derni{_e8}re fois et servir aussit{_o}t, "
        f"accompagn{_e} d'un grand bol de riz blanc.",
    ]
    r02_astuce = (
        f"Si la sauce est trop liquide, {_e}crase deux morceaux de pomme de terre "
        f"dans la casserole : cela {_e}paissit naturellement sans farine."
    )
    r02_footer = f"Poulet mijot{_e} fa{_c}on Huangmenji"

    # ---- RECIPE 03: Poulet aux champignons de Paris ----
    r03_why = (
        f"C'est une assiette rapide, {_e}conomique et riche en prot{_e}ines. "
        f"Les champignons de Paris donnent une sauce douce, tr{_e8}s accessible "
        f"pour les personnes qui d{_e}couvrent la cuisine chinoise maison."
    )
    r03_diff = "Facile"
    r03_temps = f"15 min + 12 min\ncuisson"
    r03_ingredients = [
        f"1 blanc de poulet",
        f"200 g de champignons de Paris",
        f"1 gousse d'ail",
        f"2 c. {_a} soupe de sauce soja",
        f"1 c. {_a} caf{_e} de farine ou de f{_e}cule",
        f"Huile, sel, poivre",
    ]
    r03_substitutions = [
        f"Les champignons en barquette remplacent des champignons chinois "
        f"plus difficiles {_a} trouver.",
        f"L'huile d'olive ou de tournesol convient pour une cuisine du quotidien.",
        f"La farine ou la Ma{_ef}zena remplace la f{_e}cule pour attendrir le "
        f"poulet, selon ce que l'on a sous la main.",
    ]
    r03_steps = [
        f"Couper le blanc de poulet en fines lamelles (l{_e}g{_e8}rement en biais "
        f"pour obtenir des tranches plus larges). Dans un bol, m{_e}langer le "
        f"poulet avec 1 c. {_a} soupe de sauce soja, la farine (ou la f{_e}cule) "
        f"et une pinc{_e}e de poivre. Laisser reposer le temps de pr{_e}parer "
        f"le reste.",
        f"{_E}mincer les champignons de Paris en tranches r{_e}guli{_e8}res. "
        f"Hacher finement la gousse d'ail.",
        f"Chauffer un filet d'huile dans une po{_ea}le {_a} feu vif. Y faire "
        f"saisir le poulet en une seule couche. Le retirer d{_e8}s qu'il est dor{_e}, "
        f"sans chercher {_a} le cuire compl{_e8}tement — il finira sa cuisson "
        f"plus tard. R{_e}server sur une assiette.",
        f"Dans la m{_ea}me po{_ea}le, baisser l{_e}g{_e8}rement le feu et faire "
        f"revenir l'ail hach{_e} 30 secondes. Ajouter les champignons {_e}minc{_e}s "
        f"et les faire sauter jusqu'{_a} ce qu'ils rendent leur eau et commencent "
        f"{_a} dorer.",
        f"Remettre le poulet dans la po{_ea}le avec 1 c. {_a} soupe de sauce soja "
        f"et 2 c. {_a} soupe d'eau. M{_e}langer vivement pendant 2 minutes pour "
        f"que le poulet finisse de cuire et que la sauce nappe bien l'ensemble.",
        f"Servir imm{_e}diatement avec du riz blanc.",
    ]
    r03_astuce = (
        f"Coupe le poulet quand il est encore l{_e}g{_e8}rement froid : les "
        f"tranches seront plus fines et cuiront plus vite."
    )
    r03_footer = "Poulet aux champignons de Paris"

    # ---- RECIPE 04: Poulet effiloché sauce gingembre-ciboule ----
    r04_why = (
        f"Cette recette est l{_e}g{_e8}re, parfum{_e}e et tr{_e8}s pratique quand "
        f"on ne veut pas manger frit ou trop gras. Le poulet est cuit doucement "
        f"{_a} la vapeur, puis r{_e}veill{_e} par une sauce chaude au gingembre "
        f"et {_a} la ciboule."
    )
    r04_diff = "Facile"
    r04_temps = f"10 min + 18 min\ncuisson"
    r04_ingredients = [
        f"1 blanc de poulet",
        f"1 morceau de gingembre frais",
        f"1 ciboule ou oignon nouveau",
        f"1 c. {_a} soupe de sauce soja",
        f"Sel, sucre, poivre",
        f"2 c. {_a} soupe d'huile",
    ]
    r04_substitutions = [
        f"La ciboule peut {_ea}tre remplac{_e}e par le vert d'un poireau "
        f"tr{_e8}s finement coup{_e}.",
        f"Sans panier vapeur, une assiette creuse pos{_e}e dans une casserole "
        f"avec un fond d'eau bouillante suffit largement.",
        f"Un filet de jus de citron peut apporter une note de fra{_e8}cheur "
        f"si l'on n'a pas de vinaigre.",
        f"L'huile de tournesol ou de colza convient tr{_e8}s bien pour la sauce chaude.",
    ]
    r04_steps = [
        f"D{_e}poser le blanc de poulet dans une assiette creuse avec quelques "
        f"tranches de gingembre frais. Saler l{_e}g{_e8}rement.",
        f"Porter une casserole d'eau {_a} {_e}bullition (environ 2-3 cm d'eau "
        f"au fond). Poser l'assiette dans la casserole sans qu'elle touche l'eau, "
        f"couvrir et cuire {_a} la vapeur 15 {_a} 18 minutes selon l'{_e}paisseur "
        f"du blanc. Le poulet est cuit quand il est ferme au toucher et que le "
        f"jus qui s'en {_e}coule est clair.",
        f"Laisser ti{_e}dir le poulet quelques minutes, puis l'effilocher {_a} "
        f"la main ou avec deux fourchettes, dans le sens des fibres pour obtenir "
        f"de beaux filaments.",
        f"Dans un petit bol, m{_e}langer le gingembre fra{_e8}chement r{_e2}p{_e}, "
        f"la ciboule tr{_e8}s finement {_e}minc{_e}e, une pinc{_e}e de sel, une "
        f"pinc{_e}e de sucre, du poivre et la sauce soja.",
        f"Chauffer l'huile dans une petite casserole jusqu'{_a} ce qu'elle soit "
        f"bien chaude (elle doit fr{_e}mir l{_e}g{_e8}rement). Verser l'huile "
        f"br{_u}lante en un seul geste sur le m{_e}lange gingembre-ciboule — "
        f"l'huile chaude va imm{_e}diatement lib{_e}rer les ar{_o}mes.",
        f"Verser la sauce parfum{_e}e sur le poulet effiloch{_e}, m{_e}langer "
        f"d{_e}licatement et servir {_a} temp{_e}rature ambiante ou l{_e}g{_e8}rement "
        f"ti{_e8}de.",
    ]
    r04_astuce = (
        f"Pr{_e}pare plus de poulet et garde une partie nature : le lendemain, "
        f"il peut aller dans un sandwich, une salade ou un bol de nouilles."
    )
    r04_footer = f"Poulet effiloch{_e} sauce gingembre-ciboule"

    # ---- RECIPE 05: Riz sauté à la saucisse ----
    r05_why = (
        f"Le riz saut{_e} est le meilleur ami des restes. Ici, la saucisse fum{_e}e "
        f"fran{_c}aise remplace la saucisse chinoise et donne un go{_u}t g{_e}n{_e}reux, "
        f"parfait pour transformer un bol de riz froid en vrai repas."
    )
    r05_diff = f"Tr{_e8}s facile"
    r05_temps = f"10 min + 8 min\ncuisson"
    r05_ingredients = [
        f"1 grand bol de riz cuit froid (id{_e}alement de la veille)",
        f"2 {_oe}ufs",
        f"1 saucisse fum{_e}e (type Montb{_e}liard ou Morteau)",
        f"1 c. {_a} soupe de sauce soja",
        f"Un peu d'oignon ou de ciboule",
        f"Huile, poivre",
    ]
    r05_substitutions = [
        f"La saucisse fum{_e}e remplace la saucisse chinoise quand elle n'est "
        f"pas disponible.",
        f"Des lardons peuvent d{_e}panner, mais il faut en mettre peu car ils "
        f"sont sal{_e}s.",
        f"Ajoute des petits pois surgel{_e}s pour une version plus compl{_e8}te "
        f"et color{_e}e.",
    ]
    r05_steps = [
        f"Couper la saucisse fum{_e}e en petits d{_e}s r{_e}guliers. Battre "
        f"les {_oe}ufs dans un bol avec une pinc{_e}e de sel.",
        f"Chauffer un filet d'huile dans une grande po{_ea}le ou un wok {_a} feu "
        f"vif. Y verser les {_oe}ufs battus et les brouiller rapidement en les "
        f"cassant en morceaux {_a} la spatule. R{_e}server sur une assiette "
        f"d{_e8}s qu'ils sont encore moelleux.",
        f"Dans la m{_ea}me po{_ea}le, faire revenir les d{_e}s de saucisse et "
        f"l'oignon {_e}minc{_e} jusqu'{_a} ce qu'ils commencent {_a} dorer et "
        f"embaument.",
        f"Ajouter le riz froid dans la po{_ea}le. Avec la spatule, {_e}craser "
        f"d{_e}licatement les {_e}ventuels blocs de riz et bien s{_e}parer les "
        f"grains. Faire sauter {_a} feu vif en remuant constamment pour que "
        f"chaque grain soit bien chauff{_e} et l{_e}g{_e8}rement grill{_e}.",
        f"Remettre les {_oe}ufs dans la po{_ea}le, arroser de sauce soja et "
        f"poivrer g{_e}n{_e}reusement. Faire sauter encore 1 minute pour que "
        f"tout soit bien m{_e}lang{_e} et chaud.",
        f"Servir aussit{_o}t, dans un grand bol.",
    ]
    r05_astuce = (
        f"Le riz de la veille est id{_e}al. Si tu viens de le cuire, {_e}tale-le "
        f"10 minutes sur une assiette pour qu'il s{_e8}che un peu avant de le faire "
        f"sauter."
    )
    r05_footer = f"Riz saut{_e} {_a} la saucisse"

    # ---- RECIPE 06: Chaussons chinois à la pâte brisée ----
    r06_why = (
        f"Cette version s'inspire des chaussons {_a} la ciboulette chinois, mais "
        f"sans p{_e2}te maison. La p{_e2}te bris{_e}e de supermarch{_e} rend la "
        f"recette possible m{_ea}me sans rouleau, sans plan de travail et sans "
        f"grande cuisine."
    )
    r06_diff = "Facile"
    r06_temps = f"15 min + 18 min\ncuisson"
    r06_ingredients = [
        f"1 rouleau de p{_e2}te bris{_e}e",
        f"2 {_oe}ufs",
        f"1 petit poireau ou une botte de ciboulette",
        f"1 c. {_a} soupe de sauce soja",
        f"Sel, poivre",
        f"Un peu d'huile pour la po{_ea}le",
    ]
    r06_substitutions = [
        f"La p{_e2}te bris{_e}e remplace la p{_e2}te {_e}tal{_e}e {_a} la main.",
        f"Le poireau remplace la ciboulette chinoise, plus rare en supermarch{_e} "
        f"classique.",
        f"Une p{_e2}te feuillet{_e}e fonctionne aussi, avec un r{_e}sultat plus "
        f"croustillant.",
    ]
    r06_steps = [
        f"Battre les {_oe}ufs en omelette, les cuire rapidement dans une po{_ea}le "
        f"l{_e}g{_e8}rement huil{_e}e en les cassant en petits morceaux, puis "
        f"les laisser ti{_e}dir dans un saladier.",
        f"{_E}mincer tr{_e8}s finement le poireau (le blanc et le vert tendre) "
        f"ou la ciboulette. L'ajouter aux {_oe}ufs refroidis avec la sauce soja, "
        f"une pinc{_e}e de sel et du poivre. Bien m{_e}langer.",
        f"D{_e}rouler la p{_e2}te bris{_e}e et la d{_e}couper en grands cercles "
        f"(avec un bol retourn{_e} comme emporte-pi{_e8}ce) ou en rectangles "
        f"{_a} l'aide d'un couteau.",
        f"D{_e}poser une cuill{_e8}re {_a} soupe de farce au centre de chaque "
        f"cercle de p{_e2}te. Refermer en demi-lune et bien presser les bords "
        f"avec les doigts, puis avec les dents d'une fourchette pour bien sceller.",
        f"Chauffer une po{_ea}le l{_e}g{_e8}rement huil{_e}e {_a} feu moyen. "
        f"D{_e}poser les chaussons et les cuire 4 {_a} 5 minutes par c{_o}t{_e}, "
        f"jusqu'{_a} ce qu'ils soient bien dor{_e}s et croustillants.",
        f"Servir chaud, {_e}ventuellement avec un petit bol de sauce soja "
        f"agr{_e}ment{_e}e de vinaigre pour tremper.",
    ]
    r06_astuce = (
        f"Ne mets pas trop de farce : les chaussons se ferment mieux et ne "
        f"fuient pas dans la po{_ea}le."
    )
    r06_footer = f"Chaussons chinois {_a} la p{_e2}te bris{_e}e"

    # ---- RECIPE 07: Nouilles sautées aux spaghetti ----
    r07_why = (
        f"Les spaghetti sont partout en France, bon march{_e} et faciles {_a} "
        f"doser. Avec une bonne cuisson et un passage sous l'eau froide, ils "
        f"deviennent une base tr{_e8}s correcte pour des nouilles saut{_e}es maison."
    )
    r07_diff = "Facile"
    r07_temps = f"12 min + 10 min\ncuisson"
    r07_ingredients = [
        f"160 g de spaghetti",
        f"2 {_oe}ufs",
        f"1 carotte",
        f"1 oignon",
        f"Une poign{_e}e de chou {_e}minc{_e} ou de salade",
        f"2 c. {_a} soupe de sauce soja",
        f"Huile, sel",
    ]
    r07_substitutions = [
        f"Les spaghetti remplacent les nouilles chinoises.",
        f"La salade un peu fatigu{_e}e peut remplacer le chou en fin de cuisson.",
        f"Les l{_e}gumes surgel{_e}s en julienne font gagner du temps.",
    ]
    r07_steps = [
        f"Cuire les spaghetti dans une grande casserole d'eau bouillante sal{_e}e, "
        f"en les retirant 1 minute avant le temps indiqu{_e} sur le paquet. Ils "
        f"doivent {_ea}tre al dente.",
        f"{_E}goutter les spaghetti puis les passer imm{_e}diatement sous l'eau "
        f"froide pour stopper la cuisson et raffermir leur texture. Bien {_e}goutter "
        f"et les enrober d'un l{_e}ger filet d'huile pour {_e}viter qu'ils ne "
        f"collent entre eux.",
        f"Battre les {_oe}ufs, les cuire rapidement dans une po{_ea}le chaude en "
        f"les brouillant, puis les r{_e}server sur une assiette.",
        f"{_E}mincer l'oignon, tailler la carotte en fines juliennes et {_e}mincer "
        f"finement le chou. Faire revenir le tout dans une grande po{_ea}le avec "
        f"un filet d'huile {_a} feu vif, jusqu'{_a} ce que les l{_e}gumes "
        f"commencent {_a} ramollir tout en restant croquants.",
        f"Ajouter les spaghetti et les {_oe}ufs dans la po{_ea}le, arroser de "
        f"sauce soja. Faire sauter vivement 2 {_a} 3 minutes en soulevant et "
        f"en m{_e}langeant pour que tout s'impr{_e8}gne bien et que les p{_e2}tes "
        f"commencent {_a} l{_e}g{_e8}rement griller.",
        f"Servir imm{_e}diatement, bien chaud.",
    ]
    r07_astuce = (
        f"Le passage {_a} l'eau froide est le petit geste qui change tout : "
        f"les p{_e2}tes deviennent plus fermes et se tiennent mieux {_a} la po{_ea}le."
    )
    r07_footer = f"Nouilles saut{_e}es aux spaghetti"

    # ---- RECIPE 08: Aubergines mijotées à la chair à saucisse ----
    r08_why = (
        f"Les aubergines mijot{_e}es avec une petite sauce sucr{_e}e-sal{_e}e "
        f"rappellent les plats chinois qui appellent un grand bol de riz. La "
        f"chair {_a} saucisse remplace la viande hach{_e}e et apporte du go{_u}t "
        f"sans beaucoup d'assaisonnement."
    )
    r08_diff = "Moyenne"
    r08_temps = f"15 min + 20 min\ncuisson"
    r08_ingredients = [
        f"2 aubergines",
        f"120 g de chair {_a} saucisse",
        f"2 gousses d'ail",
        f"2 c. {_a} soupe de sauce soja",
        f"1 c. {_a} caf{_e} de sucre",
        f"1 c. {_a} soupe de vinaigre (de vin ou de cidre)",
        f"Huile, eau",
    ]
    r08_substitutions = [
        f"La chair {_a} saucisse remplace le porc hach{_e}.",
        f"Le vinaigre de vin ou de cidre remplace tr{_e8}s bien le vinaigre de riz.",
        f"Pour une version v{_e}g{_e}tarienne, utilise des champignons de Paris "
        f"finement hach{_e}s.",
    ]
    r08_steps = [
        f"Couper les aubergines en b{_e2}tonnets r{_e}guliers. Les saler "
        f"l{_e}g{_e8}rement dans une passoire, m{_e}langer et laisser d{_e}gorger "
        f"10 minutes. Rincer rapidement et bien {_e}ponger avec du papier "
        f"absorbant — cela r{_e}duit l'amertume et limite l'absorption "
        f"d'huile {_a} la cuisson.",
        f"Chauffer un bon filet d'huile dans une grande po{_ea}le ou un wok {_a} "
        f"feu moyen-vif. Y faire dorer les b{_e2}tonnets d'aubergine par petites "
        f"quantit{_e}s pour qu'ils colorent bien sans bouillir. R{_e}server sur "
        f"une assiette.",
        f"Dans la m{_ea}me po{_ea}le, verser un petit filet d'huile si n{_e}cessaire. "
        f"Faire revenir l'ail finement hach{_e} 30 secondes, puis ajouter la "
        f"chair {_a} saucisse en l'{_e}miettant {_a} la spatule. La faire revenir "
        f"jusqu'{_a} ce qu'elle soit bien dor{_e}e et l{_e}g{_e8}rement croustillante.",
        f"Ajouter la sauce soja, le sucre et le vinaigre. M{_e}langer rapidement, "
        f"puis verser un petit verre d'eau (environ 80 ml). Porter {_a} fr{_e}missement.",
        f"Remettre les aubergines dans la po{_ea}le, m{_e}langer d{_e}licatement "
        f"pour les enrober de sauce. Baisser le feu, couvrir et laisser mijoter "
        f"8 {_a} 10 minutes, jusqu'{_a} ce que les aubergines soient fondantes "
        f"et la viande bien impr{_e}gn{_e}e de sauce. Si la sauce est trop "
        f"abondante, faire r{_e}duire 2 minutes {_a} d{_e}couvert.",
        f"Servir bien chaud avec un grand bol de riz blanc.",
    ]
    r08_astuce = (
        f"Si tu veux utiliser moins d'huile, passe les aubergines 5 minutes au "
        f"micro-ondes avant de les po{_ea}ler : elles absorberont moins de "
        f"mati{_e8}re grasse."
    )
    r08_footer = f"Aubergines mijot{_e}es {_a} la chair {_a} saucisse"

    # ---- RECIPE 09: Galettes de pommes de terre façon chinoise ----
    r09_why = (
        f"Peu d'ingr{_e}dients, beaucoup de r{_e}confort. Ces galettes sont "
        f"croustillantes dehors, tendres dedans, et assez nourrissantes pour "
        f"un repas rapide ou un d{_e8}ner l{_e}ger."
    )
    r09_diff = f"Tr{_e8}s facile"
    r09_temps = f"12 min + 12 min\ncuisson"
    r09_ingredients = [
        f"2 pommes de terre moyennes",
        f"2 c. {_a} soupe de farine",
        f"1 ciboule ou un peu d'oignon nouveau",
        f"Sel, poivre",
        f"Huile pour la po{_ea}le",
    ]
    r09_substitutions = [
        f"La ciboule peut {_ea}tre remplac{_e}e par de la ciboulette, de "
        f"l'oignon {_e}minc{_e} ou du poireau tr{_e8}s fin.",
        f"La farine de bl{_e} classique suffit.",
        f"Un peu de paprika peut donner une couleur plus chaude.",
    ]
    r09_steps = [
        f"{_E}plucher les pommes de terre et les r{_e2}per avec une r{_e2}pe "
        f"{_a} gros trous, ou les couper en tr{_e8}s fines lamelles au couteau. "
        f"Plus les morceaux sont fins, plus les galettes seront croustillantes.",
        f"Presser l{_e}g{_e8}rement les pommes de terre r{_e2}p{_e}es entre les "
        f"mains ou dans un torchon propre pour retirer l'exc{_e8}s d'eau, sans "
        f"les s{_e}cher compl{_e8}tement — il faut qu'il reste un peu "
        f"d'amidon pour lier le tout.",
        f"Dans un saladier, m{_e}langer les pommes de terre avec la farine, la "
        f"ciboule finement {_e}minc{_e}e, une bonne pinc{_e}e de sel et du "
        f"poivre. M{_e}langer jusqu'{_a} obtenir une p{_e2}te homog{_e8}ne qui "
        f"se tient.",
        f"Chauffer une po{_ea}le g{_e}n{_e}reusement huil{_e}e {_a} feu moyen. "
        f"D{_e}poser des petites cuiller{_e}es de p{_e2}te et les aplatir {_a} "
        f"la spatule pour former des galettes fines et r{_e}guli{_e8}res.",
        f"Cuire 5 {_a} 6 minutes par c{_o}t{_e}, sans les retourner trop t{_o}t, "
        f"jusqu'{_a} ce que les bords soient bien dor{_e}s et croustillants. "
        f"{_E}goutter sur du papier absorbant.",
        f"Servir imm{_e}diatement, nature ou avec une petite sauce soja-vinaigre.",
    ]
    r09_astuce = (
        f"Fais des galettes petites plut{_o}t qu'une grande : elles se retournent "
        f"plus facilement et deviennent plus croustillantes."
    )
    r09_footer = f"Galettes de pommes de terre fa{_c}on chinoise"

    # ---- RECIPE 10: {_OE}ufs brouillés à la tomate sur riz ----
    r10_why = (
        f"C'est l'une des portes d'entr{_e}e les plus simples vers la cuisine "
        f"familiale chinoise. Des {_oe}ufs, des tomates, du riz : rien de "
        f"spectaculaire, mais exactement le genre de plat qui r{_e}pare une "
        f"journ{_e}e longue."
    )
    r10_diff = f"Tr{_e8}s facile"
    r10_temps = f"10 min + 10 min\ncuisson"
    r10_ingredients = [
        f"2 tomates m{_u}res",
        f"3 {_oe}ufs",
        f"1 bol de riz cuit",
        f"Sel",
        f"1 petite pinc{_e}e de sucre",
        f"Sauce soja (optionnelle)",
        f"Huile pour la po{_ea}le",
    ]
    r10_substitutions = [
        f"Des tomates cerises coup{_e}es en deux donnent une sauce plus sucr{_e}e.",
        f"En hiver, une tomate fra{_e8}che avec un peu de coulis peut mieux "
        f"fonctionner.",
        f"La sauce soja est optionnelle : le plat peut rester tr{_e8}s doux.",
    ]
    r10_steps = [
        f"Battre les {_oe}ufs dans un bol avec une pinc{_e}e de sel. Ne pas "
        f"trop battre : quelques filets de blanc doivent encore {_ea}tre visibles.",
        f"Couper les tomates en quartiers, puis chaque quartier en deux pour "
        f"obtenir des morceaux de taille moyenne.",
        f"Chauffer un filet d'huile dans une po{_ea}le {_a} feu vif. Quand "
        f"l'huile est bien chaude, verser les {_oe}ufs battus. Les laisser "
        f"prendre 15 secondes sans y toucher, puis les brouiller rapidement "
        f"en les cassant en gros morceaux moelleux. Les retirer de la po{_ea}le "
        f"d{_e8}s qu'ils sont encore l{_e}g{_e8}rement humides — ils finiront "
        f"de cuire plus tard.",
        f"Dans la m{_ea}me po{_ea}le, verser les tomates avec une pinc{_e}e de "
        f"sucre (le sucre {_e}quilibre l'acidit{_e} des tomates). Faire revenir "
        f"2 {_a} 3 minutes en remuant de temps en temps, jusqu'{_a} ce que les "
        f"tomates commencent {_a} rendre leur jus et deviennent l{_e}g{_e8}rement "
        f"compot{_e}es.",
        f"Remettre les {_oe}ufs dans la po{_ea}le et m{_e}langer d{_e}licatement "
        f"pendant 30 secondes {_a} 1 minute. Les {_oe}ufs vont absorber un peu "
        f"du jus de tomate.",
        f"Servir imm{_e}diatement sur un bol de riz blanc bien chaud.",
    ]
    r10_astuce = (
        f"Ne cuis pas trop les {_oe}ufs au premier passage. Ils finiront de "
        f"cuire avec la tomate et resteront plus tendres."
    )
    r10_footer = f"{_OE}ufs brouill{_e}s {_a} la tomate sur riz"

    # ==================== RENDER ALL RECIPES ====================
    recipes = [
        (1, "Congee aux travers de porc", r01_why, r01_diff, r01_temps,
         r01_ingredients, r01_substitutions, r01_steps, r01_astuce, r01_footer),
        (2, f"Poulet mijot{_e} fa{_c}on Huangmenji", r02_why, r02_diff, r02_temps,
         r02_ingredients, r02_substitutions, r02_steps, r02_astuce, r02_footer),
        (3, "Poulet aux champignons de Paris", r03_why, r03_diff, r03_temps,
         r03_ingredients, r03_substitutions, r03_steps, r03_astuce, r03_footer),
        (4, f"Poulet effiloch{_e} sauce gingembre-ciboule", r04_why, r04_diff,
         r04_temps, r04_ingredients, r04_substitutions, r04_steps, r04_astuce,
         r04_footer),
        (5, f"Riz saut{_e} {_a} la saucisse", r05_why, r05_diff, r05_temps,
         r05_ingredients, r05_substitutions, r05_steps, r05_astuce, r05_footer),
        (6, f"Chaussons chinois {_a} la p{_e2}te bris{_e}e", r06_why, r06_diff,
         r06_temps, r06_ingredients, r06_substitutions, r06_steps, r06_astuce,
         r06_footer),
        (7, f"Nouilles saut{_e}es aux spaghetti", r07_why, r07_diff, r07_temps,
         r07_ingredients, r07_substitutions, r07_steps, r07_astuce, r07_footer),
        (8, f"Aubergines mijot{_e}es {_a} la chair {_a} saucisse", r08_why,
         r08_diff, r08_temps, r08_ingredients, r08_substitutions, r08_steps,
         r08_astuce, r08_footer),
        (9, f"Galettes de pommes de terre fa{_c}on chinoise", r09_why, r09_diff,
         r09_temps, r09_ingredients, r09_substitutions, r09_steps, r09_astuce,
         r09_footer),
        (10, f"{_OE}ufs brouill{_e}s {_a} la tomate sur riz", r10_why, r10_diff,
         r10_temps, r10_ingredients, r10_substitutions, r10_steps, r10_astuce,
         r10_footer),
    ]

    for recipe in recipes:
        pdf.recipe_page(*recipe)

    # ==================== CONCLUSION ====================
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font('C', 'B', 20)
    pdf.set_text_color(180, 40, 40)
    pdf.cell(0, 12, 'CONCLUSION', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('C', 'B', 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Ce que nous avons appris", 0, 1, 'C')
    pdf.ln(8)

    pdf.set_font('C', '', 11)
    pdf.set_text_color(60, 60, 60)
    lines = [
        "La cuisine interculturelle ne consiste pas seulement",
        f"{_a} importer des ingr{_e}dients exotiques.",
        "",
        "Elle peut aussi na{_ea}tre de substitutions locales,",
        f"de contraintes budg{_e}taires et de cr{_e}ativit{_e} {_e}tudiante.",
        "",
        f"L'IFC propose une mani{_e8}re simple de rendre la cuisine",
        f"chinoise plus accessible, plus locale et plus durable.",
    ]
    for line in lines:
        if line:
            pdf.cell(0, 7, line, 0, 1, 'C')
        else:
            pdf.ln(4)

    pdf.ln(20)
    pdf.set_font('C', 'I', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "Ce que nous avons appris", 0, 1, 'R')

    # ==================== SAVE ====================
    output_path = r'C:\Users\Lenovo\Desktop\le-wok-du-coin-modifie.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')
    return output_path


if __name__ == '__main__':
    build_pdf()

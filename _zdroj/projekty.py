#!/usr/bin/env python3
"""Generátor stránek projektů.

Každý projekt má vlastní stránku ve stejném vzhledu jako middleware.html.
Obsah je v seznamu PROJEKTY níže, šablona v render_page().

Spuštění z kořene repozitáře:
    python3 _zdroj/projekty.py

Vytvoří/přepíše soubory <slug>.html v kořeni a obnoví blok
„Další projekty“ v middleware.html (mezi značkami DALSI-PROJEKTY).
Složky začínající podtržítkem GitHub Pages nezveřejňuje.
"""

import json
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
WEB = "https://zdenekstuksa.cz"
QR = (Path(__file__).parent / "qr-ilustrace.txt").read_text(encoding="utf-8")

# pořadí = pořadí v navigaci „předchozí / další“
PORADI = [
    ("middleware.html", "Middleware Ventilek"),
    ("kompresory-vzduchotechnika.html", "Kompresory-Vzduchotechnika.cz"),
    ("zakaznicka-aplikace.html", "Zákaznická aplikace"),
    ("sablona-eshopu.html", "Šablona e-shopu"),
    ("newslettery.html", "AI newslettery"),
    ("parovani-katalogu.html", "Párování katalogu"),
    ("martin-kuska.html", "Martin Kuška"),
    ("dundee-agency.html", "Dundee Agency"),
    ("pro-jachting.html", "Pro-jachting.cz"),
    ("ucetni-kancelar.html", "Účetní kancelář"),
    ("kvit.html", "Kvit"),
    ("najedno.html", "NaJedno"),
]

# ---------- drobné stavební kameny ----------


def shot(src, alt, bar, w=1280, h=800, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        f'<figure class="shot"><div class="shot__bar" aria-hidden="true"><i></i><i></i><i></i>'
        f"<span>{bar}</span></div>"
        f'<img src="assets/{src}" alt="{alt}" width="{w}" height="{h}" {load}></figure>'
    )


def phone(src, alt, eager=False, tag="figure"):
    load = "" if eager else ' loading="lazy"'
    return f'<{tag} class="phone"><img src="assets/{src}" alt="{alt}" width="600" height="1022"{load}></{tag}>'


def stage(desk, desk_alt, bar, mob, mob_alt, h=800):
    return (
        '<div class="pj-stage">'
        + shot(desk, desk_alt, bar, h=h, eager=True)
        + phone(mob, mob_alt, eager=True)
        + "</div>"
    )


def phones(items, note):
    inner = "".join(phone(s, a, eager=True) for s, a in items)
    return f'<div class="phones">{inner}<p class="phones__note">{note}</p></div>'


def ikona(d):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'


IKONY = {
    "klic": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
    "balik": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="m3 7.5 9 4.5 9-4.5M12 12v9"/>',
    "doklad": '<path d="M6 3h9l3 3v15H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "hvezda": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
}

# ---------- vizuály v úvodu jednotlivých projektů ----------

VIZ_ESHOP = stage(
    "eshop-uvod.webp",
    "Úvodní stránka e-shopu Kompresory-Vzduchotechnika.cz",
    "kompresory-vzduchotechnika.cz",
    "eshop-mobil.webp",
    "E-shop Kompresory-Vzduchotechnika.cz v mobilu",
)

VIZ_APLIKACE = f"""<div class="notify">
            {phone("aplikace-prihlaseni.webp", "Zákaznická aplikace: přihlášení kódem z e-mailu", eager=True)}
            <ul class="toasts" aria-label="Ukázka oznámení v aplikaci">
              <li><span class="ticon">{ikona(IKONY["klic"])}</span><span>Přihlašovací kód<small>šest číslic do e-mailu, žádné heslo</small></span></li>
              <li><span class="ticon">{ikona(IKONY["balik"])}</span><span>Zásilka je na cestě<small>sledování přímo v aplikaci</small></span></li>
              <li><span class="ticon">{ikona(IKONY["doklad"])}</span><span>Faktura ke stažení<small>doklady v PDF</small></span></li>
              <li><span class="ticon">{ikona(IKONY["hvezda"])}</span><span>Oblíbené zboží<small>rychlý opakovaný nákup</small></span></li>
            </ul>
          </div>
          <p class="pj-note">Přihlašovací obrazovka je skutečná, oznámení vedle ní jsou ilustrace.</p>"""

VIZ_SABLONA = """<div class="mock">
            <p class="mock__bar"><span class="vlog__dot" aria-hidden="true"></span>Košík · násobky balení</p>
            <div class="mock__row">
              <div>Hadice na stlačený vzduch<small>prodává se po 100 m</small></div>
              <span class="stepper" data-stepper data-step="100" data-max="500" data-unit=" m" aria-hidden="true"><b>−</b><output>100 m</output><b>+</b></span>
            </div>
            <div class="mock__row"><div>Množství jen po celých baleních<small>jinak se objednávka musí opravovat ručně</small></div><span class="mock__ok">hlídá ✓</span></div>
          </div>
          <div class="mock">
            <p class="mock__bar">Noční kontrola</p>
            <div class="mock__row"><div>Stránky produktových řad<small>každou noc automaticky</small></div><span class="mock__ok">v pořádku ✓</span></div>
            <div class="mock__row"><div>Upozornění do mobilu<small>jen když něco nesedí</small></div><span class="mock__wait">připraveno</span></div>
          </div>
          <div class="mock">
            <p class="mock__bar">Produkty v článku · posun stránky na mobilu</p>
            <div class="meter">
              <div class="meter__row"><span>dřív</span><span class="meter__track"><span class="meter__fill" style="width: 95%"></span></span><strong>0,95</strong></div>
              <div class="meter__row"><span>teď</span><span class="meter__track"><span class="meter__fill meter__fill--ok" style="width: 3%"></span></span><strong>0,027</strong></div>
            </div>
          </div>
          <p class="pj-note">Ilustrace funkcí šablony. Čísla posunu stránky jsou skutečná měření.</p>"""

VIZ_NEWSLETTERY = """<div class="mock">
            <p class="mock__bar"><span class="vlog__dot" aria-hidden="true"></span>Jedna kampaň · tři formáty</p>
            <div class="formats">
              <figure class="format format--45"><div class="format__art"><b>Novinka měsíce</b><i></i><i></i></div><figcaption>1080 × 1350</figcaption></figure>
              <figure class="format format--11"><div class="format__art"><b>Novinka měsíce</b><i></i><i></i></div><figcaption>1080 × 1080</figcaption></figure>
              <figure class="format format--916"><div class="format__art"><b>Novinka měsíce</b><i></i><i></i></div><figcaption>1080 × 1920</figcaption></figure>
            </div>
            <div class="channels"><span>E-mail</span><span>Facebook</span><span>Instagram</span><span>Stories</span><span>LinkedIn</span></div>
          </div>
          <p class="pj-note">Ilustrace formátů, ne skutečná grafika kampaně.</p>"""


def match_row(nas, dod, d, none=False):
    cls = " match__row--none" if none else ""
    score = "—" if none else "✓"
    return (
        f'<div class="match__row{cls}"><code>{nas}</code>'
        f'<span class="match__line" style="--d: {d}s"></span>'
        f'<code>{dod}</code><span class="match__score">{score}</span></div>'
    )


VIZ_PAROVANI = (
    '<div class="mock match" aria-label="Ilustrace párování kódů">'
    '<p class="mock__bar"><span class="vlog__dot" aria-hidden="true"></span>Párování podle výkresů a parametrů</p>'
    '<div class="match__head"><span>Náš kód</span><span></span><span>Dodavatel</span><span></span></div>'
    + match_row("ŠR-G1/4-8", "SV 08-R14", 0)
    + match_row("ŠR-G3/8-10", "SV 10-R38", 0.5)
    + match_row("KOL-G1/2-12", "WV 12-R12", 1)
    + match_row("T-G1/4-6", "TV 06-R14", 1.5)
    + match_row("RED-G3/8-1/4", "bez protějšku", 0, none=True)
    + '<div class="mock__row"><div>Zapsáno do ABRA Flexi<small>přes API, bez ručního přepisování</small></div>'
    '<span class="mock__ok">468 vazeb ✓</span></div></div>'
    '<p class="pj-note">Ilustrace s vymyšlenými kódy. Počet vazeb je skutečný.</p>'
)

VIZ_KUSKA = stage(
    "kuska-uvod.webp",
    "Návrh webu Martina Kušky: úvodní stránka",
    "Martin Kuška · návrh webu",
    "kuska-mobil.webp",
    "Návrh webu Martina Kušky v mobilu",
) + '<p class="pj-note">Snímky z rozpracované verze webu.</p>'

VIZ_DUNDEE = f"""<div class="mock">
            <p class="mock__bar"><span class="vlog__dot" aria-hidden="true"></span>Administrace · poptávky</p>
            <div class="board">
              <div class="board__col"><h4>Nové</h4><div class="board__card is-moving">Svatba<small>červen · 80 hostů</small></div><div class="board__card">Firemní večírek<small>prosinec</small></div></div>
              <div class="board__col"><h4>V jednání</h4><div class="board__card">Narozeninová oslava<small>září · 40 hostů</small></div></div>
              <div class="board__col"><h4>Potvrzeno</h4><div class="board__card">Svatba<small>srpen</small></div><div class="board__card">Večírek<small>listopad</small></div></div>
            </div>
          </div>
          <div class="mock">
            <div class="ticket"><div><small>Vstupenka</small><strong>Večerní akce</strong><span>Zaplaceno QR platbou ✓</span></div>{QR}</div>
          </div>
          <p class="pj-note">Ilustrace funkcí, ne snímek webu. Web je zatím návrh.</p>"""

VIZ_JACHTING = """<div class="mock">
            <p class="mock__bar"><span class="vlog__dot" aria-hidden="true"></span>Akční nabídka</p>
            <p class="offer__title">Plavba · akční termín</p>
            <div class="countdown" data-countdown data-hours="62" aria-label="Ukázka odpočtu do konce nabídky">
              <span><b data-d>2</b>dny</span><span><b data-h>14</b>hod</span><span><b data-m>00</b>min</span><span><b data-s>00</b>s</span>
            </div>
            <div class="seats" aria-label="Volná místa: 3 z 8"><i></i><i></i><i></i><i></i><i></i><i class="is-free"></i><i class="is-free"></i><i class="is-free"></i><span>volná místa 3 z 8</span></div>
          </div>
          <div class="mock" data-campaign data-on="Nabídka běží · kampaň běží" data-off="Vyprodáno · kampaň se sama pozastavila">
            <p class="mock__bar">Reklama v Google Ads a Skliku</p>
            <span class="switch"><i aria-hidden="true"></i><span data-campaign-text>Nabídka běží · kampaň běží</span></span>
          </div>
          <p class="pj-note">Ilustrace funkcí, ne snímek webu. Web je zatím návrh.</p>"""

VIZ_UCETNI = """<div class="mock">
            <div class="guard">
              <svg viewBox="0 0 48 56" aria-hidden="true"><path d="M24 3 44 10v16c0 13-9 22-20 27C13 48 4 39 4 26V10z"/><path d="m16 28 6 6 11-12"/></svg>
              <div><strong data-count="167796">167 796</strong><span>zablokovaných pokusů o přihlášení, které našel bezpečnostní audit serveru</span></div>
            </div>
          </div>
          <div class="mock">
            <p class="mock__bar">Klientský portál</p>
            <div class="mock__row"><div>Pozvánka pro nového klienta<small>účty zakládá kancelář, ne kdokoli z internetu</small></div><span class="mock__ok">odesláno ✓</span></div>
            <div class="mock__row"><div>Formulář s podklady<small>klient vyplní online</small></div><span class="mock__wait">čeká</span></div>
          </div>
          <p class="pj-note">Ilustrace portálu. Počet pokusů je skutečný údaj z auditu.</p>"""

VIZ_KVIT = phones(
    [
        ("kvit-skupiny.webp", "Kvit: seznam skupin"),
        ("kvit-prehled.webp", "Kvit: přehled skupiny s bilancí členů"),
        ("kvit-vyrovnani.webp", "Kvit: kdo komu kolik pošle, s QR platbou"),
    ],
    "Snímky s ukázkovými daty.",
)

VIZ_NAJEDNO = phones(
    [
        ("najedno-domu.webp", "NaJedno: úvodní obrazovka s tajným hlasováním"),
        ("najedno-setkani.webp", "NaJedno: setkání s nápojovým lístkem"),
        ("najedno-pas.webp", "NaJedno: pas s razítky a odznaky"),
    ],
    "Snímky z návrhu vinné verze appky. Pas a odznaky jsou zatím jen v návrhu.",
)

# ---------- výzvy na konci stránky ----------

CTA_FIRMA = (
    "Chcete něco podobného pro svůj e-shop?",
    "Napište mi, co vás nejvíc zdržuje. Podívám se, co by šlo zjednodušit, propojit nebo zautomatizovat.",
)
CTA_WEB = (
    "Potřebujete web, který pro vás bude pracovat?",
    "Postavím ho na míru, včetně administrace, kterou zvládnete sami. Začínám vždycky tím, co lidé opravdu hledají.",
)
CTA_APP = (
    "Máte nápad na aplikaci?",
    "Rád pomůžu z nápadu udělat aplikaci, kterou budou lidé opravdu používat.",
)

# ---------- obsah ----------

PROJEKTY = [
    dict(
        slug="kompresory-vzduchotechnika.html",
        title="Kompresory-Vzduchotechnika.cz",
        desc="Rodinný e-shop se stlačeným vzduchem v pěti jazycích, který vede Zdeněk Štuksa. Poradenství, B2B ceníky, kalkulačky a vlastní systémy pod povrchem.",
        eyebrow="Vlastní firma · e-shop od roku 2012",
        h1="Kompresory-<wbr>Vzduchotechnika.cz",
        h1_long=True,
        lead="Rodinný e-shop, který vedu. Kompresory, úprava vzduchu, rozvody a pneumatika na jednom místě, v pěti jazycích, s prodejnou a servisem v Žebráku. Je to místo, kde všechno, co umím, nejdřív vyzkouším na sobě.",
        meta=["Shoptet Premium", "5 jazyků", "prodejna Žebrák", "B2B ceníky"],
        actions=[("Otevřít e-shop ↗", "https://www.kompresory-vzduchotechnika.cz/")],
        visual=VIZ_ESHOP,
        stats=[
            ("4,8 z 5", "hodnocení od 1 149 zákazníků"),
            ("5", "jazykových verzí"),
            ("20 000+", "položek v katalogu"),
            ("od 2010", "v oboru stlačeného vzduchu"),
        ],
        zadani_h2="Specializovaný e-shop s malým týmem",
        zadani=[
            ("Technický sortiment", "Zákazník často neví, jaký kompresor nebo filtr potřebuje. Bez poradenství by koupil špatně, nebo by nekoupil vůbec."),
            ("Firmy i domácnosti", "Firmy chtějí své ceny a objednávky po celých baleních, domácí kutil zase jednoduchý nákup a rychlou dopravu."),
            ("Pět zemí", "Přes 20 000 položek v pěti jazycích. Ručně se to přeložit ani udržovat nedá."),
        ],
        reseni="E-shop běží na <strong>Shoptetu</strong>, ale všechno kolem jsem si postavil sám: vlastní šablonu, middleware, který ho propojuje s účetnictvím a dalšími službami, a aplikaci pro zákazníky.",
        moduly_h2="Co na e-shopu najdete",
        moduly=[
            ("Pět jazykových verzí", "Čeština, slovenština, polština, angličtina a němčina. Texty překládá AI v middlewaru a nové zboží je hned ve všech jazycích.", "Prodáváme i do zahraničí bez překladatelské agentury."),
            ("Poradna a kalkulačky", "Články v poradně, kalkulačka výběru kompresoru a průvodce sestavením úpravy vzduchu od kompresoru až po spotřebič.", "Zákazník si vybere správně sám."),
            ("Ceníky pro firmy", "Firemní zákazníci mají své ceníky a minimální množství podle toho, po kolika kusech se zboží prodává.", "Firma vidí své ceny hned po přihlášení."),
            ("Prodejna a servis", "Kamenná prodejna v Žebráku. Poradíme s výběrem, navrhneme rozvod, dohlédneme na instalaci a postaráme se o pravidelný servis.", "Jeden partner od výběru až po servis."),
        ],
        pod_povrchem=[
            ("middleware.html", "Middleware Ventilek", "Propojuje e-shop s účetnictvím a dvaceti dalšími službami."),
            ("sablona-eshopu.html", "Vlastní šablona", "Vzhled, košík a noční kontroly e-shopu."),
            ("zakaznicka-aplikace.html", "Zákaznická aplikace", "Objednávky, zásilky a doklady v mobilu."),
        ],
        galerie=[
            ("shot", "eshop-uvod.webp", "Úvodní stránka: poradenství, hodnocení a doprava zdarma hned nahoře.", "kompresory-vzduchotechnika.cz", 800),
            ("shot", "eshop-kategorie.webp", "Kategorie Úprava vzduchu s odkazem na sestavení celé trasy.", "kompresory-vzduchotechnika.cz/uprava-vzduchu/", 800),
            ("phone", "eshop-mobil.webp", "E-shop v mobilu."),
        ],
        tech="Shoptet Premium · vlastní šablona · ABRA Flexi · middleware Ventilek · Zásilkovna · Ecomail · Heureka · Zboží.cz",
        cta=CTA_FIRMA,
        fakta=[("Stav", "Běží"), ("Od", "2012, značka od 2010"), ("Kde", "Žebrák a online v pěti zemích")],
    ),
    dict(
        slug="zakaznicka-aplikace.html",
        title="Zákaznická aplikace",
        desc="Aplikace do mobilu pro zákazníky Kompresory-Vzduchotechnika.cz: přihlášení kódem z e-mailu, objednávky, zásilky, doklady v PDF a reklamace.",
        eyebrow="Vlastní firma · v provozu od října 2026",
        h1="Zákaznická aplikace",
        lead="Aplikace do mobilu pro zákazníky našeho e-shopu. Bez hesla: zákazník zadá e-mail, dostane šestimístný kód a vidí své objednávky, zásilky, doklady i reklamace. Instaluje se přímo z prohlížeče, bez obchodu s aplikacemi.",
        meta=["PWA", "push oznámení", "bez hesla", "B2B přehled"],
        actions=[("Otevřít aplikaci ↗", "https://app.kompresory-vzduchotechnika.cz/")],
        visual=VIZ_APLIKACE,
        stats=[
            ("6 číslic", "místo hesla"),
            ("48", "automatických testů přihlášení"),
            ("18", "kontrol po každém nasazení"),
            ("PWA", "instalace z prohlížeče"),
        ],
        zadani_h2="Méně telefonátů, víc přehledu",
        zadani=[
            ("Kde je můj balík?", "Nejčastější dotazy zákazníků byly o stavu objednávky, faktuře nebo reklamaci. Odpovídal na ně člověk."),
            ("Hesla se zapomínají", "Klasický účet s heslem je pro řadu zákazníků překážka. Heslo zapomenou a nakoupí jinde."),
        ],
        reseni="Aplikace bere data z <strong>middlewaru</strong>, takže zákazník vidí totéž co my: objednávku, zásilku, doklady i reklamace. Přihlášení je jednorázovým kódem z e-mailu.",
        moduly_h2="Co aplikace umí",
        moduly=[
            ("Přihlášení kódem z e-mailu", "Žádné heslo. Aplikace navíc neprozradí, jestli zadaný e-mail u nás nakupuje, takže se přes ni nedá zjišťovat, kdo je náš zákazník.", "Bezpečné a jednoduché i pro lidi, kteří hesla nemají rádi."),
            ("Objednávky a zásilky", "Přehled objednávek se sledováním zásilky.", "Méně telefonátů „kde je můj balík“."),
            ("Doklady v PDF", "Faktury a další doklady ke stažení přímo v mobilu.", "Účetní zákazníka má doklad hned."),
            ("Reklamace", "Přehled reklamací a jejich stavu na jednom místě.", "Zákazník ví, jak jeho reklamace pokračuje."),
            ("Oblíbené a seznamy", "Oblíbené zboží a nákupní seznamy pro opakované nákupy.", "Pravidelný materiál objednáte na pár klepnutí."),
            ("Přehled pro firmy a oznámení", "Firmy mají přehled svých nákupů. Aplikace posílá oznámení do mobilu, sama se aktualizuje a má návod na instalaci.", "Vždy aktuální verze bez starostí."),
        ],
        tech="PWA · push oznámení · napojení přes middleware Ventilek · automatické testy",
        cta=CTA_FIRMA,
        fakta=[("Stav", "Běží od října 2026"), ("Pro", "zákazníky Kompresory-Vzduchotechnika.cz"), ("Instalace", "z prohlížeče, bez obchodu")],
    ),
    dict(
        slug="sablona-eshopu.html",
        title="Vlastní šablona e-shopu",
        desc="Vlastní šablona e-shopu na Shoptet Blank v pěti jazycích: košík hlídá násobky balení, noční kontroly, kalkulačky a produkty v článcích.",
        eyebrow="Vlastní firma · běží od července 2026",
        h1="Vlastní šablona e-shopu",
        lead="Vzhled a chování e-shopu jsem postavil na šabloně Shoptet Blank, kterou lze upravit do posledního detailu. Běží v pěti jazycích a stará se o to, aby se e-shop dobře používal, rychle načítal a sám hlásil chyby.",
        meta=["Shoptet Blank", "5 jazyků", "noční kontroly", "kalkulačky"],
        actions=[("Prohlédnout na e-shopu ↗", "https://www.kompresory-vzduchotechnika.cz/")],
        visual=VIZ_SABLONA,
        stats=[
            ("5", "jazykových verzí"),
            ("0,027", "posun stránky s produkty na mobilu, dřív 0,95"),
            ("každou noc", "automatická kontrola stránek"),
            ("GPSR", "údaje výrobců podle EU"),
        ],
        zadani_h2="Hotová šablona nestačila",
        zadani=[
            ("Zboží po baleních", "Spoustu zboží prodáváme jen po celých baleních. Hotová šablona to nehlídala a objednávky se musely opravovat."),
            ("Chyby nikdo nevidí", "Když se na stránce něco rozbije, často si toho první všimne zákazník."),
            ("Technické poradenství", "Zákazník potřebuje kalkulačky a články s produkty, ne jen výpis zboží."),
        ],
        reseni="Šablonu jsem napsal na <strong>Shoptet Blank</strong> a propojil ji s middlewarem, který jí dodává data pro kalkulačky a ceníky.",
        moduly_h2="Co šablona umí",
        moduly=[
            ("Košík hlídá násobky balení", "Zboží, které se prodává po celých baleních, jde objednat jen v násobcích. Údaje bere z účetnictví.", "Žádné opravy objednávek a dovolávání zákazníkům."),
            ("Noční kontroly", "Každou noc automaticky projde stránky produktových řad. Když něco nesedí, pošle upozornění do mobilu.", "Chybu najdeme dřív než zákazník."),
            ("Kalkulačky", "Moduly kalkulaček přímo v šabloně. Data pro ně sestavuje middleware z katalogu.", "Zákazník si vybere stroj nebo filtr sám."),
            ("Produkty v článcích", "Boxy s produkty přímo v článcích poradny. Na mobilu se stránka při načítání neposouvá: posun klesl z 0,95 na 0,027.", "Čtenář nakoupí rovnou z článku a Google stránku nepenalizuje."),
            ("Připravenost na AI nákupy", "Kontrola produktového feedu pro nákupy přes AI asistenty.", "Produkty najdou i lidé, kteří nakupují přes chatovací asistenty."),
            ("Údaje výrobců podle GPSR", "Povinné údaje o výrobci u produktů podle evropského nařízení o bezpečnosti výrobků.", "E-shop splňuje nové evropské povinnosti."),
        ],
        tech="Shoptet Blank · JavaScript · CSS · 5 jazyků · napojení na middleware Ventilek",
        cta=CTA_FIRMA,
        fakta=[("Stav", "Běží od července 2026"), ("Pro", "Kompresory-Vzduchotechnika.cz"), ("Postaveno na", "Shoptet Blank")],
    ),
    dict(
        slug="newslettery.html",
        title="AI newslettery a kampaně",
        desc="Kampaně pro zhruba 10 800 odběratelů: šablony v Ecomailu, AI texty pro všechny kanály a grafiky generované automaticky ve třech formátech.",
        eyebrow="Vlastní firma · marketing",
        h1="AI newslettery a kampaně",
        lead="Kampaně pro zhruba 10 800 odběratelů. AI připraví texty pro e-mail i sociální sítě a grafiky se generují samy ve třech formátech. Co se pošle, rozhoduju já.",
        meta=["Ecomail", "AI texty", "automatické grafiky", "UTM"],
        actions=[],
        visual=VIZ_NEWSLETTERY,
        stats=[
            ("~10 800", "odběratelů newsletteru"),
            ("99,5–99,7 %", "doručených e-mailů"),
            ("16–17 %", "otevření"),
            ("1–1,5 %", "prokliků"),
        ],
        stats_note="Výsledky kampaní z července 2026.",
        zadani_h2="Jedna kampaň, pět kanálů",
        zadani=[
            ("Hodně formátů", "Newsletter, příspěvek, čtverec, Stories, LinkedIn. Každý kanál chce jiný text a jiný rozměr grafiky."),
            ("Málo času", "Ruční příprava jedné kampaně do všech kanálů zabrala půl dne."),
        ],
        reseni="Postavil jsem postup, kde <strong>AI připraví texty i grafiky</strong> pro všechny kanály naráz. Já vyberu téma, zkontroluju výsledek a pošlu.",
        moduly_h2="Co postup umí",
        moduly=[
            ("Šablony v Ecomailu", "Jednotný vzhled všech newsletterů, který se nemusí pokaždé skládat znovu.", "Kampaň vypadá profesionálně za pár minut."),
            ("Grafiky ve třech formátech", "1080 × 1350 pro příspěvky, 1080 × 1080 pro čtverec a 1080 × 1920 pro Stories. Generují se automaticky.", "Jedna kampaň má hotové podklady pro všechny sítě."),
            ("Texty pro každý kanál", "E-mail, Facebook, Instagram, Stories a LinkedIn. Každý ve správné délce a tónu.", "Žádné kopírování jednoho textu všude."),
            ("Měření", "Každý odkaz má označení kanálu (UTM), takže v analytice je vidět, odkud přišly návštěvy a objednávky.", "Víme, který kanál opravdu prodává."),
        ],
        postup=[
            ("Vyberu téma", "Novinka, akce nebo rada z poradny. A produkty, které k tomu patří."),
            ("AI připraví podklady", "Texty pro všechny kanály a grafiky ve třech formátech."),
            ("Zkontroluju a pošlu", "Co jde ven, vždycky projde mýma rukama."),
        ],
        tech="Ecomail · AI texty · generované grafiky · UTM · Google Analytics 4",
        cta=CTA_FIRMA,
        fakta=[("Stav", "Používá se"), ("Pro", "Kompresory-Vzduchotechnika.cz"), ("Kanály", "e-mail, Facebook, Instagram, LinkedIn")],
    ),
    dict(
        slug="parovani-katalogu.html",
        title="Párování katalogu dodavatelů",
        desc="AI porovnala stovky šroubení podle výkresů a parametrů s katalogem dodavatele a zapsala 468 vazeb rovnou do ABRA Flexi.",
        eyebrow="Vlastní firma · nákup",
        h1="Párování katalogu dodavatelů",
        lead="Stovky šroubení a fitinků jsme měli u dvou dodavatelů pod různými kódy. AI je porovnala podle technických výkresů a parametrů a hotové vazby zapsala rovnou do účetnictví ABRA Flexi.",
        meta=["AI", "ABRA Flexi API", "technické výkresy"],
        actions=[],
        visual=VIZ_PAROVANI,
        stats=[
            ("512", "prověřených položek"),
            ("468", "vazeb zapsaných do ABRY"),
            ("45", "podkategorií"),
            ("přes API", "zápis rovnou do ABRA Flexi"),
        ],
        zadani_h2="Stejný díl, jiný kód",
        zadani=[
            ("Každý dodavatel po svém", "Stejné šroubení má u každého dodavatele jiný kód i jiný popis. Bez vazby se musí při každé objednávce dohledávat."),
            ("Ruční párování trvá týdny", "Každý díl má závit, rozměr, materiál a tvar. Porovnat stovky dílů ručně je práce na týdny a snadno se splete."),
        ],
        reseni="AI dostala <strong>výkresy a parametry</strong> obou katalogů, porovnala je a vazby se zapsaly přes API přímo do karet v ABŘE.",
        moduly_h2="Co to přineslo",
        moduly=[
            ("Porovnání podle výkresů", "Neporovnávají se jen názvy, ale rozměry, závity a tvar z technických výkresů a parametrů.", "Spárovaný díl opravdu pasuje."),
            ("Zápis rovnou do účetnictví", "468 vazeb mezi našimi kódy a katalogem dodavatele se zapsalo přes API do ABRA Flexi.", "Objednávání u dodavatele bez dohledávání kódů."),
            ("Co nemá protějšek, je vidět", "Díly, které druhý dodavatel nevede, zůstaly bez vazby a jsou na seznamu zvlášť.", "Víme, kde je potřeba hledat jiného dodavatele."),
        ],
        postup=[
            ("Načíst oba katalogy", "Naše skladové karty a katalog dodavatele, rozdělené do 45 podkategorií."),
            ("Porovnat výkresy a parametry", "AI hledá díl, který opravdu odpovídá rozměrem, závitem i tvarem."),
            ("Zapsat do ABRY", "Hotové vazby jdou přes API rovnou do karet v účetnictví."),
        ],
        tech="AI · ABRA Flexi REST API · technické výkresy a parametry",
        cta=CTA_FIRMA,
        fakta=[("Stav", "Hotovo"), ("Pro", "Kompresory-Vzduchotechnika.cz"), ("Výsledek", "468 vazeb v ABRA Flexi")],
    ),
    dict(
        slug="martin-kuska.html",
        title="Martin Kuška, obsahový specialista a spisovatel",
        desc="Osobní web pro obsahového specialistu, autora románů z Křivoklátska, průvodce a lektora jízdy na kole: práce pro firmy na prvním místě, stránka a formulář pro každý obor, strukturovaná data a měření se souhlasem.",
        eyebrow="Web pro přítele · rozpracováno",
        h1="Martin Kuška",
        lead="Osobní web pro obsahového specialistu, který píše odborné texty a obsahové strategie pro firmy, romány z Křivoklátska, provází krajinou a učí jezdit na kole v terénu. Práce pro firmy je na prvním místě, ostatní obory mají každý vlastní stránku.",
        meta=["Astro", "SEO + GEO", "strukturovaná data", "GA4 se souhlasem"],
        actions=[],
        visual=VIZ_KUSKA,
        stats=[
            ("4", "obory, každý s vlastní stránkou"),
            ("5", "formulářů na poptávku a přihlášky"),
            ("3", "stránky s častými dotazy pro Google"),
            ("4", "knihy s vlastním popisem pro vyhledávače"),
        ],
        zadani_h2="Čtyři obory, jeden člověk",
        zadani=[
            ("Firmy na prvním místě", "Martina živí hlavně obsah pro firmy. Knihy, procházky a kolo musí být vidět, ale nesmí přehlušit hlavní obor."),
            ("Různí návštěvníci", "Firma hledá autora odborných textů, čtenář knihu, turista procházku a cyklista kurz. Každý potřebuje něco jiného."),
            ("Dohledatelnost", "Web musí najít Google i AI vyhledávače a musí jim být jasné, kdo Martin je a co nabízí."),
        ],
        reseni="Úvod staví do popředí <strong>práci pro firmy</strong> a Martinův příběh. Knihy, procházky a kolo mají vlastní stránky s termíny a formuláři a celý web drží jeden klidný, „papírový“ styl.",
        moduly_h2="Co web umí",
        moduly=[
            ("Obsah pro firmy na prvním místě", "Služby od rešerše přes audit obsahu po SEO a GEO architekturu, obory, ve kterých se Martin vyzná, a značky, pro které psal.", "Firma hned vidí, s čím pomůže a pro koho pracoval."),
            ("Vlastní stránka pro každý obor", "Spisovatel se čtyřmi knihami a besedami, procházky po Křivoklátsku a tvůrčí dílny, kurzy jízdy na kole pro děti, začátečníky i pokročilé.", "Návštěvník najde jen to, co ho zajímá."),
            ("Formuláře s termíny", "Poptávka, přihláška na kurz, procházku nebo besedu. Kontrola údajů a ochrana proti spamu, klik na termín rovnou předvyplní formulář.", "Méně psaní pro zájemce, méně spamu pro Martina."),
            ("Strukturovaná data", "Google dostane strojově čitelný popis osoby, knih, služeb, častých dotazů a drobečkové navigace.", "Bohatší výsledky ve vyhledávání."),
            ("Měření se souhlasem", "Google Analytics 4 s režimem souhlasu v2 a srozumitelná stránka o ochraně soukromí. Měří se jen to, s čím návštěvník souhlasí.", "Data pro rozhodování v souladu s pravidly."),
            ("Rychlý statický web", "Postavený na Astru: stránky jsou předem hotové, bez zbytečného JavaScriptu, a fungují i na slabém signálu.", "Web se načte hned i v lese."),
        ],
        galerie=[
            ("shot", "kuska-uvod.webp", "Úvod: obsahový specialista a Martinův příběh.", "Martin Kuška · úvod", 800),
            ("shot", "kuska-firmy.webp", "Obsah a strategie pro firmy.", "Martin Kuška · pro firmy", 800),
            ("shot", "kuska-spisovatel.webp", "Spisovatel se čtyřmi knihami a besedami.", "Martin Kuška · spisovatel", 800),
            ("shot", "kuska-kolo.webp", "Kurzy jízdy na kole v terénu.", "Martin Kuška · kurzy na kole", 800),
            ("phone", "kuska-mobil.webp", "Úvod v mobilu."),
        ],
        galerie_note="Snímky z rozpracované verze webu. Termíny, ceny a některé fotky jsou zatím jen ukázka.",
        tech="Astro · strukturovaná data JSON-LD · Google Analytics 4 s režimem souhlasu v2",
        cta=CTA_WEB,
        fakta=[("Stav", "Rozpracováno"), ("Pro", "Martin Kuška"), ("Postaveno na", "Astro")],
    ),
    dict(
        slug="dundee-agency.html",
        title="Dundee Agency",
        desc="Audit a návrh nového webu pro eventovou a svatební agenturu: stránky služeb podle hledanosti, vstupenky s QR platbou a administrace s poptávkami a reklamou.",
        eyebrow="Pro klienta · návrh",
        h1="Dundee Agency",
        lead="Audit a návrh nového webu pro eventovou a svatební agenturu. Začal jsem daty: co lidé hledají, co dělá konkurence a jak agenturu vidí AI vyhledávače. Z toho vznikl web, administrace a plán spuštění.",
        meta=["Next.js", "Payload CMS", "vstupenky", "Ads + Sklik"],
        actions=[],
        visual=VIZ_DUNDEE,
        stats=[
            ("15 stran", "auditu v PDF"),
            ("11", "stránek služeb"),
            ("99–100", "Lighthouse na mobilu"),
            ("27", "automatických testů"),
        ],
        zadani_h2="Nejdřív data, pak web",
        zadani=[
            ("Kde agentura ztrácí", "Web neodpovídal tomu, co lidé hledají, a poptávka byla zbytečně složitá."),
            ("Hodně ruční práce", "Poptávky, vstupenky, příspěvky na sítě a reklama, každé jinde a všechno ručně."),
        ],
        reseni="Audit ukázal, co lidé hledají a kde agentura ztrácí zákazníky. Podle toho vznikl <strong>nový web s vlastní administrací v češtině</strong>, ve které agentura zvládne poptávky, vstupenky, sítě i reklamu sama.",
        moduly_h2="Co návrh obsahuje",
        moduly=[
            ("Stránky služeb podle hledanosti", "Jedenáct stránek služeb podle toho, co lidé opravdu hledají. Staré adresy se přesměrují, aby web nepřišel o pozice ve vyhledávání.", "Víc zákazníků z Googlu i Seznamu."),
            ("Poptávka na jedné obrazovce", "Krátký formulář, který funguje i bez JavaScriptu.", "Méně opuštěných poptávek."),
            ("Vstupenky s QR platbou", "Prodej vstupenek na akce s platbou přes QR kód.", "Peníze za vstupenky bez prostředníka."),
            ("Poptávky v administraci", "Každá poptávka má svůj stav od nové až po potvrzenou.", "Žádná poptávka nezapadne."),
            ("Plánované příspěvky", "Příspěvky na Facebook a Instagram se naplánují dopředu přímo z administrace.", "Sítě žijí i v nejrušnější sezóně."),
            ("Návratnost reklamy", "Google Ads a Sklik s návratností počítanou ze skutečných objednávek.", "Peníze jdou jen do reklamy, která vydělává."),
        ],
        postup=[
            ("Audit", "SEO podle dat z Marketing Mineru, srovnání s konkurencí, viditelnost v AI vyhledávačích a cesty zákazníků. 15 stran v PDF."),
            ("Návrh webu a administrace", "42 stránek, 11 stránek služeb, poptávky, vstupenky, sítě a reklama."),
            ("Plán spuštění", "Přesměrování starých adres, měření a postup, jak web spustit bez ztráty pozic."),
        ],
        tech="Next.js · Payload CMS · Marketing Miner · Google Ads · Sklik · Meta",
        cta=CTA_WEB,
        fakta=[("Stav", "Návrh"), ("Pro", "eventovou a svatební agenturu"), ("Postaveno na", "Next.js a Payload CMS")],
    ),
    dict(
        slug="pro-jachting.html",
        title="Pro-jachting.cz",
        desc="SEO audit a návrh nového webu pro jachtařskou školu a půjčovnu lodí: akční nabídky s odpočtem, objednávka bez registrace a kampaně, které se samy pozastaví.",
        eyebrow="Pro klienta · návrh",
        h1="Pro-jachting.cz",
        lead="SEO audit a návrh nového webu pro jachtařskou školu a půjčovnu lodí. Majitel si v administraci sám spravuje nabídky kurzů a plaveb, příspěvky na sítě i reklamu a vidí, kolik mu co vydělalo.",
        meta=["Next.js", "Payload CMS", "rezervace", "SEO audit"],
        actions=[],
        visual=VIZ_JACHTING,
        stats=[
            ("95–97", "Lighthouse na mobilu"),
            ("100", "přístupnost a SEO"),
            ("18", "automatických testů"),
            ("bez registrace", "objednávka kurzu nebo plavby"),
        ],
        zadani_h2="Nabídky, které se mění každý týden",
        zadani=[
            ("Akce s omezenou kapacitou", "Termíny plaveb a kurzů mají omezený počet míst a akční nabídky platí jen chvíli. Web musí být vždy aktuální."),
            ("Reklama běží i na vyprodané", "Když se termín vyprodá, reklama za něj dál utrácí, dokud ji někdo ručně nevypne."),
        ],
        reseni="Nabídky v administraci <strong>hlídají samy sebe</strong>: ukazují odpočet a volná místa, po skončení se skryjí a reklama na ně se sama pozastaví.",
        moduly_h2="Co návrh obsahuje",
        moduly=[
            ("Pevné a akční nabídky", "S odpočtem do konce a počtem volných míst. Po skončení nebo vyprodání se samy skryjí.", "Na webu nikdy nevisí neplatná nabídka."),
            ("Objednávka bez registrace", "Zájemce objedná bez zakládání účtu. Funguje i bez JavaScriptu.", "Méně opuštěných objednávek."),
            ("Odkud přišla objednávka", "U každé objednávky je vidět, z jakého zdroje zákazník přišel.", "Víme, co přivádí zákazníky."),
            ("Kampaně jedním klikem", "Google Ads a Sklik s náklady, tržbami a návratností. Když nabídka skončí, kampaň se sama pozastaví.", "Žádné peníze za reklamu na vyprodaný termín."),
            ("Plánované příspěvky", "Příspěvky na Facebook a Instagram naplánované z administrace.", "Sítě se plní i během sezóny na vodě."),
            ("SEO audit", "Audit ukázal, kde web ztrácí návštěvníky, a podle něj vznikla nová struktura stránek.", "Web, který lidé najdou."),
        ],
        postup=[
            ("SEO audit", "Co lidé hledají, kde web ztrácí návštěvníky a co dělá konkurence."),
            ("Redesign a rezervace", "Nová struktura stránek, nabídky s kapacitou a objednávka bez registrace."),
            ("Administrace pro majitele", "Nabídky, sítě a reklama s přehledem návratnosti na jednom místě."),
        ],
        tech="Next.js · Payload CMS · Google Ads · Sklik · Meta",
        cta=CTA_WEB,
        fakta=[("Stav", "Návrh"), ("Pro", "jachtařskou školu a půjčovnu lodí"), ("Postaveno na", "Next.js a Payload CMS")],
    ),
    dict(
        slug="ucetni-kancelar.html",
        title="Účetní kancelář",
        desc="Firemní web a klientský portál pro účetní kancelář na vlastním serveru, včetně bezpečnostního auditu a plánu zabezpečení.",
        eyebrow="Pro klienta · ve výrobě",
        h1="Web a portál pro účetní kancelář",
        lead="Firemní web a klientský portál, přes který si kancelář s klienty předává podklady. Běží na vlastním serveru, který jsem prověřil a zabezpečuju.",
        meta=["klientský portál", "vlastní server", "bezpečnostní audit"],
        actions=[],
        visual=VIZ_UCETNI,
        stats=[
            ("vlastní", "server pod kontrolou"),
            ("na pozvánku", "přístup do portálu"),
            ("online", "formuláře pro klienty"),
            ("audit", "a plán dalšího zabezpečení"),
        ],
        zadani_h2="Citlivá data, žádné kompromisy",
        zadani=[
            ("Podklady e-mailem", "Klienti posílali účetní podklady e-mailem a v přílohách. Nepřehledné a ne zrovna bezpečné."),
            ("Server pod útokem", "Každý server na internetu zkouší někdo uhodnout heslo. Otázka je, jestli se to ví a jestli je to pod kontrolou."),
        ],
        reseni="Postavil jsem <strong>web a portál</strong>, kam se klient dostane jen na pozvánku, a udělal bezpečnostní audit serveru s plánem, jak ho zabezpečit ještě víc.",
        moduly_h2="Co projekt obsahuje",
        moduly=[
            ("Firemní web", "Představení kanceláře a jejích služeb.", "Klienti kancelář snadno najdou."),
            ("Portál jen na pozvánku", "Účty zakládá kancelář. Kdokoli z internetu se do portálu nezaregistruje.", "Do portálu se dostanou jen klienti."),
            ("Formuláře pro klienty", "Podklady a údaje klient vyplní online místo e-mailů s přílohami.", "Podklady jsou na jednom místě a v pořádku."),
            ("Bezpečnostní audit a plán", "Audit serveru našel 167 796 zablokovaných pokusů o přihlášení. K tomu plán, jak server zabezpečit ještě víc.", "Kancelář ví, co se na serveru děje."),
        ],
        tech="vlastní server · klientský portál · bezpečnostní audit",
        cta=CTA_WEB,
        fakta=[("Stav", "Ve výrobě"), ("Pro", "účetní kancelář (jméno neuvádím)"), ("Běží na", "vlastním serveru")],
    ),
    dict(
        slug="kvit.html",
        title="Kvit",
        desc="Kvit: aplikace na férové dělení společných výdajů. Skupiny, čtyři způsoby dělení, vyrovnání QR platbou, cizí měny a provoz i bez signálu.",
        eyebrow="Vlastní aplikace · běží",
        h1="Kvit",
        lead="Aplikace na férové dělení společných výdajů. Založíš skupinu, pošleš kamarádům odkaz, píšete výdaje a Kvit na konci řekne, kdo komu kolik pošle. Vznikla z vlastní potřeby: chtěl jsem dělit výdaje s kamarády bez limitů a reklam.",
        meta=["PWA", "offline", "QR platby", "Supabase"],
        actions=[("Otevřít Kvit ↗", "https://app.kvit.cloud/")],
        visual=VIZ_KVIT,
        stats=[
            ("4", "způsoby dělení výdajů"),
            ("QR", "platba při vyrovnání"),
            ("offline", "funguje i bez signálu"),
            ("v1.1", "listopad 2026"),
        ],
        zadani_h2="Kdo komu kolik?",
        zadani=[
            ("Výlet, byt, dovolená", "Při společných výdajích se rychle ztratí přehled. Kdo platil benzín, kdo nákup, kdo ubytování?"),
            ("Aplikace s limity", "Podobné aplikace mají reklamy nebo omezení. Chtěl jsem jednoduchou a férovou."),
        ],
        reseni="Kvit vede <strong>bilanci každého člena</strong> a na konci navrhne co nejméně plateb, kterými se všichni vyrovnají. Zaplatit jde rovnou QR kódem.",
        moduly_h2="Co Kvit umí",
        moduly=[
            ("Skupiny pro každou příležitost", "Výlet, domácnost, pár i půjčka. Kamarádi se připojí přes odkaz a nemusí mít účet.", "Skupina je založená za minutu."),
            ("Čtyři způsoby dělení", "Rovným dílem, podle vah, přesnými částkami nebo procenty.", "Férově, i když každý jedl něco jiného."),
            ("Vyrovnání na pár klepnutí", "Kdo komu kolik pošle, s QR platbou do banky.", "Žádné přepisování čísel účtů."),
            ("Opakované výdaje a účtenky", "Nájem a předplatné se zapíšou samy, k výdaji jde přiložit účtenka.", "Nic se nezapomene."),
            ("Cizí měny a grafy", "Kurzy podle ČNB a grafy útrat ve verzi Pro.", "Přehled i z dovolené v zahraničí."),
            ("Offline a upozornění", "Funguje i bez signálu a data se srovnají později. Upozornění, připomínky a export.", "Výdaj zapíšete i na horách bez signálu."),
        ],
        tech="React · TypeScript · Vite · Tailwind · Supabase na vlastním serveru · PowerSync · Docker",
        cta=CTA_APP,
        fakta=[("Stav", "Běží, verze 1.1"), ("Pro", "kohokoli, kdo dělí výdaje"), ("Adresa", "app.kvit.cloud")],
    ),
    dict(
        slug="najedno.html",
        title="NaJedno",
        desc="NaJedno: appka pro partu, která chce zajít na jedno. Tajné hlasování s kvórem, výběr hospody, check-in, nápojový lístek a čárky v reálném čase.",
        eyebrow="Vlastní aplikace · běží pro partu přátel",
        h1="NaJedno",
        lead="Appka pro partu, která chce zajít na jedno. Nikdo neví, že jsi klikl. Odhalí se to všem naráz, až vás bude dost. Pak už jen vybrat hospodu a jít.",
        meta=["PWA", "realtime", "push oznámení"],
        actions=[],
        visual=VIZ_NAJEDNO,
        stats=[
            ("tajné", "hlasování s kvórem"),
            ("realtime", "čárky a lístek pro celou partu"),
            ("push", "oznámení do mobilu"),
            ("v0.2", "běží pro partu přátel"),
        ],
        zadani_h2="Půjde někdo?",
        zadani=[
            ("Nikdo nechce být první", "V chatu se nikomu nechce psát „půjdu“, když neví, jestli půjde i někdo další."),
            ("A kam vlastně?", "Domluva o hospodě a čase se v chatu ztratí mezi ostatními zprávami."),
        ],
        reseni="NaJedno má <strong>tajné „jsem pro“ s kvórem</strong>: každý klikne potichu a odhalí se to až ve chvíli, kdy vás je dost. Pak parta hlasuje o hospodě.",
        moduly_h2="Co NaJedno umí",
        moduly=[
            ("Tajné „jsem pro“", "Půjdu, když půjdou aspoň tři. Dokud není kvórum, nikdo neví, kdo klikl.", "Nikdo nemusí být první."),
            ("Hlasování o hospodě", "Parta vybere podnik a potvrdí, kam se jde.", "Žádné dohadování v chatu."),
            ("Check-in „Jsem tu“", "Kdo už sedí, dá vědět jedním klepnutím.", "Ostatní vědí, jestli můžou přijít."),
            ("Lístek a čárky", "Nápojový lístek a čárky v reálném čase pro celou partu.", "Na konci je jasné, kdo co měl."),
            ("Fotky a avatary", "Fotky z akce včetně formátu z iPhonu a avatary pro každého.", "Vzpomínky zůstanou u party."),
            ("Upozornění do mobilu", "Oznámení, když se parta schází nebo když padne kvórum.", "Nic vám neuteče."),
        ],
        tech="PWA · realtime · push oznámení",
        cta=CTA_APP,
        fakta=[("Stav", "Běží pro partu přátel, verze 0.2"), ("Pro", "partu, co chce zajít na jedno"), ("Dál", "chystám verzi pro všechny")],
    ),
]

# ---------- šablona stránky ----------

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='14' fill='%230e1a26'/%3E%3Cpath d='M16 16 L24 10' stroke='%23e0492a' stroke-width='3' stroke-linecap='round'/%3E%3Ccircle cx='16' cy='16' r='3' fill='%23ffffff'/%3E%3C/svg%3E"


def nw(text):
    """Slovo „e-shop“ se v nadpisech nesmí rozdělit na konci řádku."""
    import re

    return re.sub(r"\b(e-shop\w*)", r'<span class="nw">\1</span>', text)


def ind(text, n):
    pad = " " * n
    return "\n".join(pad + line if line.strip() else line for line in text.split("\n"))


def section(cls, inner, ident=None):
    idattr = f' id="{ident}"' if ident else ""
    return f'    <section{idattr} class="{cls}">\n      <div class="wrap">\n{inner}\n      </div>\n    </section>'


def head(eyebrow, h2):
    return (
        '        <header class="section__head">\n'
        f'          <p class="eyebrow">{eyebrow}</p>\n'
        f"          <h2>{h2}</h2>\n"
        "        </header>"
    )


def modules_class(n):
    if n == 4 or n == 2:
        return "cs-modules cs-modules--2"
    if n == 5:
        return "cs-modules cs-modules--5"
    return "cs-modules"


def render_modules(mods):
    items = []
    for h, p, b in mods:
        items.append(
            "          <li class=\"cs-module\">\n"
            f"            <h4>{h}</h4>\n"
            f"            <p>{p}</p>\n"
            f"            <p class=\"cs-benefit\">{b}</p>\n"
            "          </li>"
        )
    return f'        <ul class="{modules_class(len(mods))}">\n' + "\n".join(items) + "\n        </ul>"


def render_gallery(items, note):
    out = []
    for it in items:
        if it[0] == "shot":
            _, src, cap, bar, h = it
            out.append(
                "          <li><figure>"
                + shot(src, cap, bar, h=h)
                + f"<figcaption>{cap}</figcaption></figure></li>"
            )
        else:
            _, src, cap = it
            out.append(
                '          <li class="gallery__phone"><figure>'
                + phone(src, cap, tag="div")
                + f"<figcaption>{cap}</figcaption></figure></li>"
            )
    html = '        <ul class="gallery">\n' + "\n".join(out) + "\n        </ul>"
    if note:
        html += f'\n        <p class="phones__note" style="text-align: left">{note}</p>'
    return html


def render_next(slug):
    slugs = [s for s, _ in PORADI]
    i = slugs.index(slug)
    prev_s, prev_n = PORADI[(i - 1) % len(PORADI)]
    next_s, next_n = PORADI[(i + 1) % len(PORADI)]
    chips = "\n".join(
        f'          <li><a href="{s}"' + (' aria-current="page"' if s == slug else "") + f">{n}</a></li>"
        for s, n in PORADI
    )
    return (
        head("Další projekty", "Co jsem postavil dál")
        + "\n"
        + '        <nav class="pj-next" aria-label="Předchozí a další projekt">\n'
        + f'          <a href="{prev_s}" rel="prev"><small>← Předchozí</small><strong>{prev_n}</strong></a>\n'
        + f'          <a href="{next_s}" rel="next"><small>Další →</small><strong>{next_n}</strong></a>\n'
        + "        </nav>\n"
        + '        <ul class="pj-all" aria-label="Všechny projekty">\n'
        + chips
        + "\n        </ul>"
    )


def render_page(p):
    def dd(v):
        slovni = any(ch.isalpha() for ch in v) and len(v) >= 12
        return f'<dd class="is-word">{v}</dd>' if slovni else f"<dd>{v}</dd>"

    stats = "\n".join(
        f"          <div><dt>{t}</dt>{dd(v)}</div>" for v, t in p["stats"]
    )
    meta = "".join(f"<li>{m}</li>" for m in p["meta"])
    actions = ""
    if p.get("actions"):
        btns = "".join(
            f'<a class="btn btn--primary" href="{u}" rel="noopener">{t}</a>' for t, u in p["actions"]
        )
        actions = f'\n          <div class="pj-actions">{btns}<a class="btn btn--on-dark" href="./#kontakt">Napsat mi</a></div>'
    stats_note = ""
    if p.get("stats_note"):
        stats_note = f'\n        <p class="pj-note">{p["stats_note"]}</p>'

    h1_cls = ' class="pj-h1--long"' if p.get("h1_long") else ""
    hero = f"""    <section class="cs-hero pj-hero">
      <canvas class="airflow" data-airflow aria-hidden="true"></canvas>
      <div class="wrap">
        <a class="cs-back" href="./#projekty">← Zpět na projekty</a>
        <div class="cs-hero__grid">
        <div>
          <p class="eyebrow">{p["eyebrow"]}</p>
          <h1{h1_cls}>{nw(p["h1"])}</h1>
          <p class="cs-hero__lead">{p["lead"]}</p>
          <ul class="pj-meta" aria-label="Technologie a vlastnosti">{meta}</ul>{actions}
        </div>
        <div class="pj-visual">
          {p["visual"]}
        </div>
        </div>
        <dl class="cs-stats">
{stats}
        </dl>{stats_note}
      </div>
    </section>"""

    sekce = []
    # zadání
    cards = "\n".join(
        "          <li class=\"card\">\n"
        f"            <h3>{h}</h3>\n"
        f"            <p>{t}</p>\n"
        "          </li>"
        for h, t in p["zadani"]
    )
    sekce.append(
        (
            None,
            head("Zadání", nw(p["zadani_h2"]))
            + "\n"
            + f'        <ul class="cards cs-problems">\n{cards}\n        </ul>\n'
            + f'        <p class="cs-answer">{p["reseni"]}</p>',
        )
    )
    # co jsem postavil
    inner = head("Co jsem postavil a jak to pomáhá", nw(p["moduly_h2"])) + "\n" + render_modules(p["moduly"])
    if p.get("pod_povrchem"):
        links = "\n".join(
            "          <li class=\"project\">\n"
            f"            <h3>{n}</h3>\n"
            f"            <p>{t}</p>\n"
            f"            <a class=\"project__more\" href=\"{s}\">Detail projektu →</a>\n"
            "          </li>"
            for s, n, t in p["pod_povrchem"]
        )
        inner += '\n        <h3 class="group-title" style="margin-top: 40px">Pod povrchem</h3>\n' + f'        <ul class="projects">\n{links}\n        </ul>'
    inner += (
        '\n        <p class="brands">\n'
        '          <span class="brands__label">Technologie</span>\n'
        f'          <span class="brands__list">{p["tech"]}</span>\n'
        "        </p>"
    )
    sekce.append(("co-umi", inner))
    # galerie
    if p.get("galerie"):
        sekce.append(("galerie", head("Jak to vypadá", "Snímky") + "\n" + render_gallery(p["galerie"], p.get("galerie_note"))))
    elif p.get("galerie_note"):
        pass
    # postup
    if p.get("postup"):
        steps = "\n".join(
            "          <li>\n"
            f"            <h3>{h}</h3>\n"
            f"            <p>{t}</p>\n"
            "          </li>"
            for h, t in p["postup"]
        )
        sekce.append(("postup", head("Postup", "Jak to vzniklo") + f'\n        <ol class="steps">\n{steps}\n        </ol>'))
    # další projekty
    sekce.append(("dalsi", render_next(p["slug"])))

    body = []
    for i, (ident, inner) in enumerate(sekce):
        cls = "section section--alt" if i % 2 == 1 else "section"
        body.append(section(cls, inner, ident))

    cta_h, cta_p = p["cta"]
    fakta = "\n".join(
        "            <li>\n"
        f'              <span class="contact__label">{l}</span>\n'
        f"              <span>{v}</span>\n"
        "            </li>"
        for l, v in p["fakta"]
    )
    contact = f"""    <section class="section">
      <div class="wrap">
        <div class="contact">
          <div class="contact__intro">
            <p class="eyebrow eyebrow--invert">Spolupráce</p>
            <h2>{cta_h}</h2>
            <p>{cta_p}</p>
            <div class="contact__actions">
              <a class="btn btn--primary" href="./#kontakt">Napsat mi</a>
              <a class="btn btn--ghost" href="./#projekty">Všechny projekty</a>
            </div>
          </div>
          <ul class="contact__list">
{fakta}
          </ul>
        </div>
      </div>
    </section>"""

    nav_anchors = '<a href="#co-umi">Co umí</a>'
    if p.get("galerie"):
        nav_anchors += '\n        <a href="#galerie">Snímky</a>'
    nav_anchors += '\n        <a href="./#projekty">Projekty</a>'

    url = f"{WEB}/{p['slug']}"
    ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebPage",
                    "@id": url,
                    "url": url,
                    "name": f"{p['title']} — Zdeněk Štuksa",
                    "description": p["desc"],
                    "inLanguage": "cs",
                    "isPartOf": {"@id": f"{WEB}/#web"},
                    "author": {
                        "@type": "Person",
                        "@id": f"{WEB}/#zdenek",
                        "name": "Zdeněk Štuksa",
                        "url": f"{WEB}/",
                    },
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Zdeněk Štuksa", "item": f"{WEB}/"},
                        {"@type": "ListItem", "position": 2, "name": p["title"], "item": url},
                    ],
                },
            ],
        },
        ensure_ascii=False,
        indent=2,
    )

    return f"""<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p["title"]} — Zdeněk Štuksa</title>
  <meta name="description" content="{p["desc"]}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#f3f5f7" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0a1118" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{WEB}/{p["slug"]}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Zdeněk Štuksa">
  <meta name="twitter:card" content="summary">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:url" content="{WEB}/{p["slug"]}">
  <meta property="og:title" content="{p["title"]} — Zdeněk Štuksa">
  <meta property="og:description" content="{p["desc"]}">
  <meta property="og:image" content="{WEB}/assets/zdenek-stuksa.jpg">

  <link rel="icon" href="{FAVICON}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
  <a class="skip-link" href="#obsah">Přeskočit na obsah</a>

  <header class="site-header">
    <div class="wrap site-header__inner">
      <a class="brand" href="./" aria-label="Zdeněk Štuksa – úvod">
        <span class="brand__mark" aria-hidden="true">ZŠ</span>
        <span class="brand__name">Zdeněk Štuksa</span>
      </a>
      <nav class="nav" aria-label="Navigace projektu">
        {nav_anchors}
        <a class="nav__cta" href="./#kontakt">Kontakt</a>
      </nav>
    </div>
  </header>

  <main id="obsah">
    <!-- generováno: _zdroj/projekty.py -->
{hero}

{chr(10).join(body)}

{contact}
  </main>

  <footer class="site-footer">
    <div class="wrap site-footer__inner">
      <span>© <span data-year>2026</span> Zdeněk Štuksa</span>
      <span><a href="./">Zpět na hlavní stránku</a></span>
      <button type="button" class="footer-link" data-consent-open hidden>Nastavení cookies</button>
    </div>
  </footer>

  <script src="script.js" defer></script>
</body>
</html>
"""


def obnov_middleware():
    """Vloží blok „Další projekty“ do ručně psané stránky middlewaru."""
    soubor = KOREN / "middleware.html"
    text = soubor.read_text(encoding="utf-8")
    zacatek, konec = "<!-- DALSI-PROJEKTY -->", "<!-- /DALSI-PROJEKTY -->"
    if zacatek not in text:
        raise SystemExit("V middleware.html chybí značka " + zacatek)
    pred, zbytek = text.split(zacatek, 1)
    _, po = zbytek.split(konec, 1)
    blok = section("section section--alt", render_next("middleware.html"), "dalsi")
    soubor.write_text(pred + zacatek + "\n" + blok + "\n    " + konec + po, encoding="utf-8")


if __name__ == "__main__":
    for p in PROJEKTY:
        (KOREN / p["slug"]).write_text(render_page(p), encoding="utf-8")
        print("zapsáno", p["slug"])
    obnov_middleware()
    print("obnoveno middleware.html")

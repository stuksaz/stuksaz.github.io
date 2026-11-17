# Zdeněk Štuksa — osobní web

Osobní web: kdo jsem, co umím, co jsem postavil a jak mě kontaktovat.
Hlavní stránka a ke každému projektu vlastní stránka.
Čisté HTML, CSS a pár řádků JavaScriptu, bez závislostí.

Adresa: **https://stuksaz.github.io**

## Soubory

| Soubor | Co v něm je |
| --- | --- |
| `index.html` | Hlavní stránka: úvod, O mně, Co umím, Projekty, Jak pracuju, Příběh, Kontakt |
| `middleware.html` | Případová studie middlewaru Ventilek (psaná ručně) |
| `kompresory-vzduchotechnika.html`, `kvit.html` a další | Stránky projektů, **generované** z `_zdroj/projekty.py` |
| `styles.css` | Vzhled. Barvy jsou proměnné nahoře v `:root`, tmavý režim hned pod |
| `script.js` | Animace (proudění vzduchu, živý deník, odpočty, počítadla) a aktuální rok |
| `assets/` | Fotka, snímky webů a aplikací (WebP) |

## Úprava stránek projektů

Texty projektů jsou v `_zdroj/projekty.py` (seznam `PROJEKTY`). Po úpravě:

```bash
python3 _zdroj/projekty.py
```

Skript přepíše všechny stránky projektů a obnoví blok „Další projekty“
v `middleware.html`. Složku `_zdroj` GitHub Pages nezveřejňuje.
Stránky projektů neupravuj ručně, při dalším spuštění by se změny ztratily.

## Náhled na počítači

Stačí otevřít `index.html` v prohlížeči. Nebo spustit lokální server:

```bash
python3 -m http.server 8000
# a otevřít http://localhost:8000
```

## Zveřejnění (GitHub Pages)

Repozitář se jmenuje `stuksaz.github.io`, takže GitHub web zveřejní na
`https://stuksaz.github.io` z větve `main`. Kdyby se web po sloučení
neobjevil: **Settings → Pages → Source: Deploy from a branch**, větev `main`,
složka `/ (root)`, **Save**.

Vlastní doménu (třeba `stuksa.cz`) jde nastavit tamtéž v **Custom domain**.

## Co ještě doplnit

- **Osobní e-mail a telefon:** teď jsou v kontaktu firemní údaje.
- **Reference:** krátká věta od spokojeného klienta nebo přítele.

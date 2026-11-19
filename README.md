# Zdeněk Štuksa — osobní web

Osobní web: kdo jsem, co umím, co jsem postavil a jak mě kontaktovat.
Hlavní stránka a ke každému projektu vlastní stránka.
Čisté HTML, CSS a pár řádků JavaScriptu, bez závislostí.

Adresa: **https://zdenekstuksa.cz** (záložní: https://stuksaz.github.io)

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

## Zveřejnění (GitHub Pages + vlastní doména)

Web zveřejňuje GitHub Pages z větve `main`, složka `/ (root)`
(**Settings → Pages → Source: Deploy from a branch**).

Doména **zdenekstuksa.cz** je v souboru `CNAME`. U registrátora domény musí být
tyto DNS záznamy:

| Typ | Název | Hodnota |
| --- | --- | --- |
| A | `@` (zdenekstuksa.cz) | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `stuksaz.github.io.` |

Jiné A/AAAA záznamy pro `@` a `www` (třeba výchozí parkovací stránka registrátora)
je potřeba smazat. Po rozšíření DNS (minuty až hodiny) v **Settings → Pages**
zaškrtnout **Enforce HTTPS**. Doménu je dobré ověřit i v nastavení účtu
(**Settings → Pages → Verified domains**), aby ji nikdo jiný nemohl
připojit ke svému webu.

Adresa webu je ve stránkách na několika místech (`canonical`, `og:url`,
obrázek pro sdílení, `sitemap.xml`, `robots.txt`, `WEB` v `_zdroj/projekty.py`).
Při změně domény je potřeba změnit všechna.

## Co ještě doplnit

- **Osobní e-mail a telefon:** teď jsou v kontaktu firemní údaje.
- **Reference:** krátká věta od spokojeného klienta nebo přítele.

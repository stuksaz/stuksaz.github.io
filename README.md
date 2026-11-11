# Zdeněk Štuksa — osobní web

Jednostránkový osobní web: kdo jsem, co umím, co jsem postavil a jak mě kontaktovat.
Čisté HTML, CSS a pár řádků JavaScriptu, bez buildu a bez závislostí.

Adresa: **https://stuksaz.github.io**

## Soubory

| Soubor       | Co v něm je                                                                       |
| ------------ | --------------------------------------------------------------------------------- |
| `index.html` | Obsah: úvod s manometrem, O mně, Co umím, Projekty, Jak pracuju, Příběh, Kontakt  |
| `styles.css` | Vzhled. Barvy jsou proměnné nahoře v `:root`, tmavý režim hned pod                |
| `script.js`  | Doplní aktuální rok do patičky                                                    |

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

- **Fotka:** v `index.html` nahradit `<div class="portrait">` obrázkem (návod je v komentáři přímo u něj).
- **Osobní e-mail a telefon:** teď jsou v kontaktu firemní údaje.
- **Reference:** krátká věta od spokojeného klienta nebo přítele.

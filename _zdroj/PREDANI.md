# Předání práce na osobním webu (stav 19. 11. 2026)

Tento soubor je pro Clauda, který pokračuje v práci na webu Zdeňka Štuksy
v nové konverzaci. Složka `_zdroj` se na webu nezveřejňuje, repozitář ale
JE veřejný, takže sem nepatří nic soukromého.

## Jak se Zdeňkem mluvit

- Česky, krok za krokem, bez technického žargonu. Zdeněk je majitel firmy,
  ne programátor.
- Nenabízet tři varianty. Rozhodnout, krátce vysvětlit proč a udělat.
- Svolení k nastavení DNS u Wedosu dal výslovně („máš na to svolení“).
  Platby, objednávky služeb a sloučení PR ale vždy potvrzuje on.

## Co je hotové

- Repozitář `stuksaz/stuksaz.github.io`, pracovní větev
  `claude/personal-website-kyzb4h`, návrh **PR #1** (draft, bez konfliktů).
  Větev `main` má jen úvodní commit, web zatím neběží.
- Statický web (HTML, CSS, trochu JavaScriptu), GitHub Pages z větve `main`.
- `index.html` hlavní stránka, `middleware.html` ruční případová studie,
  11 stránek projektů se **generuje** z `_zdroj/projekty.py`
  (`python3 _zdroj/projekty.py`, vygenerované HTML neupravovat ručně).
- `CNAME` = `zdenekstuksa.cz`, `sitemap.xml`, `robots.txt`, `canonical`
  a `og:url` na všech stránkách.
- Kontakt na webu: jsem@zdenekstuksa.cz, +420 773 489 530.
- Náhled (soukromý artefakt): https://claude.ai/artifact/DKjysm94PuwPvePLMAantp
  (publikuje se z kopie bez hlavičky dokumentu: `index.html` jen s obsahem
  `<head>` a `<body>`, ostatní soubory přes `files`).

## Co je potřeba udělat teď

### 1. DNS u Wedosu pro zdenekstuksa.cz

Stav 19. 11. 13:25 UTC: NS ns.wedos.*, A 185.8.237.22 (parkovací stránka
Wedosu), AAAA 2a0e:acc0::d22, www → stejné, žádné CAA, MX ani TXT.

Wedos administrace: **Seznam domén → zdenekstuksa.cz → Editace DNS záznamů**.

1. Smazat jen A a AAAA s prázdným názvem a všechny záznamy s názvem `www`.
2. Přidat (TTL výchozí):

| Název | Typ | Data |
| --- | --- | --- |
| (prázdný) | A | 185.199.108.153 |
| (prázdný) | A | 185.199.109.153 |
| (prázdný) | A | 185.199.110.153 |
| (prázdný) | A | 185.199.111.153 |
| (prázdný) | AAAA | 2606:50c0:8000::153 |
| (prázdný) | AAAA | 2606:50c0:8001::153 |
| (prázdný) | AAAA | 2606:50c0:8002::153 |
| (prázdný) | AAAA | 2606:50c0:8003::153 |
| www | CNAME | stuksaz.github.io. |

3. Uložit a potvrdit změny. Ověřit např.
   `https://dns.google/resolve?name=zdenekstuksa.cz&type=A`.

### 2. Schránka jsem@zdenekstuksa.cz

Ještě neexistuje (doména nemá MX). Založit ji u Wedosu, případně jako
přesměrování. Pokud je placená, rozhoduje Zdeněk. Pak poslat zkušební
e-mail. Dokud nefunguje, web nezveřejňovat (zprávy by propadaly).

### 3. Spuštění webu

1. Zdeněk potvrdí otevřené body níže, pak PR #1 → Ready for review → Merge.
2. GitHub → repozitář → **Settings → Pages**: Custom domain
   `zdenekstuksa.cz`, po vydání certifikátu zaškrtnout **Enforce HTTPS**.
   Certifikát vydává GitHub zdarma a automaticky (Let's Encrypt).
   Certifikát z Wedosu se pro GitHub Pages použít nedá.
3. Ověřit doménu v nastavení účtu GitHub: **Settings → Pages → Verified domains**.
4. Zkontrolovat https://zdenekstuksa.cz i https://www.zdenekstuksa.cz.

## Otevřené otázky na Zdeňka (před sloučením)

- Od kterého roku je v e-commerce (manometr ukazuje „~20“).
- Smí ven čísla z middlewaru (500 000+ přeložených textů, náklady na
  překlady „z tisíců na desítky Kč“)?
- Smí být na webu Pro-jachting.cz, účetní kancelář (bez jména), Kvit a NaJedno?
- Martin Kuška: souhlas se snímky webu a fotkou. Jeho web je rozpracovaný
  (artefakt https://claude.ai/artifact/R3r5ZJyqj5h6i5Jb3ZjvXb). Po spuštění
  přefotit snímky (`assets/kuska-*.webp`, bez lišty „Návrh webu“), doplnit
  odkaz a změřit Lighthouse.
- Řezbář z Podhradí: přesný název, doména a pár vět. Zatím jen karta bez
  stránky.

## Pravidla obsahu

- Repozitář je veřejný: nezveřejňovat datum narození, soukromý e-mail,
  IP adresy serverů ani hesla.
- Účetní kancelář zůstává bez jména. Zjištění z auditu Pro-jachtingu jen obecně.
- Ilustrace (makety funkcí) musí být na stránce označené jako ilustrace.
- Fakta o middlewaru se berou z `CLAUDE.md` v repozitáři `stuksaz/middleware-pim`.
- Do commitů ani PR nepsat identifikátor modelu.

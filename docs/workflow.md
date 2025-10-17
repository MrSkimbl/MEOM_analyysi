# Analyysi-workflow - Yksityiskohtainen kuvaus

## Yleiskuva

```
Input: URL → [7 vaihetta] → Output: HTML-raportti
Kesto: 10-15 min (6 yritystä)
```

---

## Vaihe 1A: Kohdeyrityksen analyysi

**API**: GPT-5 Responses API (EI web search)

**Prosessi**:
1. Analysoi yritys URL:n perusteella
2. Tunnista palvelut, tuotteet, asiakaskunta
3. Palauta JSON

**Output**:
```json
{
  "company_name": "Yritys Oy",
  "services": ["Palvelu 1", "Palvelu 2"],
  "target_customers": "Kuvaus",
  "value_proposition": "Ydinviesti",
  "analysis": "Yhteenveto"
}
```

---

## Vaihe 1B: Kilpailijoiden haku

**API**: GPT-5 Responses API + **Web Search**

**Prosessi**:
1. Käytä vaiheen 1A analyysiä kontekstina
2. Hae kilpailijoita web searchilla
3. Suodata Suomen markkinaan
4. Palauta 5 kilpailijaa

**Prompt**:
```
Yritys: {company_name}
Palvelut: {services}
Asiakkaat: {target_customers}

Etsi 5 kilpailijaa Suomen markkinassa jotka:
- Tarjoavat samankaltaisia palveluita
- Kilpailevat samoista asiakkaista
- Ovat merkittäviä toimijoita
```

**Output**: 5 kilpailijaa (nimi + URL)

---

## Vaihe 3: Asiakasreferenssien haku

**Teknologiat**: BeautifulSoup4 + GPT-5

**Prosessi (per yritys)**:
1. Etsi asiakassivuja: `/asiakkaat`, `/referenssit`, `/case`
2. Scrappaa sivut BeautifulSoup4:llä
3. Lähetä teksti GPT-5:lle
4. Pura asiakasnimet JSON:na

**Prompt**:
```
Analysoi teksti ja etsi asiakkaiden nimet.

Palauta JSON:
{
  "customers": ["Asiakas 1", "Asiakas 2"]
}

Teksti: {scraped_text}
```

**Output**: 
```python
{
  "Reaktor": ["Elisa", "YLE", "Kesko"],
  "Futurice": ["HSL", "Kela", "Alko"],
  ...
}
```

---

## Vaihe 4: ICP-analyysi (Ideal Customer Profile)

**API**: GPT-5 Responses API

**Input**: Kaikki asiakkaat kaikilta yrityksiltä

**Prosessi**:
1. Yhdistä kaikki asiakkaat (50-150 yritystä)
2. Lähetä GPT-5:lle ICP-analyysiin
3. Luo 4-6 ICP:tä

**ICP-ulottuvuudet**:
- **Firmografia**: Koko, toimialat, organisaatiotyyppi
- **Teknografia**: Digitaalinen kypsyys, tech stack
- **Tarpeet**: Haasteet, tyypilliset projektit
- **Käyttäytyminen**: Päätöksenteko, budjetti

**Output**:
```json
{
  "icps": [
    {
      "name": "Suuret finanssialan toimijat",
      "firmographic": {
        "company_size": "Enterprise",
        "industries": ["Banking", "Insurance"]
      },
      "needs": {
        "challenges": ["Compliance", "Legacy"],
        "typical_projects": ["Digital platforms"]
      },
      "example_customers": ["OP", "Nordea"],
      "market_value": "High"
    }
  ]
}
```

---

## Vaihe 5: Etusivujen copyjen haku

**Teknologia**: BeautifulSoup4 (EI OpenAI:ta)

**Prosessi (per yritys)**:
1. Scrappaa etusivu
2. Poimi:
   - H1, H2 otsikot
   - Hero-tekstit
   - Ensimmäiset kappaleet
3. Puhdista (poista nav, footer, script)

**Output**:
```python
{
  "Reaktor": {
    "hero_headline": "We create digital products",
    "main_value_prop": "Transform your business...",
    "full_text": "..."
  }
}
```

---

## Vaihe 6: Positioning-analyysi (YDIN)

**API**: GPT-5 Responses API

**Input**:
- 6 yrityksen copyt (vaihe 5)
- 4-6 ICP:tä (vaihe 4)

**Prosessi**:
1. Arvioi kunkin yrityksen viesti per ICP
2. Anna pisteet 1-5
3. Perustele vahvuudet ja heikkoudet

**Kriteerit**:
- Mainitaanko ICP:n toimialoja?
- Puhutaanko ICP:n haasteista?
- Onko case-esimerkkejä?
- Onko viesti linjassa digitaalisen kypsyyden kanssa?

**Output**:
```json
{
  "analysis": [
    {
      "company": "Reaktor",
      "positioning_by_icp": [
        {
          "icp_name": "Suuret finanssialan toimijat",
          "score": 4,
          "reasoning": "Vahva fokus...",
          "strengths": ["S1", "S2"],
          "weaknesses": ["W1"]
        }
      ]
    }
  ],
  "icp_leaders": {
    "Suuret finanssialan toimijat": "Reaktor"
  },
  "overall_insights": "Keskeiset löydökset..."
}
```

---

## Vaihe 7: HTML-raportin generointi

**Teknologia**: Python string templating + MEOM style guide

**Prosessi**:
1. Lataa MEOM:n tyylit (CSS)
2. Generoi HTML:
   - Executive summary
   - ICP-johtajat (kortit)
   - Positioning-matriisi (taulukko, värikoodattu)
   - Yrityskohtaiset analyysit
   - ICP-profiilit
3. Tallenna tiedostoon

**Output**: `report.html` (valmis avattavaksi selaimessa)

---

## Tekninen kaavio

```
analyzer.py --url X
    │
    ├─→ [1A] analyze_target_company()      GPT-5
    │
    ├─→ [1B] find_competitors()            GPT-5 + Web Search
    │
    ├─→ [3]  extract_all_customers()       BeautifulSoup + GPT-5
    │        └─→ per company:
    │            ├─ find_customer_pages()
    │            ├─ scrape_page_text()
    │            └─ extract_customer_names()  GPT-5
    │
    ├─→ [4]  create_icps()                 GPT-5
    │
    ├─→ [5]  extract_all_copy()            BeautifulSoup
    │
    ├─→ [6]  analyze_positioning()         GPT-5
    │
    └─→ [7]  generate_html_report()        Template
            └─→ report.html
```

---

## API-käyttö yhteenveto

| Vaihe | API | Web Search | Kesto |
|-------|-----|-----------|--------|
| 1A | GPT-5 Responses | - | 10-20s |
| 1B | GPT-5 Responses | ✓ | 20-40s |
| 3 | GPT-5 Responses | - | 2-4 min |
| 4 | GPT-5 Responses | - | 20-40s |
| 5 | - | - | 30-60s |
| 6 | GPT-5 Responses | - | 30-60s |
| 7 | - | - | 1s |

**Yhteensä**: 10-15 min (6 yritystä)

---

## Virheenkäsittely

- URL ei toimi → Keskeytä
- Kilpailijoita ei löydy → Jatka vain kohdeyrityksellä
- Asiakassivuja ei löydy → Merkitse "Ei julkisia referenssejä"
- Scraping epäonnistuu → Jatka muilla
- OpenAI timeout → Retry 3× exponential backoff
- JSON-parsinta epäonnistuu → Logita raakadata, keskeytä

# Analyysi-workflow - Yksityiskohtainen kuvaus

## Yleiskuva

Työkalu suorittaa seitsemän vaihetta lineaarisesti ja tuottaa lopulta HTML-raportin.

```
Input: URL → [1-7 vaiheet] → Output: HTML-raportti
```

## Vaihe 1: URL-validointi ja käsittely

**Input**: Käyttäjän antama URL komentorivillä

**Prosessi**:
1. Validoi URL-muoto
2. Tarkista että sivusto on tavoitettavissa
3. Hae yrityksen nimi ja perustiedot

**Output**: 
- Validoitu URL
- Yrityksen nimi

**OpenAI-käyttö**: Ei tässä vaiheessa (vain tekninen validointi)

---

## Vaihe 2: Kilpailijoiden haku

**Input**: Alkuperäinen URL ja yrityksen nimi

**Prosessi**:
1. Käytetään OpenAI:n web search -toimintoa
2. Etsitään 5 pääkilpailijaa Suomen markkinassa
3. Validoidaan löydetyt kilpailijat

**OpenAI Prompt**:
```
Etsi 5 pääkilpailijaa yritykselle "{yrityksen_nimi}" ({url}) Suomen markkinassa.
Keskity yrityksiin, jotka:
- Toimivat Suomessa
- Tarjoavat samankaltaisia tuotteita/palveluita
- Ovat merkittäviä toimijoita

Palauta lista muodossa:
1. Yrityksen nimi - URL
2. Yrityksen nimi - URL
...
```

**Output**: 
- Lista 5 kilpailijan nimeä ja URL:ia
- Yhteensä 6 yritystä analysoitavana (alkuperäinen + 5 kilpailijaa)

---

## Vaihe 3: Asiakasreferenssien haku

**Input**: 6 yrityksen URL:it

**Prosessi (kullekin yritykselle)**:
1. **Web scraping**: Hae yrityksen sivusto
2. **Sivujen tunnistus**: Etsi sivuja, joilla voi olla asiakasreferenssejä:
   - /asiakkaat, /referenssit, /cases, /customers
   - /portfolio, /projektit
3. **Tekstin purku**: Käytä BeautifulSoup4 tekstin erottamiseen
4. **AI-ekstrahointi**: OpenAI tunnistaa asiakasnimet tekstistä

**OpenAI Prompt** (per yritys):
```
Analysoi seuraava teksti yrityksen "{yritys}" sivustolta.
Etsi ja listaa kaikki mainitut asiakkaiden/referenssiasiakkaiden nimet.

Teksti:
{sivuston_teksti}

Palauta pelkästään lista yritysnimiä, yksi per rivi.
Älä sisällytä henkilönimiä, vain yritysten nimiä.
```

**Output**: 
- Dictionary: `{yritys_url: [asiakas1, asiakas2, ...]}`
- Yhteensä n. 20-100 asiakasta (riippuu löydöksistä)

**Virheenkäsittely**:
- Jos sivustoa ei saada haettua → jatka muilla
- Jos ei löydy asiakassivuja → merkitse "Ei julkisia referenssejä"

---

## Vaihe 4: Asiakassegmentointi

**Input**: Kaikki löydetyt asiakasnimet (yhteensä kaikilta 6 yritykseltä)

**Prosessi**:
1. Yhdistä kaikki asiakasnimet yhdeksi listaksi
2. Lähetä OpenAI:lle segmentointianalyysi
3. OpenAI tunnistaa yhteisiä piirteitä ja luo segmentit

**OpenAI Prompt**:
```
Analysoi seuraava lista B2B-asiakkaita ja luo niistä loogisia asiakassegmenttejä.

Asiakasnimet:
{kaikki_asiakkaat}

Tee seuraavaa:
1. Tunnista yhteiset toimialat/teollisuudenalat
2. Tunnista yrityskokojen jakauma (pk-yritykset, suuryritykset)
3. Tunnista maantieteelliset keskittymät
4. Luo 4-6 selkeää asiakassegmenttiä

Palauta JSON-muodossa:
{
  "segments": [
    {
      "name": "Segmentin nimi",
      "description": "Lyhyt kuvaus",
      "examples": ["Esimerkki 1", "Esimerkki 2"]
    }
  ]
}
```

**Output**: 
- 4-6 asiakassegmenttiä
- Jokainen segmentti sisältää nimen, kuvauksen ja esimerkkejä

---

## Vaihe 5: Etusivujen copyjen haku

**Input**: 6 yrityksen URL:it

**Prosessi (kullekin yritykselle)**:
1. Hae yrityksen etusivu
2. Käytä BeautifulSoup4 tekstin erottamiseen
3. Erottele tärkeät tekstiosuudet:
   - Hero-tekstit (pääotsikot)
   - Value propositionit
   - Kuvaukset palveluista/tuotteista
4. Poista navigaatio, footer jne.

**Output**:
- Dictionary: `{yritys_url: "Etusivun päätekstit..."}`
- Keskimäärin 200-500 sanaa per yritys

**Tekninen toteutus**:
```python
def extract_homepage_copy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Poista turha
    for element in soup(['script', 'style', 'nav', 'footer']):
        element.decompose()
    
    # Etsi tärkeät tekstit
    hero = soup.find(['h1', 'h2'])
    paragraphs = soup.find_all('p', limit=10)
    
    return combined_text
```

---

## Vaihe 6: Positioning-analyysi

**Input**: 
- 6 yritystä
- 4-6 segmenttiä
- Etusivujen copyt

**Prosessi**:
1. Lähetä kaikki data OpenAI:lle
2. OpenAI analysoi kunkin yrityksen viestin vahvuuden per segmentti
3. Pisteytetään asteikolla 1-5

**OpenAI Prompt**:
```
Analysoi seuraavien yritysten positioning eri asiakassegmenteille.

YRITYKSET JA NIIDEN VIESTIT:
{yritykset_ja_copyt}

ASIAKASSEGMENTIT:
{segmentit}

TEHTÄVÄ:
Arvioi kunkin yrityksen viestin (etusivun copy) vahvuus kullekin segmentille.

Kriteerit:
- Kuinka hyvin viesti resonoi segmentin tarpeiden kanssa?
- Mainitaanko segmentti eksplisiittisesti?
- Onko esimerkkejä/referenssejä segmentistä?
- Onko tarjonta relevanttia segmentille?

Palauta JSON:
{
  "analysis": [
    {
      "company": "Yritys A",
      "url": "...",
      "segments": {
        "Segmentti 1": {
          "score": 4,
          "reasoning": "Vahva fokus tähän segmenttiin..."
        },
        "Segmentti 2": { ... }
      }
    }
  ],
  "segment_leaders": {
    "Segmentti 1": "Yritys A",
    "Segmentti 2": "Yritys C"
  }
}
```

**Output**:
- Matriisi: Yritykset × Segmentit, pisteet 1-5
- Selitykset jokaiselle pisteytykselle
- Yhteenveto: Kuka on vahvin kussakin segmentissä

---

## Vaihe 7: HTML-raportin generointi

**Input**: Kaikki edellisten vaiheiden data

**Prosessi**:
1. Lataa HTML-template
2. Täytä template datalla
3. Luo visualisoinnit (taulukot, matriisit)
4. Tallenna HTML-tiedosto

**Raportin rakenne**:

```html
1. EXECUTIVE SUMMARY
   - Analysoidut yritykset
   - Päälöydökset

2. KILPAILIJA-YLEISKATSAUS
   - Taulukko 6 yrityksestä
   - Perustiedot ja URL:t

3. ASIAKASSEGMENTIT
   - 4-6 tunnistettua segmenttiä
   - Kuvaukset ja esimerkit

4. POSITIONING-MATRIISI
   - Taulukko: Yritykset × Segmentit
   - Värikoodaus vahvuuden mukaan
   - Heat map -tyylinen visualisointi

5. SEGMENTTIKOHTAINEN ANALYYSI
   Per segmentti:
   - Vahvin toimija
   - Perustelu
   - Muiden yritysten positioning

6. YRITYSKOHTAINEN ANALYYSI
   Per yritys:
   - Etusivun pääviesit
   - Asiakasreferenssit
   - Vahvuudet ja heikkoudet
   - Suositukset

7. LIITTEET
   - Kaikki löydetyt asiakasreferenssit
   - Raa'at pisteet
```

**Output**: 
- Valmis HTML-tiedosto
- Avattavissa selaimessa
- Tulostettavissa/jaettavissa PDF:nä

---

## Tekninen workflow-kaavio

```
┌─────────────────┐
│  python         │
│  analyzer.py    │
│  --url X        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 1. Validoi URL                  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 2. Hae kilpailijat (OpenAI)     │
│    → 5 yritystä                 │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 3. Loop 6 yritystä:             │
│    - Scrape asiakassivut        │
│    - OpenAI: pura asiakasnimet  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 4. Segmentoi asiakkaat (OpenAI) │
│    → 4-6 segmenttiä             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 5. Loop 6 yritystä:             │
│    - Scrape etusivu             │
│    - Tallenna copyt             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 6. Analysoi positioning         │
│    (OpenAI)                     │
│    → Matriisi + selitykset      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 7. Generoi HTML-raportti        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────┐
│  report.html    │
└─────────────────┘
```

## Arvioitu suoritusaika

- Vaihe 1: < 1 s
- Vaihe 2: 5-10 s (OpenAI + web search)
- Vaihe 3: 30-60 s (6× scraping + OpenAI)
- Vaihe 4: 5-10 s (OpenAI)
- Vaihe 5: 10-20 s (6× scraping)
- Vaihe 6: 10-20 s (OpenAI)
- Vaihe 7: 1-2 s

**Yhteensä**: 1-2 minuuttia per analyysi

## Virheenkäsittely

Työkalu käsittelee seuraavat virhetilanteet:
- URL ei ole tavoitettavissa → Ilmoita ja keskeytä
- Kilpailijoita ei löydy → Jatka pelkällä alkuperäisellä
- Asiakassivuja ei löydy → Merkitse "Ei julkisia referenssejä"
- OpenAI API-virhe → Yritä uudelleen 3× exponential backoff
- Rate limiting → Odota ja yritä uudelleen


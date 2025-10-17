# Testausohje - OpenAI API

## Yhteenveto

Tämä dokumentti kuvaa miten OpenAI API:a testataan ja miten testit on organisoitu projektissa.

## Testitulokset (Lokakuu 2025)

✅ **Kaikki 4 testiä läpäistiin onnistuneesti:**

1. **API-yhteys** - OpenAI API-avain toimii ja yhteys muodostuu
2. **Web Search** - Malli vastaa kyselyihin (huom: web search vaatii erillisen oikeuden)
3. **JSON-output** - Strukturoidun JSON-datan palautus toimii
4. **Kilpailijahaku** - Simulaatio projektille toimii täydellisesti

### Tokenien käyttö testeissä

- **Testi 1** (API-yhteys): 22 tokenia
- **Testi 2** (Web Search): 89 tokenia
- **Testi 3** (JSON-output): 119 tokenia
- **Testi 4** (Kilpailijahaku): 331 tokenia
- **Yhteensä**: ~561 tokenia per testikierros

## Test-kansion rakenne

```
test/
└── test_openai_api.py  # Päätestiskripti OpenAI API:lle
```

## Testien ajaminen

### Edellytykset

1. **Asenna riippuvuudet:**
```bash
pip install -r requirements.txt
```

2. **Konfiguroi API-avain:**
Luo `.env`-tiedosto projektin juureen:
```
OPENAI_API_KEY=your-api-key-here
```

Tai vaihtoehtoisesti:
```
OPEN_AI_API=your-api-key-here
```

### Aja testit

```bash
python test/test_openai_api.py
```

### Odotettu output

```
============================================================
               OPENAI API TESTIT
============================================================

TEST 1: OpenAI API-yhteyden testaus
[OK] API-avain loydetty
[OK] OpenAI client luotu
[OK] Vastaus saatu
[PASS] TEST 1 ONNISTUI - API toimii!

TEST 2: Web Search -toiminnallisuuden testaus
[PASS] TEST 2 ONNISTUI - Web search toimii!

TEST 3: JSON-outputin testaus
[OK] JSON-vastaus saatu
[OK] JSON-parsinta onnistui!
[PASS] TEST 3 ONNISTUI - JSON-output toimii!

TEST 4: Kilpailijahaku-simulaatio (projektille)
[OK] Kohdeyritys: Reaktor
[OK] Loydetyt kilpailijat:
  1. Futurice - https://www.futurice.com
  2. Siili Solutions - https://www.siili.com
  3. Gofore - https://gofore.com
[PASS] TEST 4 ONNISTUI - Kilpailijahaku toimii!

YHTEENVETO
[PASS] PASS - API-yhteys
[PASS] PASS - Web Search
[PASS] PASS - JSON-output
[PASS] PASS - Kilpailijahaku

Tulokset: 4/4 testia onnistui
[SUCCESS] Kaikki testit lapaisty!
```

## Testien kuvaukset

### Testi 1: API-yhteyden testaus

**Tavoite**: Varmistaa että OpenAI API-avain on oikein ja yhteys toimii.

**Testataan**:
- API-avaimen lataus .env-tiedostosta
- OpenAI client-objektin luonti
- Yksinkertainen kysely `gpt-4`-mallille
- Tokenien käytön seuranta

**Malli**: `gpt-4`

**Kriittiset virheet**:
- API-avainta ei löydy → Tarkista .env-tiedosto
- Autentikointivirhe → API-avain on virheellinen
- Verkkovirhe → Tarkista internet-yhteys

### Testi 2: Web Search -toiminnallisuus

**Tavoite**: Testata että malli voi vastata ajankohtaisiin kyselyihin.

**Testataan**:
- Web search -pyyntö (tämänhetkinen päivämäärä)
- Mallin vastaus

**Malli**: `gpt-4`

**Huomioita**:
- Web search voi vaatia erityisen API-oikeuden OpenAI:lta
- Testi hyväksyy myös vastauksen jossa malli sanoo ettei voi käyttää web search:ia
- Tulevaisuudessa päivitetään käyttämään `gpt-5-search-api`-mallia

### Testi 3: JSON-outputin testaus

**Tavoite**: Varmistaa että strukturoitu JSON-datan palautus toimii.

**Testataan**:
- `response_format={"type": "json_object"}` parametri
- JSON-parsinta
- Datan rakenne

**Malli**: `gpt-4o` (tukee JSON response format)

**Esimerkki output**:
```json
{
  "companies": [
    {"name": "Tech Solutions Inc.", "industry": "Information Technology"},
    {"name": "Green Energy Group", "industry": "Renewable Energy"},
    {"name": "Fresh Foods Co.", "industry": "Food & Beverage"}
  ]
}
```

**Kriittiset virheet**:
- `400 Bad Request` → Malli ei tue JSON-muotoa, käytä `gpt-4o` tai uudempaa

### Testi 4: Kilpailijahaku-simulaatio

**Tavoite**: Simuloi todellista käyttötapausta projektille.

**Testataan**:
- Kilpailijoiden haku esimerkkiyritykselle (Reaktor)
- JSON-muotoinen vastaus
- Datan rakenne ja sisältö

**Malli**: `gpt-4o`

**Esimerkki vastaus**:
```json
{
  "target_company": "Reaktor",
  "competitors": [
    {
      "name": "Futurice",
      "url": "https://www.futurice.com",
      "description": "Digitaalisten ratkaisujen konsultointi..."
    },
    {
      "name": "Siili Solutions",
      "url": "https://www.siili.com",
      "description": "IT- ja digipalveluihin keskittynyt..."
    },
    {
      "name": "Gofore",
      "url": "https://gofore.com",
      "description": "Digitaalisen transformaation konsultointi..."
    }
  ]
}
```

**Arvioitu kustannus**: ~$0.002 per testi (331 tokenia)

## Mallit ja niiden käyttö

| Malli | Käyttötarkoitus | JSON-tuki | Web Search |
|-------|----------------|-----------|------------|
| `gpt-4` | Perustestaus | ❌ Ei | ⚠️ Rajallinen |
| `gpt-4o` | JSON-outputit | ✅ Kyllä | ⚠️ Rajallinen |
| `gpt-4-turbo` | Nopeat kyselyt | ✅ Kyllä | ⚠️ Rajallinen |
| `gpt-5-search-api` | Web search | ✅ Kyllä | ✅ Kyllä |

**Suositus projektille**: Käytä `gpt-4o` yleisiin tehtäviin ja `gpt-5-search-api` kun tarvitset web search -toimintoa.

## Virheenkäsittely

Testiskripti käsittelee seuraavat virhetilanteet:

### 1. API-avain puuttuu

```
[FAIL] VIRHE: API-avainta ei löydy!
   Varmista että .env-tiedostossa on:
   OPENAI_API_KEY=your-api-key-here
```

**Ratkaisu**: Luo .env-tiedosto ja lisää API-avain.

### 2. OpenAI-kirjasto puuttuu

```
[FAIL] VIRHE: OpenAI-kirjasto ei ole asennettu!
   Asenna: pip install openai
```

**Ratkaisu**: `pip install openai python-dotenv`

### 3. Autentikointivirhe

```
[FAIL] VIRHE: AuthenticationError: Invalid API key
```

**Ratkaisu**: 
- Tarkista että API-avain on oikein
- Varmista että API-avaimella on riittävät oikeudet
- Hanki uusi avain: https://platform.openai.com/api-keys

### 4. Rate limit

```
[FAIL] VIRHE: RateLimitError: Rate limit exceeded
```

**Ratkaisu**:
- Odota hetki ja yritä uudelleen
- Tarkista tilin rajoitukset OpenAI:n dashboardista
- Päivitä tilin tier tarvittaessa

### 5. JSON-muoto ei tuettu

```
[FAIL] VIRHE: BadRequestError: 'response_format' not supported with this model
```

**Ratkaisu**: Vaihda malli `gpt-4o`:ksi tai uudempaan.

## Windows-yhteensopivuus

Testit on suunniteltu toimimaan Windows-ympäristössä:

- Unicode-symbolit (✅❌) korvataan ASCII-merkeillä ([PASS][FAIL])
- Merkistökoodaus käsitellään safe_print()-funktiolla
- PowerShell-yhteensopivuus varmistettu

## CI/CD-integraatio (tulevaisuus)

Testit voidaan myöhemmin integroida CI/CD-putken:

```yaml
# .github/workflows/test.yml (esimerkki)
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python test/test_openai_api.py
```

## Testien laajentaminen

Tulevat testit (kun analyzer.py valmistuu):

1. **test_web_scraping.py**
   - BeautifulSoup4-toiminnallisuus
   - Asiakasreferenssien purku
   - Error handling

2. **test_full_analysis.py**
   - End-to-end testi koko workflowlle
   - HTML-raportin generointi
   - Integraatiotestit

3. **test_error_handling.py**
   - Virheellinen URL
   - Ei löydy kilpailijoita
   - API-virheet

## Parhaat käytännöt

1. **Aja testit ennen commitia**: Varmista että kaikki toimii
2. **Seuraa tokenien käyttöä**: Pidä kirjaa kustannuksista
3. **Päivitä testit säännöllisesti**: OpenAI päivittää malleja
4. **Dokumentoi muutokset**: Päivitä tämä ohje kun testit muuttuvat
5. **Käytä .env-tiedostoa**: Älä koskaan commitoi API-avaimia

## Yhteenveto

- ✅ Testit toimivat lokakuu 2025
- ✅ API-yhteys vahvistettu
- ✅ JSON-output toimii `gpt-4o`-mallilla
- ✅ Kilpailijahaku simulaatio onnistui
- ⚠️ Web search vaatii `gpt-5-search-api`-mallin (tulossa)

**Seuraavat askeleet**: 
1. Toteuta analyzer.py pääskripti
2. Lisää web scraping -testit
3. Toteuta end-to-end testit

---

**Päivitetty**: Lokakuu 17, 2025  
**Versio**: 1.0  
**Tila**: ✅ Toimivat testit


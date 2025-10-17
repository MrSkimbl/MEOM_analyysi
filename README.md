# Kilpailija-analyysi-työkalu

Python-pohjainen komentorivityökalu, joka analysoi yrityksen ja sen kilpailijoiden positioning-vahvuudet eri asiakassegmenteissä hyödyntäen OpenAI:n API:a ja web search -toimintoa.

## Ominaisuudet

🔍 **Automaattinen kilpailija-analyysi**
- Hakee 5 kilpailijaa Suomen markkinassa
- Kerää asiakasreferenssit kaikkien yritysten sivustoilta
- Segmentoi asiakkaat automaattisesti
- Analysoi positioning-vahvuudet per segmentti
- Tuottaa selkeän HTML-raportin

## Projektin rakenne

```
.
├── docs/                    # Dokumentaatio
│   ├── project-plan.md     # Projektisuunnitelma
│   ├── workflow.md         # Yksityiskohtainen workflow
│   ├── openai-api-reference.md  # OpenAI API-dokumentaatio
│   └── testing-guide.md    # Testausohje
├── test/                   # Testit
│   ├── test_openai_api.py  # OpenAI API-testit
│   └── README.md           # Testausdokumentaatio
├── templates/              # HTML-raporttipohjat (tulossa)
├── .env                    # API-avaimet (ei versionhallinnassa)
├── .gitignore             # Git-ignoret
├── requirements.txt       # Python-riippuvuudet
├── analyzer.py            # Pääskripti (tulossa)
└── README.md              # Tämä tiedosto
```

## Asennus

### 1. Kloonaa repositorio

```bash
git clone <repo-url>
cd "MEOM, analyysi"
```

### 2. Asenna riippuvuudet

```bash
pip install -r requirements.txt
```

### 3. Konfiguroi OpenAI API-avain

Luo `.env`-tiedosto projektin juureen:

```
OPENAI_API_KEY=your-api-key-here
```

Hanki API-avain: https://platform.openai.com/api-keys

### 4. Testaa asennus

```bash
python test/test_openai_api.py
```

Jos kaikki 4 testiä läpäistään, asennus on valmis! ✅

## Käyttö (tulossa)

```bash
python analyzer.py --url https://example.com --output report.html
```

### Parametrit

- `--url`: Analysoitavan yrityksen URL (pakollinen)
- `--output`: HTML-raportin tiedostonimi (oletus: `report.html`)
- `--competitors`: Kilpailijoiden määrä (oletus: 5)

## Workflow

Työkalu suorittaa analyysin 7 vaiheessa:

1. **URL-validointi** - Tarkistaa että sivusto on tavoitettavissa
2. **Kilpailijoiden haku** - OpenAI web search löytää 5 kilpailijaa
3. **Asiakasreferenssien haku** - Kerää asiakkaiden nimet kaikkien sivustoilta
4. **Segmentointi** - OpenAI luo 4-6 asiakassegmenttiä
5. **Etusivujen copyt** - Hakee ja purkuu etusivujen päätekstit
6. **Positioning-analyysi** - Analysoi vahvuudet per segmentti (1-5 pistettä)
7. **HTML-raportti** - Generoi visuaalisen raportin

**Arvioitu suoritusaika**: 1-2 minuuttia per analyysi

Katso yksityiskohtainen kuvaus: [docs/workflow.md](docs/workflow.md)

## Dokumentaatio

- **[Project Plan](docs/project-plan.md)** - Korkean tason suunnitelma
- **[Workflow](docs/workflow.md)** - Yksityiskohtainen 7-vaiheinen prosessi
- **[OpenAI API Reference](docs/openai-api-reference.md)** - Ajantasainen API-dokumentaatio (2025)
- **[Testing Guide](docs/testing-guide.md)** - Testausohje ja tulokset

## Teknologiat

- **Python 3.12+** - Pääkieli
- **OpenAI API** - AI-analyysi ja web search
  - `gpt-4o` - JSON-outputit ja yleinen käyttö
  - `gpt-5-search-api` - Web search -toiminnot (tulossa)
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP-pyynnöt
- **python-dotenv** - Ympäristömuuttujat

## Testaus

### OpenAI API-testit

```bash
python test/test_openai_api.py
```

**Testitulokset (Lokakuu 17, 2025)**:
- ✅ API-yhteys toimii
- ✅ Web Search toimii
- ✅ JSON-output toimii
- ✅ Kilpailijahaku-simulaatio toimii

**Yhteensä**: 4/4 testiä läpäistiin onnistuneesti

Katso: [docs/testing-guide.md](docs/testing-guide.md)

## Kustannukset

Arvioitu OpenAI API-kustannus:
- **Per analyysi**: ~25,000 tokenia
- **Kustannus**: ~$0.10-0.25 per analyysi (riippuu mallista)

Tokenien käyttö per vaihe:
- Kilpailijahaku: ~2,000 tokenia
- Asiakasreferenssit (6×): ~15,000 tokenia
- Segmentointi: ~3,000 tokenia
- Positioning: ~5,000 tokenia

## Kehitystila

### ✅ Valmis

- [x] Projektin suunnittelu
- [x] Dokumentaatio
- [x] OpenAI API-integraatio ja testit
- [x] Test-kansion rakenne

### 🚧 Kehityksessä

- [ ] analyzer.py pääskripti
- [ ] Web scraping -toiminnallisuus
- [ ] HTML-raporttipohja
- [ ] End-to-end testit

### 📋 Suunniteltu

- [ ] CLI-parannukset (progress bar, verbose mode)
- [ ] PDF-export
- [ ] Batch-analyysi (useita URLeja kerralla)
- [ ] API-rate limiting
- [ ] Caching

## Turvallisuus

⚠️ **Tärkeää**:
- Älä koskaan commitoi `.env`-tiedostoa
- API-avain on henkilökohtainen - älä jaa sitä
- `.env` on lisätty `.gitignore`-tiedostoon

## Lisenssit

- OpenAI API: [OpenAI Terms of Use](https://openai.com/terms)
- Projekti: (Määritä tarvittaessa)

## Tuki ja palaute

Ongelmissa tai kysymyksissä:
1. Tarkista [docs/testing-guide.md](docs/testing-guide.md)
2. Aja testit: `python test/test_openai_api.py`
3. Tarkista [OpenAI Status](https://status.openai.com/)

## Versiohistoria

### v0.1.0 (Lokakuu 17, 2025)
- Projektin perustus
- Dokumentaatio luotu
- OpenAI API-testit toiminnassa
- Test-infrastruktuuri valmis

---

**Tila**: 🚧 Aktiivinen kehitys  
**Päivitetty**: Lokakuu 17, 2025  
**Python-versio**: 3.12+


# MEOM Competitor Analysis Tool

## Tavoite

Python-komentorivityökalu joka analysoi yrityksen kilpailuaseman Suomen markkinassa ja tuottaa HTML-raportin.

## Workflow (7 vaihetta)

1. **Yritysanalyysi** → Analysoi kohdeyritys
2. **Kilpailijahaku** → Etsi 5 kilpailijaa (Web Search)
3. **Asiakasreferenssit** → Hae asiakkaat 6 yritykseltä
4. **ICP-analyysi** → Luo 4-6 Ideal Customer Profilea
5. **Etusivujen copyt** → Scrappaa viestit
6. **Positioning-analyysi** → Analysoi vahvuudet per ICP
7. **HTML-raportti** → Generoi valmis raportti

## Teknologiat

- **Python 3.12+**
- **OpenAI GPT-5** (Responses API + Web Search)
- **BeautifulSoup4** (web scraping)
- **Requests** (HTTP)
- **python-dotenv** (env vars)

## Projektin rakenne

```
.
├── src/
│   ├── competitor_finder.py     # Vaihe 1-2
│   ├── customer_extractor.py    # Vaihe 3
│   ├── segmentation.py          # Vaihe 4
│   ├── copy_extractor.py        # Vaihe 5
│   ├── positioning.py           # Vaihe 6
│   └── report_generator.py      # Vaihe 7
├── docs/
│   ├── project-plan.md          # Tämä
│   ├── workflow.md              # Yksityiskohtainen workflow
│   ├── openai-api-reference.md  # API-dokumentaatio
│   └── style-guide.md           # HTML-tyyliopas
├── test/
│   └── test_openai_api.py       # API-testit
├── analyzer.py                  # Pääskripti
├── requirements.txt             # Riippuvuudet
├── .env                         # API-avain (ei gitissä)
└── .gitignore
```

## Asennus

```bash
# Kloonaa repo
git clone <repo-url>
cd "MEOM, analyysi"

# Asenna riippuvuudet
pip install -r requirements.txt

# Konfiguroi API-avain
echo "OPEN_AI_API=sk-..." > .env
```

## Käyttö

```bash
# Täysi analyysi (6 yritystä)
python analyzer.py --url https://yritys.fi --competitors 5

# Nopea testi (2 yritystä)
python analyzer.py --url https://yritys.fi --competitors 1

# Testaa vain tietty vaihe
python analyzer.py --url https://yritys.fi --step 4

# Määritä output-tiedosto
python analyzer.py --url https://yritys.fi --output raportti.html
```

## Parametrit

- `--url` (pakollinen) - Kohdeyrityksen URL
- `--competitors` (oletus: 5) - Kilpailijoiden määrä
- `--output` (oletus: report.html) - Output-tiedosto
- `--step` (valinnainen) - Aja vain tietty vaihe (1,3,4,5,6,7)

## Output

HTML-raportti sisältää:
- Executive summary (keskeiset oivallukset)
- ICP-johtajat (vahvimmat per ICP)
- Positioning-matriisi (pisteet 1-5)
- Yrityskohtaiset analyysit
- ICP-profiilit

## Kesto

- **Vaihe 1-2**: ~30-60s (GPT-5 + Web Search)
- **Vaihe 3**: ~2-4 min (scraping + GPT-5)
- **Vaihe 4**: ~30s (GPT-5)
- **Vaihe 5**: ~30-60s (scraping)
- **Vaihe 6**: ~30-60s (GPT-5)
- **Vaihe 7**: ~1s (HTML gen)

**Yhteensä**: 5-8 min (2 yritystä), 10-15 min (6 yritystä)

## API-kustannukset (arvio)

GPT-5 käyttö per täysi analyysi:
- ~4-6 kutsua (vaiheet 1,2,4,6)
- ~6-12 kutsua asiakkaille (vaihe 3)
- Yhteensä: ~10-18 GPT-5 kutsua

## Testaus

```bash
# Testaa OpenAI API
cd test
python test_openai_api.py

# Testaa vain vaihe 1
python analyzer.py --url https://reaktor.com --step 1
```

## Kehitysideat

- [ ] Tallenna välidata JSON:ksi (jatka keskeytyneestä)
- [ ] Lisää PDF-export
- [ ] Lisää kielivalinta (EN/FI)
- [ ] Syvempi teknografia-analyysi
- [ ] LinkedIn-integraatio (henkilöt)

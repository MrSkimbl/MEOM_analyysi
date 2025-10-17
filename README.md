# MEOM Competitor Analysis Tool

Python-komentorivityökalu joka analysoi yrityksen kilpailuaseman Suomen markkinassa ja tuottaa HTML-raportin.

## 🚀 Pikakäynnistys

```bash
# 1. Asenna riippuvuudet
pip install -r requirements.txt

# 2. Konfiguroi OpenAI API-avain
echo "OPEN_AI_API=sk-your-key-here" > .env

# 3. Aja analyysi
python analyzer.py --url https://yritys.fi --competitors 5
```

## 📊 Mitä työkalu tekee?

Analysoi kohdeyrityksen ja sen kilpailijat 7 vaiheessa:

1. **Yritysanalyysi** - Analysoi kohdeyrityksen palvelut ja asiakaskunta
2. **Kilpailijahaku** - Löytää 5 kilpailijaa Suomen markkinasta (Web Search)
3. **Asiakasreferenssit** - Kerää asiakasnimet kaikista 6 yrityksestä
4. **ICP-analyysi** - Luo 4-6 Ideal Customer Profilea
5. **Etusivujen copyt** - Scrappaa yritysten viestit
6. **Positioning-analyysi** - Arvioi vahvuudet per ICP (pisteet 1-5)
7. **HTML-raportti** - Generoi ammattimainen raportti

**Kesto**: 10-15 min (6 yritystä) | 5-8 min (2 yritystä)

## 📁 Projektin rakenne

```
.
├── src/                        # Lähdekoodit
│   ├── competitor_finder.py    # Vaiheet 1-2
│   ├── customer_extractor.py   # Vaihe 3
│   ├── segmentation.py         # Vaihe 4
│   ├── copy_extractor.py       # Vaihe 5
│   ├── positioning.py          # Vaihe 6
│   └── report_generator.py     # Vaihe 7
├── docs/                       # Dokumentaatio
│   ├── README.md               # Dokumentaatio-indeksi
│   ├── project-plan.md         # Projektisuunnitelma
│   ├── workflow.md             # Yksityiskohtainen workflow
│   ├── openai-api-reference.md # OpenAI API-ohjeet
│   └── style-guide.md          # HTML-tyyliopas
├── test/
│   └── test_openai_api.py      # API-testit
├── analyzer.py                 # PÄÄSKRIPTI
├── requirements.txt
└── .env                        # API-avain (älä commitoi!)
```

## 🔧 Käyttö

### Peruskomento

```bash
python analyzer.py --url https://yritys.fi
```

### Parametrit

| Parametri | Kuvaus | Oletus |
|-----------|--------|--------|
| `--url` | Kohdeyrityksen URL (pakollinen) | - |
| `--competitors` | Kilpailijoiden määrä | 5 |
| `--output` | Raportin tiedostonimi | report.html |
| `--step` | Aja vain tietty vaihe (testaus) | Kaikki |

### Esimerkkejä

```bash
# Täysi analyysi (6 yritystä)
python analyzer.py --url https://reaktor.com --competitors 5

# Nopea testi (2 yritystä)
python analyzer.py --url https://meom.fi --competitors 1

# Määritä output-tiedosto
python analyzer.py --url https://meom.fi --output meom-analyysi.html

# Testaa vain kilpailijahaku
python analyzer.py --url https://meom.fi --step 1

# Testaa ICP-analyysi
python analyzer.py --url https://meom.fi --competitors 1 --step 4
```

## 📦 Riippuvuudet

```
openai>=1.54.0        # GPT-5 Responses API + Web Search
beautifulsoup4        # Web scraping
requests              # HTTP-pyynnöt
python-dotenv         # Env-muuttujat
```

## 🔑 API-avain

Tarvitset OpenAI API-avaimen jolla on pääsy:
- GPT-5 malleihin
- Web Search -toimintoon

Lisää avain `.env`-tiedostoon:
```
OPEN_AI_API=sk-your-key-here
```

## 📈 Output (HTML-raportti)

Raportti sisältää:
- ✅ **Executive Summary** - Keskeiset oivallukset
- ✅ **ICP Leaders** - Vahvimmat toimijat per ICP
- ✅ **Positioning-matriisi** - Pisteet 1-5 (värikoodattu)
- ✅ **Yrityskohtaiset analyysit** - Vahvuudet ja heikkoudet
- ✅ **ICP-profiilit** - Yksityiskohtaiset asiakasprofiilit

**Tyyli**: MEOM brand (ks. `docs/style-guide.md`)

## 🧪 Testaus

```bash
# Testaa OpenAI API -yhteys
cd test
python test_openai_api.py

# Testaa vain kilpailijahaku (nopea)
python analyzer.py --url https://reaktor.com --step 1
```

## 💰 Kustannukset

Täysi analyysi (6 yritystä) käyttää:
- ~10-18 GPT-5 API-kutsua
- ~1-2 Web Search -toimintoa

Arvioitu hinta: $1-3 per analyysi (riippuen GPT-5 hinnoittelusta)

## 🐛 Yleisiä ongelmia

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "OpenAI API-avain puuttuu!"
```bash
echo "OPEN_AI_API=sk-..." > .env
```

### "UnicodeEncodeError" (Windows)
Työkalu käsittelee tämän automaattisesti. Jos ongelmia, aja PowerShellissä:
```bash
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📚 Dokumentaatio

Katso `/docs` kansio:
- **project-plan.md** - Projektin rakenne ja tavoitteet
- **workflow.md** - Yksityiskohtainen 7-vaiheinen kuvaus
- **openai-api-reference.md** - OpenAI API käyttö
- **style-guide.md** - HTML-raportin tyyliopas

## 🛠️ Kehitysideat

- [ ] JSON-välidata (jatka keskeytyneestä)
- [ ] PDF-export
- [ ] Kielivalinta (EN/FI)
- [ ] LinkedIn-integraatio
- [ ] Syvempi teknografia-analyysi

## 📄 Lisenssi

MEOM internal tool

## 🤝 Tekijä

MEOM - B2B-verkkosivut ja digitaalinen kehitys

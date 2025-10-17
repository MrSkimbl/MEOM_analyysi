# Kilpailija-analyysi-työkalu - Projektisuunnitelma

## Tavoite

Rakennetaan Python-pohjainen komentorivityökalu, joka:
1. Ottaa vastaan URL:n
2. Hakee 5 kilpailijaa Suomen markkinassa
3. Hakee kaikkien kuuden yrityksen asiakasreferenssit
4. Muotoilee asiakkaista segmentit
5. Hakee etusivujen copyt
6. Analysoi positioning-vahvuudet per segmentti
7. Tuottaa HTML-raportin

## Projektin rakenne

```
.
├── docs/                    # Dokumentaatio
│   ├── project-plan.md     # Tämä tiedosto
│   └── workflow.md         # Workflow-kuvaus
├── templates/
│   └── report_template.html # HTML-raporttipohja
├── .env.example            # API-avaimen template
├── .gitignore             # Python ja .env
├── requirements.txt       # Riippuvuudet
├── README.md             # Käyttöohjeet
└── analyzer.py           # Pääskripti
```

## Teknologiat

- **Python 3.8+**: Pääkieli
- **OpenAI API**: AI-analyysi ja web search
  - ChatCompletion API viimeisimmällä mallilla (gpt-4o tai uudempi)
  - Web search -toiminnallisuus kilpailijoiden haussa
- **BeautifulSoup4**: Web scraping
- **Requests**: HTTP-pyynnöt
- **python-dotenv**: Ympäristömuuttujat
- **argparse**: Komentoriviparametrit

## Toteutus vaiheittain

### Vaihe 1: Projektin perustus
- [x] Luo dokumentaatiokansio
- [ ] Luo `requirements.txt` riippuvuuksilla
- [ ] Luo `.env.example` API-avain templatella
- [ ] Luo `.gitignore` Python-projekteille
- [ ] Luo `README.md` käyttöohjeilla

### Vaihe 2: Pääskripti (analyzer.py)
- [ ] Luo `CompetitorAnalyzer`-luokka
- [ ] Toteuta `find_competitors()` - OpenAI search
- [ ] Toteuta `extract_customer_references()` - Web scraping + AI
- [ ] Toteuta `segment_customers()` - AI-segmentointi
- [ ] Toteuta `extract_homepage_copy()` - Web scraping
- [ ] Toteuta `analyze_positioning()` - AI-analyysi
- [ ] Toteuta `generate_html_report()` - Raportin generointi

### Vaihe 3: HTML-template
- [ ] Luo templates-kansio
- [ ] Suunnittele raportin rakenne
- [ ] Toteuta HTML-template

### Vaihe 4: Testaus
- [ ] Testaa työkalu esimerkkiURLilla
- [ ] Dokumentoi tulokset
- [ ] Viimeistele README

## Käyttö

```bash
# Asenna riippuvuudet
pip install -r requirements.txt

# Määritä API-avain
cp .env.example .env
# Lisää OPENAI_API_KEY .env-tiedostoon

# Aja analyysi
python analyzer.py --url https://example.com --output report.html
```

## OpenAI-integraation yksityiskohdat

### Kilpailijoiden haku
- Prompti: "Etsi 5 pääkilpailijaa yritykselle [URL] Suomen markkinassa"
- Käytetään web search -toimintoa reaaliaikaiseen tietoon

### Segmentointi
- Kerätään kaikkien 6 yrityksen asiakasnimet
- Prompti: "Analysoi nämä asiakkaat ja luo loogisia asiakassegmenttejä"

### Positioning-analyysi
- Syöte: Yritykset, segmentit, etusivujen copyt
- Prompti: "Analysoi miten kunkin yrityksen viesti resonoi eri segmenttien kanssa"
- Output: Vahvuusmatriisi

## Huomiot

- Työkalu on read-only: ei tee muutoksia mihinkään sivustoihin
- Rate limiting: Huomioidaan OpenAI API-rajoitukset
- Virheenkäsittely: Graceful degradation jos sivustoja ei saada haettua
- Privacy: Ei tallenneta henkilötietoja


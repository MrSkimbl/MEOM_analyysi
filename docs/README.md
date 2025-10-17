# MEOM Competitor Analysis Tool - Dokumentaatio

## Pikakäynnistys

```bash
# Asenna riippuvuudet
pip install -r requirements.txt

# Konfiguroi API-avain
echo "OPEN_AI_API=your-key-here" > .env

# Aja analyysi
python analyzer.py --url https://esimerkki.fi --competitors 5
```

## Dokumentit

- **project-plan.md** - Projektin rakenne ja tavoitteet
- **workflow.md** - 7-vaiheinen analyysi-workflow
- **openai-api-reference.md** - OpenAI API käyttö (GPT-5, Web Search)
- **style-guide.md** - HTML-raportin tyyliopas (MEOM brand)

## Työkalun rakenne

```
src/
├── competitor_finder.py    # Vaihe 1: Yritysanalyysi + kilpailijat
├── customer_extractor.py   # Vaihe 3: Asiakasreferenssit
├── segmentation.py         # Vaihe 4: ICP-analyysi
├── copy_extractor.py       # Vaihe 5: Etusivujen copyt
├── positioning.py          # Vaihe 6: Positioning-analyysi
└── report_generator.py     # Vaihe 7: HTML-raportti

analyzer.py                 # Pääskripti
```

## Workflow (7 vaihetta)

1. **Yritysanalyysi** - Analysoi kohdeyritys GPT-5:llä
2. **Kilpailijahaku** - Etsi 5 kilpailijaa (GPT-5 + Web Search)
3. **Asiakasreferenssit** - Scrappaa + poimi asiakasnimet (GPT-5)
4. **ICP-analyysi** - Luo 4-6 Ideal Customer Profilea (GPT-5)
5. **Etusivujen copyt** - Scrappaa yritysten viestit (BeautifulSoup)
6. **Positioning** - Analysoi viestien vahvuus per ICP (GPT-5)
7. **HTML-raportti** - Generoi valmis raportti (MEOM style)

## Kesto

- Nopea (2 yritystä): ~5-8 min
- Täysi (6 yritystä): ~10-15 min

## API-käyttö

- **GPT-5 Responses API** vaiheissa 1, 2, 4, 6
- **Web Search** vain vaiheessa 2 (kilpailijahaku)
- **BeautifulSoup** vaiheissa 3, 5 (web scraping)


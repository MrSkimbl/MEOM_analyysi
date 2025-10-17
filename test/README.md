# Test-kansio

Tämä kansio sisältää kaikki projektin testit.

## Testit

### test_openai_api.py

Testaa OpenAI API-integraation:
- API-yhteys
- Web Search -toiminnallisuus
- JSON-outputit
- Kilpailijahaku-simulaatio

**Aja testit:**
```bash
python test/test_openai_api.py
```

**Edellytykset:**
- `.env`-tiedosto API-avaimella
- `pip install openai python-dotenv`

## Dokumentaatio

Katso yksityiskohtainen ohjeistus: [../docs/testing-guide.md](../docs/testing-guide.md)

## Testitulosten yhteenveto

Viimeisin testikierros: **Lokakuu 17, 2025**

| Testi | Tila | Tokeneja |
|-------|------|----------|
| API-yhteys | ✅ PASS | 22 |
| Web Search | ✅ PASS | 89 |
| JSON-output | ✅ PASS | 119 |
| Kilpailijahaku | ✅ PASS | 331 |

**Yhteensä**: 4/4 testiä läpäistiin onnistuneesti.


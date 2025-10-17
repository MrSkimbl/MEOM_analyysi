# OpenAI API Reference - GPT-5 ja Web Search

## Tärkeää: Responses API vs Chat Completions API

**Tässä projektissa käytetään RESPONSES API**, ei Chat Completions API:a.

### Miksi Responses API?

- ✅ GPT-5 tuki
- ✅ Web Search toimii (`tools=[{"type": "web_search"}]`)
- ✅ Yksinkertaisempi käyttöliittymä

### Milloin Chat Completions?

- Vain GPT-4o ja vanhemmat mallit
- Web Search **ei** toimi
- Monimutkaisempi (`messages` array)

---

## GPT-5 Responses API (käytetään tässä projektissa)

### Perus käyttö (EI web search)

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

response = client.responses.create(
    model="gpt-5",
    input="Analysoi yritys osoitteessa https://esimerkki.fi"
)

print(response.output_text)
```

### Web Search (VAIN kilpailijahaussa)

```python
response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],  # Aktivoi web search
    input="Etsi kilpailijat yritykselle X Suomen markkinassa"
)

print(response.output_text)
```

### JSON-muotoinen vastaus

```python
import json

response = client.responses.create(
    model="gpt-5",
    input="""Analysoi yritys ja palauta JSON:
{
  "name": "...",
  "services": ["...", "..."]
}

TÄRKEÄÄ: Palauta VAIN JSON, ei muuta tekstiä.
"""
)

data = json.loads(response.output_text)
```

---

## Projektin käyttö per vaihe

| Vaihe | API | Web Search | Prompt-tyyppi |
|-------|-----|-----------|---------------|
| 1A: Yritysanalyysi | GPT-5 Responses | ❌ | JSON output |
| 1B: Kilpailijahaku | GPT-5 Responses | ✅ | JSON output + Web |
| 3: Asiakasnimet | GPT-5 Responses | ❌ | JSON output |
| 4: ICP-analyysi | GPT-5 Responses | ❌ | JSON output |
| 5: Etusivujen copyt | - | - | BeautifulSoup |
| 6: Positioning | GPT-5 Responses | ❌ | JSON output |
| 7: HTML-raportti | - | - | Python templating |

---

## Tärkeät parametrit

### ✅ Tuetut parametrit (GPT-5)

```python
response = client.responses.create(
    model="gpt-5",                           # Malli
    input="prompt tähän",                    # Syöte (string)
    tools=[{"type": "web_search"}],          # Web search (valinnainen)
)
```

### ❌ EI tuetut parametrit

```python
# ÄLÄTEE NÄIN GPT-5:llä:
response = client.responses.create(
    model="gpt-5",
    messages=[...],              # ❌ Vain Chat Completions API:ssa
    max_tokens=1000,             # ❌ Käytä max_completion_tokens
    temperature=0.7,             # ❌ Vain oletus (1) tuettu
    response_format={"type": "json_object"}  # ❌ Ei tarvita, JSON toimii suoraan
)
```

---

## JSON-parsinta (paras käytäntö)

```python
import json

try:
    response = client.responses.create(
        model="gpt-5",
        input="""Palauta JSON:
{
  "key": "value"
}

TÄRKEÄÄ: Palauta VAIN JSON, ei selityksiä."""
    )
    
    # Parsi JSON
    data = json.loads(response.output_text)
    
except json.JSONDecodeError as e:
    print(f"JSON-parsinta epäonnistui!")
    print(f"Vastaus: {response.output_text[:500]}")
    # Debug: katsele raakadataa
    raise
```

---

## Web Search - Milloin käyttää?

### ✅ Käytä web searchissa:
- Kilpailijahaku (tarvitaan ajantasaista markkinatietoa)
- Tuoreita uutisia tarvittaessa

### ❌ ÄLÄ käytä web searchia:
- JSON-parsinta (asiakasnimet, ICP:t)
- Analyysi joka perustuu annettuun tekstiin
- Kaikki tekstipohjainen analyysi

**Syy**: Web search hidastaa ja maksaa enemmän. Käytä vain kun tarvitaan reaaliaikaista tietoa.

---

## Virheenkäsittely

```python
from openai import OpenAI
import json

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    
    # Parsi JSON
    result = json.loads(response.output_text)
    
except json.JSONDecodeError as e:
    print(f"[ERROR] JSON-parsinta epäonnistui")
    print(f"Vastaus: {response.output_text[:500]}")
    raise
    
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)}")
    raise
```

---

## Mallit

| Malli | API | Web Search | JSON | Käyttö projektissa |
|-------|-----|-----------|------|-------------------|
| `gpt-5` | Responses | ✅ | ✅ | **Kaikki vaiheet** |
| `gpt-4o` | Chat Completions | ❌ | ✅ | Ei käytössä |
| `gpt-4` | Chat Completions | ❌ | ❌ | Ei käytössä |

---

## Esimerkki: Kilpailijahaku (Web Search)

```python
from openai import OpenAI
import json

client = OpenAI()

prompt = """
Yritys: Reaktor Oy (https://reaktor.com)
Palvelut: Digitaalinen transformaatio, ohjelmistokehitys
Asiakkaat: Suuryritykset ja julkishallinto

Etsi 5 kilpailijaa Suomen markkinassa.

Palauta JSON:
{
  "competitors": [
    {"name": "Yritys", "url": "https://..."}
  ]
}
"""

response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],  # AKTIVOI WEB SEARCH
    input=prompt
)

data = json.loads(response.output_text)
print(data['competitors'])
```

---

## Yhteenveto

1. **Käytä `client.responses.create`** - EI `chat.completions.create`
2. **Käytä `input` parametria** - EI `messages`
3. **Web search** vain kilpailijahaussa (`tools=[{"type": "web_search"}]`)
4. **JSON** toimii suoraan, ei tarvita `response_format`
5. **Virheenkäsittely** aina JSON-parsinnassa

## Dokumentaatio

Virallinen dokumentaatio: https://platform.openai.com/docs/guides/tools-web-search?api-mode=responses&lang=python

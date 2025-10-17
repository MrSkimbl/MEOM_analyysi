# OpenAI API - Responses API & Web Search (2025)

## Responses API - Uusi tapa

OpenAI:n **Responses API** on uusi, yksinkertaisempi tapa käyttää GPT-5:tä.

### Perusesimerkki

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Analysoi yritys Reaktor.com"
)

print(response.output_text)
```

### Web Search -työkalu

```python
response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input="Etsi kilpailijat yritykselle Reaktor.com Suomessa"
)

print(response.output_text)
```

### JSON-output

```python
response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input="Palauta JSON: Reaktorin kilpailijat Suomessa",
    response_format="json"
)

import json
data = json.loads(response.output_text)
```

## Mallit

- `gpt-5` - Paras malli, tukee web search:ia
- `gpt-5-mini` - Nopeampi, halvempi

## Parametrit (Responses API)

| Parametri | Kuvaus |
|-----------|--------|
| `model` | "gpt-5" tai "gpt-5-mini" |
| `input` | Syöte (string) |
| `tools` | Lista: [{"type": "web_search"}] |
| `response_format` | "json" jos haluat JSON |
| `max_tokens` | HUOM: GPT-5 ei välttämättä tue, kokeile ilman |

## Vastauksen käsittely

```python
response = client.responses.create(...)

# Tekstivastaus
text = response.output_text

# Tokenien käyttö (jos saatavilla)
if hasattr(response, 'usage'):
    tokens = response.usage.total_tokens
```

## Projektissa käytettävä koodi

### Yritysanalyysi (ilman web search)

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input=f"Analysoi yritys {url}. Palauta JSON muodossa..."
)

data = json.loads(response.output_text)
```

### Kilpailijahaku (web search)

```python
response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input=f"Etsi 5 kilpailijaa {url}. Palauta JSON..."
)

data = json.loads(response.output_text)
```

## Virheenkäsittely

```python
try:
    response = client.responses.create(...)
except Exception as e:
    print(f"Virhe: {e}")
```

---

**Lähde**: OpenAI Platform Docs - Responses API  
**Päivitetty**: Lokakuu 2025

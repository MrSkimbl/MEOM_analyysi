"""
Vaihe 1: Kohdeyrityksen analyysi ja kilpailijoiden haku OpenAI:lla
"""

import os
from openai import OpenAI
import json


def safe_print(text):
    """Windows-yhteensopiva tulostus"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Korvaa ongelmalliset merkit
        text = text.encode('ascii', 'ignore').decode('ascii')
        print(text)


def analyze_target_company(target_url: str, api_key: str = None) -> dict:
    """
    Analysoi kohdeyrityksen palvelut, asiakkaat ja positioning
    
    Args:
        target_url: Kohdeyrityksen URL
        api_key: OpenAI API-avain
        
    Returns:
        dict: {
            "company_name": "Yrityksen nimi",
            "url": "https://...",
            "services": ["Palvelu 1", "Palvelu 2", ...],
            "products": ["Tuote 1", "Tuote 2", ...],
            "target_customers": "Kuvaus asiakaskunnasta",
            "customer_segments": ["Segmentti 1", "Segmentti 2", ...],
            "value_proposition": "Pääviesti",
            "analysis": "Vapaamuotoinen analyysi"
        }
    """
    
    # Hae API-avain
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    
    if not api_key:
        raise ValueError("OpenAI API-avain puuttuu!")
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Analysoi yritys osoitteessa {target_url} ja palauta VAIN JSON (ei muuta tekstiä).

TÄRKEÄÄ:
- Tee paras mahdollinen analyysi saatavilla olevan tiedon perusteella
- ÄLÄ kysy mitään, vaan anna paras arvio
- Palauta PELKKÄ JSON-objekti, ei selityksiä

Analysoi:
1. Yrityksen nimi
2. Pääpalvelut ja tuotteet
3. Asiakaskunta (toimialat, yrityskokoat)
4. Value proposition
5. Lyhyt yhteenveto

JSON-rakenne (PAKOLLINEN):
{{
    "company_name": "Yrityksen nimi",
    "url": "{target_url}",
    "services": ["Palvelu 1", "Palvelu 2"],
    "products": ["Tuote 1"],
    "target_customers": "Kuvaus asiakaskunnasta",
    "customer_segments": ["Segmentti 1", "Segmentti 2"],
    "value_proposition": "Ydinviesti",
    "analysis": "Yhteenveto yrityksestä"
}}

Palauta VAIN ylläoleva JSON, ei muuta."""
    
    print(f"[1/2] Analysoidaan yritys: {target_url}")
    print("  - Kaytetaan GPT-5 Responses API...")
    
    # RESPONSES API - uusi tapa!
    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )
    
    # Debug
    print(f"[DEBUG] Response tyyppi: {type(response)}")
    print(f"[DEBUG] Response attribuutit: {dir(response)}")
    if hasattr(response, 'output_text'):
        print(f"[DEBUG] output_text pituus: {len(response.output_text)}")
        print(f"[DEBUG] output_text (200 merkkia): {response.output_text[:200]}")
    
    # Parsi vastaus
    result = json.loads(response.output_text)
    
    print(f"[OK] Yritysanalyysi valmis!")
    print(f"  - Yritys: {result.get('company_name', 'N/A')}")
    print(f"  - Palveluita: {len(result.get('services', []))}")
    
    return result


def find_competitors(target_url: str, count: int = 5, api_key: str = None, company_analysis: dict = None) -> dict:
    """
    Hakee kilpailijat yritykselle OpenAI:n avulla
    
    Args:
        target_url: Kohdeyrityksen URL
        count: Kuinka monta kilpailijaa haetaan (oletus: 5)
        api_key: OpenAI API-avain (jos None, haetaan ympäristömuuttujasta)
        company_analysis: Yritysanalyysi vaiheesta 1a (jos None, tehdään ensin analyysi)
        
    Returns:
        dict: {
            "target_company": "Yrityksen nimi",
            "target_url": "https://...",
            "company_analysis": {...},
            "competitors": [
                {
                    "name": "Kilpailija 1",
                    "url": "https://...",
                    "description": "Kuvaus",
                    "similarity_reason": "Miksi kilpailija"
                }
            ]
        }
    """
    
    # Hae API-avain
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    
    if not api_key:
        raise ValueError("OpenAI API-avain puuttuu! Aseta OPENAI_API_KEY ympäristömuuttujaan.")
    
    # Jos yritysanalyysia ei ole annettu, tee se ensin
    if company_analysis is None:
        print("\n[INFO] Yritysanalyysia ei annettu, tehdaan ensin...\n")
        company_analysis = analyze_target_company(target_url, api_key)
    
    # Luo OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Muodosta konteksti yritysanalyysista
    company_context = f"""
    KOHDEYRITYKSEN ANALYYSI:
    Yritys: {company_analysis.get('company_name', 'N/A')}
    URL: {company_analysis.get('url', target_url)}
    
    Palvelut: {', '.join(company_analysis.get('services', []))}
    Tuotteet: {', '.join(company_analysis.get('products', []))}
    
    Asiakaskunta: {company_analysis.get('target_customers', 'N/A')}
    Asiakassegmentit: {', '.join(company_analysis.get('customer_segments', []))}
    
    Value Proposition: {company_analysis.get('value_proposition', 'N/A')}
    
    Analyysi: {company_analysis.get('analysis', 'N/A')}
    """
    
    # Muodosta prompt
    prompt = f"""
    {company_context}
    
    TEHTÄVÄ:
    Etsi {count} pääkilpailijaa tälle yritykselle Suomen markkinassa.
    
    Kilpailijat tulee valita seuraavien kriteereiden perusteella:
    1. Tarjoavat samankaltaisia palveluita/tuotteita
    2. Palvelevat samankaltaista asiakaskuntaa (huomioi yrityskokojen samankaltaisuus)
    3. Toimivat Suomessa tai palvelevat aktiivisesti Suomen markkinaa
    4. Ovat todellisia, olemassa olevia yrityksiä
    5. Kilpailevat suorasti tai epäsuorasti samasta asiakaskunnasta
    
    Palauta vastaus JSON-muodossa:
    {{
        "target_company": "{company_analysis.get('company_name', 'N/A')}",
        "competitors": [
            {{
                "name": "Kilpailijan virallinen nimi",
                "url": "https://kilpailijan-verkkosivu.fi",
                "description": "1-2 lauseen kuvaus yrityksestä",
                "similarity_reason": "Miksi tämä on relevantti kilpailija (palvelut, asiakkaat, markkina-asema)"
            }}
        ]
    }}
    
    Varmista että:
    - Löydät täsmälleen {count} kilpailijaa
    - Kaikki kilpailijat ovat relevantteja kohdeyrityksen analyysiin nähden
    - URL:t ovat toimivia
    - similarity_reason selittää selkeästi kilpailija-aseman
    """
    
    print(f"\n[2/2] Haetaan kilpailijoita...")
    print("  - Kaytetaan GPT-5 WEB SEARCH...")
    
    # RESPONSES API + WEB SEARCH
    response = client.responses.create(
        model="gpt-5",
        tools=[{"type": "web_search"}],  # AKTIVOI WEB SEARCH
        input=prompt
    )
    
    # Parsi vastaus
    result = json.loads(response.output_text)
    
    # Lisää kohdeyrityksen URL ja analyysi
    result["target_url"] = target_url
    result["company_analysis"] = company_analysis
    
    print(f"[OK] Kilpailijahaku valmis!")
    print(f"  - Loydettiin: {len(result.get('competitors', []))} kilpailijaa")
    
    return result


def validate_competitor_data(data: dict) -> bool:
    """
    Validoi että kilpailijoiden data on oikeassa muodossa
    
    Args:
        data: Kilpailijoiden data
        
    Returns:
        bool: True jos data on validia
    """
    required_fields = ["target_company", "target_url", "competitors"]
    
    for field in required_fields:
        if field not in data:
            print(f"Virhe: Pakollinen kenttä '{field}' puuttuu!")
            return False
    
    if not isinstance(data["competitors"], list):
        print("Virhe: 'competitors' pitää olla lista!")
        return False
    
    for i, comp in enumerate(data["competitors"]):
        if not all(key in comp for key in ["name", "url", "description"]):
            print(f"Virhe: Kilpailijalta {i+1} puuttuu pakollisia kenttiä!")
            return False
    
    return True


def print_company_analysis(analysis: dict):
    """
    Tulostaa yritysanalyysin yhteenvedon
    
    Args:
        analysis: Yritysanalyysi
    """
    print("\n" + "=" * 60)
    print("YRITYSANALYYSI")
    print("=" * 60)
    
    print(f"\nYritys: {analysis.get('company_name', 'N/A')}")
    print(f"URL: {analysis.get('url', 'N/A')}")
    
    safe_print(f"\nPalvelut:")
    for service in analysis.get('services', []):
        safe_print(f"  - {service}")
    
    if analysis.get('products'):
        safe_print(f"\nTuotteet:")
        for product in analysis.get('products', []):
            safe_print(f"  - {product}")
    
    safe_print(f"\nAsiakaskunta: {analysis.get('target_customers', 'N/A')}")
    
    safe_print(f"\nAsiakassegmentit:")
    for segment in analysis.get('customer_segments', []):
        safe_print(f"  - {segment}")
    
    safe_print(f"\nValue Proposition:")
    safe_print(f"  {analysis.get('value_proposition', 'N/A')}")
    
    print("\n" + "=" * 60)


def print_competitor_summary(data: dict):
    """
    Tulostaa kilpailijoiden yhteenvedon
    
    Args:
        data: Kilpailijoiden data
    """
    print("\n" + "=" * 60)
    print("KILPAILIJAHAKU - YHTEENVETO")
    print("=" * 60)
    
    print(f"\nKohdeyritys: {data.get('target_company', 'N/A')}")
    print(f"URL: {data.get('target_url', 'N/A')}")
    
    print(f"\nLoydetyt kilpailijat ({len(data.get('competitors', []))}):")
    print("-" * 60)
    
    for i, comp in enumerate(data.get('competitors', []), 1):
        safe_print(f"\n{i}. {comp.get('name', 'N/A')}")
        safe_print(f"   URL: {comp.get('url', 'N/A')}")
        safe_print(f"   Kuvaus: {comp.get('description', 'N/A')}")
        if comp.get('similarity_reason'):
            safe_print(f"   Kilpailija koska: {comp.get('similarity_reason', 'N/A')}")
    
    print("\n" + "=" * 60)


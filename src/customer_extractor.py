"""
Vaihe 3: Asiakasreferenssien haku
BeautifulSoup4 + OpenAI
"""

import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json
import time
from urllib.parse import urljoin, urlparse


def find_customer_pages(base_url: str) -> list[str]:
    """
    Kokeilee löytää asiakassivuja yritykseltä
    
    Args:
        base_url: Yrityksen pääsivu
        
    Returns:
        Lista mahdollisista asiakassivujen URL:eista
    """
    # Yleisimmät polut asiakassivuille
    common_paths = [
        '/asiakkaat',
        '/referenssit', 
        '/cases',
        '/customers',
        '/portfolio',
        '/work',
        '/projektit',
        '/clients',
        '/references'
    ]
    
    candidate_urls = []
    
    # Yhdistä base_url ja polut
    for path in common_paths:
        url = urljoin(base_url, path)
        candidate_urls.append(url)
    
    # Testaa myös pääsivu
    candidate_urls.insert(0, base_url)
    
    return candidate_urls


def scrape_page_text(url: str, timeout: int = 10) -> str:
    """
    Hakee sivun ja poimii tekstisisällön
    
    Args:
        url: Sivun URL
        timeout: Timeout sekunneissa
        
    Returns:
        Sivun tekstisisältö (tyhjä string jos epäonnistui)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Parsi HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Poista turha sisältö
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Hae tekstit
        text = soup.get_text(separator=' ', strip=True)
        
        # Puhdista ylimääräiset välilyönnit
        text = ' '.join(text.split())
        
        return text
        
    except requests.Timeout:
        print(f"  [WARN] Timeout: {url}")
        return ""
    except requests.RequestException as e:
        print(f"  [WARN] Virhe haettaessa {url}: {type(e).__name__}")
        return ""
    except Exception as e:
        print(f"  [WARN] Odottamaton virhe {url}: {type(e).__name__}")
        return ""


def extract_customer_names(text: str, company_name: str, api_key: str = None) -> list[str]:
    """
    Poimii asiakasnimet tekstistä OpenAI:lla
    
    Args:
        text: Tekstisisältö sivulta
        company_name: Yrityksen nimi (kontekstia varten)
        api_key: OpenAI API-avain
        
    Returns:
        Lista asiakasnimiä
    """
    if not text or len(text) < 50:
        return []
    
    # Hae API-avain
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    
    if not api_key:
        raise ValueError("OpenAI API-avain puuttuu!")
    
    client = OpenAI(api_key=api_key)
    
    # Rajoita tekstin pituutta (max ~3000 sanaa)
    words = text.split()[:3000]
    text_limited = ' '.join(words)
    
    prompt = f"""Etsi KAIKKI yritys- ja organisaatioiden nimet seuraavasta tekstistä yrityksen {company_name} sivuilta.

TÄRKEÄÄ:
- Etsi VAIN yritysten ja organisaatioiden nimet (ei henkilönimiä)
- Palauta PELKKÄ JSON-lista, ei selityksiä
- Jos et löydä yhtään, palauta tyhjä lista: {{"customers": []}}

Teksti:
{text_limited}

Palauta JSON:
{{
    "customers": ["Yritys 1", "Yritys 2", "Yritys 3"]
}}

VAIN JSON, ei muuta tekstiä."""
    
    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        # Parsi JSON
        result = json.loads(response.output_text)
        customers = result.get('customers', [])
        
        # Suodata tyhjät ja liian lyhyet
        customers = [c.strip() for c in customers if c and len(c.strip()) > 2]
        
        return customers
        
    except json.JSONDecodeError:
        print(f"  [WARN] JSON-parsinta epaonnistui yritykselle {company_name}")
        return []
    except Exception as e:
        print(f"  [WARN] Virhe asiakasnimienpoiminnassa: {type(e).__name__}")
        return []


def get_all_customers(company_url: str, company_name: str, api_key: str = None) -> list[str]:
    """
    Hakee kaikki asiakkaat yrityksen sivuilta
    
    Args:
        company_url: Yrityksen URL
        company_name: Yrityksen nimi
        api_key: OpenAI API-avain
        
    Returns:
        Lista uniikkeja asiakasnimiä
    """
    print(f"\n  Haetaan asiakkaita: {company_name}")
    print(f"    URL: {company_url}")
    
    all_customers = []
    
    # 1. Etsi mahdolliset asiakassivut
    candidate_urls = find_customer_pages(company_url)
    print(f"    Kokeillaan {len(candidate_urls)} sivua...")
    
    # 2. Käy läpi sivut
    for url in candidate_urls:
        # Pieni viive ettei tule rate limitiä
        time.sleep(0.5)
        
        # Scrape sivu
        text = scrape_page_text(url)
        
        if not text:
            continue
        
        # Jos sivulla on sanoja "asiakas", "referenssi", "case" jne, todennäköisesti oikea sivu
        keywords = ['asiakas', 'referenssi', 'case', 'customer', 'client', 'portfolio', 'työ']
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in keywords) or url == company_url:
            print(f"    [OK] Loydetty potentiaalinen sivu: {url[:60]}...")
            
            # Poimi asiakasnimet
            customers = extract_customer_names(text, company_name, api_key)
            
            if customers:
                print(f"    [OK] Loydetty {len(customers)} asiakasta")
                all_customers.extend(customers)
            else:
                print(f"    [-] Ei asiakkaita taalta")
        
        # Jos löysimme jo paljon asiakkaita, ei tarvitse jatkaa
        if len(all_customers) > 20:
            break
    
    # 3. Poista duplikaatit
    unique_customers = list(set(all_customers))
    
    print(f"    [DONE] Yhteensa {len(unique_customers)} uniikkia asiakasta")
    
    return unique_customers


def extract_all_companies_customers(companies: list[dict], api_key: str = None) -> dict:
    """
    Hakee kaikkien yritysten asiakkaat
    
    Args:
        companies: Lista yrityksiä (dict: name, url)
        api_key: OpenAI API-avain
        
    Returns:
        Dictionary: {yritys_nimi: [asiakas1, asiakas2, ...]}
    """
    print("\n" + "=" * 60)
    print("ASIAKASREFERENSSIEN HAKU")
    print("=" * 60)
    print(f"\nHaetaan asiakkaita {len(companies)} yritykselta...")
    
    customers_by_company = {}
    
    for i, company in enumerate(companies, 1):
        name = company.get('name', 'N/A')
        url = company.get('url', '')
        
        print(f"\n[{i}/{len(companies)}] {name}")
        
        if not url:
            print("  [SKIP] URL puuttuu")
            customers_by_company[name] = []
            continue
        
        try:
            customers = get_all_customers(url, name, api_key)
            customers_by_company[name] = customers
            
        except Exception as e:
            print(f"  [ERROR] {type(e).__name__}: {str(e)}")
            customers_by_company[name] = []
        
        # Pieni tauko yritysten välissä
        if i < len(companies):
            time.sleep(1)
    
    return customers_by_company


def print_customer_summary(customers_by_company: dict):
    """Tulostaa yhteenvedon asiakkaista"""
    print("\n" + "=" * 60)
    print("ASIAKASREFERENSSIT - YHTEENVETO")
    print("=" * 60)
    
    total_customers = sum(len(customers) for customers in customers_by_company.values())
    
    print(f"\nYhteensa {total_customers} asiakasta loytyi {len(customers_by_company)} yritykselta:")
    print("-" * 60)
    
    for company, customers in customers_by_company.items():
        print(f"\n{company}: {len(customers)} asiakasta")
        if customers:
            # Näytä max 5 ensimmäistä
            for customer in customers[:5]:
                print(f"  - {customer}")
            if len(customers) > 5:
                print(f"  ... ja {len(customers) - 5} muuta")
    
    print("\n" + "=" * 60)


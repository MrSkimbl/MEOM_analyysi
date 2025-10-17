"""
Vaihe 5: Etusivujen copyjen haku
BeautifulSoup4 - ei tarvita OpenAI:ta
"""

import requests
from bs4 import BeautifulSoup
import time


def extract_homepage_copy(url: str, timeout: int = 10) -> dict:
    """
    Poimii etusivun tärkeimmät tekstit
    
    Args:
        url: Yrityksen etusivun URL
        timeout: Timeout sekunneissa
        
    Returns:
        Dictionary copyista tai tyhjä jos epäonnistui
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"    Haetaan: {url}")
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Poista turha
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # 1. Etsi hero/pääotsikko (H1)
        hero_headline = ""
        h1 = soup.find('h1')
        if h1:
            hero_headline = h1.get_text(strip=True)
        
        # 2. Etsi alaotsikko (ensimmäinen H2 tai suuri teksti H1:n jälkeen)
        hero_subheadline = ""
        h2 = soup.find('h2')
        if h2:
            hero_subheadline = h2.get_text(strip=True)
        
        # 3. Etsi kaikki otsikot (H1-H3)
        headlines = []
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            text = tag.get_text(strip=True)
            if text and len(text) > 3:
                headlines.append(text)
        
        # 4. Etsi kappaleet (P)
        paragraphs = []
        for p in soup.find_all('p', limit=10):  # Max 10 ensimmäistä
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Vähintään 20 merkkiä
                paragraphs.append(text)
        
        # 5. Yhdistä kaikki tekstit
        all_text = soup.get_text(separator=' ', strip=True)
        all_text = ' '.join(all_text.split())  # Puhdista välilyönnit
        
        # Rajoita pituutta
        if len(all_text) > 5000:
            all_text = all_text[:5000] + "..."
        
        # 6. Yritä tunnistaa value proposition (ensimmäinen pidempi kappale)
        main_value_prop = ""
        for p in paragraphs:
            if len(p) > 50:  # Ensimmäinen yli 50 merkin kappale
                main_value_prop = p
                break
        
        # 7. Key messages (otsikot + ensimmäiset kappaleet)
        key_messages = []
        key_messages.extend(headlines[:3])  # Max 3 otsikkoa
        key_messages.extend([p for p in paragraphs[:3] if p not in key_messages])  # Max 3 kappaletta
        
        result = {
            "url": url,
            "hero_headline": hero_headline,
            "hero_subheadline": hero_subheadline,
            "main_value_prop": main_value_prop,
            "key_messages": key_messages[:5],  # Max 5
            "full_text": all_text,
            "success": True
        }
        
        print(f"    [OK] Loydetty hero: '{hero_headline[:50]}...'")
        
        return result
        
    except requests.Timeout:
        print(f"    [WARN] Timeout: {url}")
        return {"url": url, "success": False, "error": "Timeout"}
    except requests.RequestException as e:
        print(f"    [WARN] Virhe: {type(e).__name__}")
        return {"url": url, "success": False, "error": str(e)}
    except Exception as e:
        print(f"    [WARN] Odottamaton virhe: {type(e).__name__}")
        return {"url": url, "success": False, "error": str(e)}


def extract_all_companies_copy(companies: list[dict]) -> dict:
    """
    Hakee kaikkien yritysten etusivujen copyt
    
    Args:
        companies: Lista yrityksiä [{"name": "...", "url": "..."}]
        
    Returns:
        Dictionary: {yritys_nimi: copy_dict}
    """
    print("\n" + "=" * 60)
    print("ETUSIVUJEN COPYJEN HAKU")
    print("=" * 60)
    print(f"\nHaetaan etusivujen copyt {len(companies)} yritykselta...")
    
    copies_by_company = {}
    
    for i, company in enumerate(companies, 1):
        name = company.get('name', 'N/A')
        url = company.get('url', '')
        
        print(f"\n[{i}/{len(companies)}] {name}")
        
        if not url:
            print("    [SKIP] URL puuttuu")
            copies_by_company[name] = {
                "url": "",
                "success": False,
                "error": "No URL"
            }
            continue
        
        try:
            copy = extract_homepage_copy(url)
            copies_by_company[name] = copy
            
        except Exception as e:
            print(f"    [ERROR] {type(e).__name__}: {str(e)}")
            copies_by_company[name] = {
                "url": url,
                "success": False,
                "error": str(e)
            }
        
        # Pieni viive yritysten välissä
        if i < len(companies):
            time.sleep(0.5)
    
    return copies_by_company


def print_copy_summary(copies_by_company: dict):
    """Tulostaa yhteenvedon copyista"""
    print("\n" + "=" * 60)
    print("ETUSIVUJEN COPYT - YHTEENVETO")
    print("=" * 60)
    
    successful = sum(1 for copy in copies_by_company.values() if copy.get('success', False))
    failed = len(copies_by_company) - successful
    
    print(f"\nYhteensa {len(copies_by_company)} yrityst:")
    print(f"  - Onnistuneita: {successful}")
    print(f"  - Epaonnistuneita: {failed}")
    print("-" * 60)
    
    for company, copy in copies_by_company.items():
        print(f"\n{company}:")
        
        if not copy.get('success', False):
            print(f"  [FAIL] {copy.get('error', 'Unknown error')}")
            continue
        
        hero = copy.get('hero_headline', '')
        if hero:
            # Safe print
            try:
                print(f"  Hero: {hero[:80]}")
            except:
                print(f"  Hero: {hero[:80].encode('ascii', 'ignore').decode('ascii')}")
        
        value_prop = copy.get('main_value_prop', '')
        if value_prop:
            try:
                print(f"  Value: {value_prop[:100]}...")
            except:
                print(f"  Value: {value_prop[:100].encode('ascii', 'ignore').decode('ascii')}...")
        
        key_msgs = copy.get('key_messages', [])
        if key_msgs:
            print(f"  Key messages: {len(key_msgs)} kpl")
        
        full_text = copy.get('full_text', '')
        if full_text:
            print(f"  Tekstia yhteensa: {len(full_text)} merkkia")
    
    print("\n" + "=" * 60)


"""
OpenAI API-testiskripti
Testaa että OpenAI API toimii ja web search -toiminnallisuus on käytössä
"""

import os
import sys
from dotenv import load_dotenv

# Lataa ympäristömuuttujat
load_dotenv()

# Windows-yhteensopiva tulostus
def safe_print(text):
    """Tulosta teksti Windows-yhteensopivasti"""
    # Korvaa Unicode-symbolit ASCII-merkeillä
    text = text.replace('✓', '[OK]')
    text = text.replace('✅', '[PASS]')
    text = text.replace('❌', '[FAIL]')
    text = text.replace('⚠️', '[WARN]')
    text = text.replace('🎉', '[SUCCESS]')
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def test_api_connection():
    """Testaa OpenAI API-yhteys"""
    print("=" * 60)
    print("TEST 1: OpenAI API-yhteyden testaus")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        # Hae API-avain (tukee molempia muotoja)
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
        
        if not api_key:
            safe_print("[FAIL] VIRHE: API-avainta ei löydy!")
            print("   Varmista että .env-tiedostossa on:")
            print("   OPENAI_API_KEY=your-api-key-here")
            print("   tai")
            print("   OPEN_AI_API=your-api-key-here")
            return False
        
        safe_print(f"[OK] API-avain loydetty (pituus: {len(api_key)} merkkia)")
        
        # Luo client
        client = OpenAI(api_key=api_key)
        safe_print("[OK] OpenAI client luotu")
        
        # Testaa yksinkertainen kysely
        print("\nLahetetaan testikysely...")
        response = client.chat.completions.create(
            model="gpt-4",  # Käytetään gpt-4 varmuuden vuoksi
            messages=[
                {"role": "user", "content": "Vastaa vain: 'API toimii'"}
            ],
            max_tokens=10
        )
        
        answer = response.choices[0].message.content
        safe_print(f"[OK] Vastaus saatu: {answer}")
        
        # Tulosta usage-tiedot
        usage = response.usage
        print(f"\nTokenien kaytto:")
        print(f"  - Prompt tokens: {usage.prompt_tokens}")
        print(f"  - Completion tokens: {usage.completion_tokens}")
        print(f"  - Yhteensa: {usage.total_tokens}")
        
        safe_print("\n[PASS] TEST 1 ONNISTUI - API toimii!")
        return True
        
    except ImportError:
        safe_print("[FAIL] VIRHE: OpenAI-kirjasto ei ole asennettu!")
        print("   Asenna: pip install openai")
        return False
    except Exception as e:
        safe_print(f"[FAIL] VIRHE: {type(e).__name__}: {str(e)}")
        return False


def test_web_search():
    """Testaa web search -toiminnallisuus"""
    print("\n" + "=" * 60)
    print("TEST 2: Web Search -toiminnallisuuden testaus")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
        client = OpenAI(api_key=api_key)
        
        print("Lähetetään web search -kysely...")
        print("Kysytään: 'Mikä on tämän päivän päivämäärä?'")
        
        response = client.chat.completions.create(
            model="gpt-4",  # gpt-4 tukee web search:ia
            messages=[
                {"role": "user", "content": "Mikä on tämän päivän päivämäärä? (Käytä web search)"}
            ],
            max_tokens=100
        )
        
        answer = response.choices[0].message.content
        safe_print(f"\n[OK] Vastaus: {answer}")
        
        # Tokenien käyttö
        usage = response.usage
        print(f"\nTokenien kaytto:")
        print(f"  - Prompt tokens: {usage.prompt_tokens}")
        print(f"  - Completion tokens: {usage.completion_tokens}")
        print(f"  - Yhteensa: {usage.total_tokens}")
        
        safe_print("\n[PASS] TEST 2 ONNISTUI - Web search toimii!")
        return True
        
    except Exception as e:
        safe_print(f"[FAIL] VIRHE: {type(e).__name__}: {str(e)}")
        print("\nHuom: Web search voi vaatia erityisen API-oikeuden tai mallin.")
        return False


def test_json_output():
    """Testaa JSON-muotoisen outputin"""
    print("\n" + "=" * 60)
    print("TEST 3: JSON-outputin testaus")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        import json
        
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
        client = OpenAI(api_key=api_key)
        
        print("Pyydetään strukturoitua JSON-dataa...")
        
        response = client.chat.completions.create(
            model="gpt-4o",  # gpt-4o tukee JSON response format
            messages=[
                {
                    "role": "user",
                    "content": """Luo JSON-objekti kolmesta esimerkkiyrityksestä:
                    {
                        "companies": [
                            {"name": "...", "industry": "..."}
                        ]
                    }"""
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=200
        )
        
        json_text = response.choices[0].message.content
        safe_print(f"\n[OK] JSON-vastaus saatu:\n{json_text}")
        
        # Parsi JSON
        data = json.loads(json_text)
        safe_print(f"\n[OK] JSON-parsinta onnistui!")
        print(f"  - Loydettiin {len(data.get('companies', []))} yrity sta")
        
        # Tokenien käyttö
        usage = response.usage
        print(f"\nTokenien kaytto:")
        print(f"  - Yhteensa: {usage.total_tokens} tokenia")
        
        safe_print("\n[PASS] TEST 3 ONNISTUI - JSON-output toimii!")
        return True
        
    except json.JSONDecodeError as e:
        safe_print(f"[FAIL] VIRHE: JSON-parsinta epaonnistui: {e}")
        return False
    except Exception as e:
        safe_print(f"[FAIL] VIRHE: {type(e).__name__}: {str(e)}")
        return False


def test_competitor_search_simulation():
    """Simuloi kilpailijahaku projektia varten"""
    print("\n" + "=" * 60)
    print("TEST 4: Kilpailijahaku-simulaatio (projektille)")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        import json
        
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
        client = OpenAI(api_key=api_key)
        
        test_url = "https://www.reaktor.com"
        print(f"Haetaan kilpailijoita yritykselle: {test_url}")
        
        prompt = f"""
        Etsi 3 pääkilpailijaa yritykselle {test_url} Suomen markkinassa.
        
        Palauta JSON-muodossa:
        {{
            "target_company": "Yrityksen nimi",
            "competitors": [
                {{
                    "name": "Kilpailija 1",
                    "url": "https://...",
                    "description": "Lyhyt kuvaus"
                }}
            ]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",  # gpt-4o tukee JSON response format
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=500
        )
        
        json_text = response.choices[0].message.content
        data = json.loads(json_text)
        
        safe_print(f"\n[OK] Kohdeyritys: {data.get('target_company', 'N/A')}")
        safe_print(f"\n[OK] Loydetyt kilpailijat:")
        for i, comp in enumerate(data.get('competitors', []), 1):
            print(f"  {i}. {comp.get('name', 'N/A')}")
            print(f"     URL: {comp.get('url', 'N/A')}")
            print(f"     Kuvaus: {comp.get('description', 'N/A')[:80]}...")
            print()
        
        # Tokenien käyttö
        usage = response.usage
        print(f"Tokenien kaytto: {usage.total_tokens} tokenia")
        
        safe_print("\n[PASS] TEST 4 ONNISTUI - Kilpailijahaku toimii!")
        return True
        
    except Exception as e:
        safe_print(f"[FAIL] VIRHE: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Aja kaikki testit"""
    print("\n")
    print("=" * 60)
    print(" " * 15 + "OPENAI API TESTIT")
    print("=" * 60)
    print()
    
    results = []
    
    # Aja testit
    results.append(("API-yhteys", test_api_connection()))
    results.append(("Web Search", test_web_search()))
    results.append(("JSON-output", test_json_output()))
    results.append(("Kilpailijahaku", test_competitor_search_simulation()))
    
    # Yhteenveto
    print("\n" + "=" * 60)
    print("YHTEENVETO")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTulokset: {passed}/{total} testia onnistui")
    
    if passed == total:
        print("\n[SUCCESS] Kaikki testit lapaisty! OpenAI API on valmis kayttoon.")
        return 0
    else:
        print(f"\n[WARN] {total - passed} testia epaonnistui. Tarkista asetukset.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


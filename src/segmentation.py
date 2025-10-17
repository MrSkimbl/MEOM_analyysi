"""
Vaihe 4: ICP (Ideal Customer Profile) -analyysi
Luo 4-6 ICP:tä asiakaslistoista
"""

import os
from openai import OpenAI
import json


def create_icps(customers_by_company: dict, api_key: str = None) -> dict:
    """
    Luo ICP:t (Ideal Customer Profiles) kaikista asiakkaista
    
    Args:
        customers_by_company: {yritys: [asiakkaat]}
        api_key: OpenAI API-avain
        
    Returns:
        ICP-data: {"icps": [...], "total_customers": N}
    """
    
    # Hae API-avain
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    
    if not api_key:
        raise ValueError("OpenAI API-avain puuttuu!")
    
    client = OpenAI(api_key=api_key)
    
    # Yhdistä kaikki asiakkaat
    all_customers = []
    for company, customers in customers_by_company.items():
        all_customers.extend(customers)
    
    # Poista duplikaatit
    unique_customers = list(set(all_customers))
    
    print(f"\nYhteensa {len(unique_customers)} uniikkia asiakasta")
    print("Luodaan ICP:t (Ideal Customer Profiles)...")
    
    # Rajoita 150 ensimmäiseen jos liikaa
    if len(unique_customers) > 150:
        print(f"  - Rajoitetaan {len(unique_customers)} -> 150 asiakasta analyysiin")
        unique_customers = unique_customers[:150]
    
    # Muotoile asiakkaslista
    customer_list = "\n".join([f"- {customer}" for customer in unique_customers])
    
    prompt = f"""Analysoi seuraavat B2B-asiakkaat ja luo 4-6 ICP:ta (Ideal Customer Profile).

ASIAKKAAT ({len(unique_customers)} kpl):
{customer_list}

TEHTAVA:
Luo 4-6 erillaista ICP:ta nain, etta:
1. Jokainen ICP edustaa selkeaa asiakastyyppia
2. ICP:t kattavat mahdollisimman monen asiakkaan
3. ICP:t ovat konkreettisia ja actionable

JOKAISELLE ICP:LLE MAARITA:

1. NIMI: Kuvaava nimi (esim. "Suuret finanssialan konsernit")

2. FIRMOGRAFIA:
   - company_size: Yrityksen koko (Small/Medium/Large/Enterprise)
   - industries: Paatoimialat (lista)
   - org_type: Organisaatiotyyppi (Private/Public/Government)
   - geography: Maantieteellinen kattavuus

3. TEKNOGRAFIA:
   - digital_maturity: Digitaalisen kypsyyden taso (Low/Medium/High)
   - tech_sophistication: Teknologinen edistykseellisyys
   - innovation_appetite: Innovaatiohakuisuus (Low/Medium/High)

4. TARPEET & HAASTEET:
   - challenges: Paahaasteet (lista 3-5)
   - typical_projects: Tyypilliset projektityypit (lista)
   - priorities: Prioriteetit (lista)

5. KAYTTAYTYMINEN:
   - decision_speed: Paatoksenteon nopeus (Fast/Medium/Slow)
   - budget_level: Budjettitaso (Low/Medium/High/Very High)
   - partnership_style: Kumppanuustyyli

6. ESIMERKIT:
   - example_customers: 3-8 esimerkkia YLLA OLEVASTA LISTASTA
   - estimated_size: Kuinka monta asiakasta kuuluu tahan ICP:hen (arvio)

7. MARKKINA-ARVO:
   - market_value: Segmentin arvo (Low/Medium/High/Very High)
   - reasoning: Lyhyt perustelu

PALAUTA JSON:
{{
    "icps": [
        {{
            "name": "ICP nimi",
            "firmographic": {{
                "company_size": "...",
                "industries": ["Industry 1", "Industry 2"],
                "org_type": "...",
                "geography": "..."
            }},
            "technographic": {{
                "digital_maturity": "...",
                "tech_sophistication": "...",
                "innovation_appetite": "..."
            }},
            "needs": {{
                "challenges": ["Haaste 1", "Haaste 2"],
                "typical_projects": ["Projekti 1", "Projekti 2"],
                "priorities": ["Prioriteetti 1", "Prioriteetti 2"]
            }},
            "behavioral": {{
                "decision_speed": "...",
                "budget_level": "...",
                "partnership_style": "..."
            }},
            "example_customers": ["Asiakas 1", "Asiakas 2"],
            "estimated_size": 10,
            "market_value": "...",
            "reasoning": "Miksi tama ICP on arvokas"
        }}
    ]
}}

TARKEA: Palauta VAIN JSON, ei muuta tekstia."""
    
    print("  - Analysoidaan asiakkaita GPT-5:lla...")
    
    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        # Parsi JSON
        result = json.loads(response.output_text)
        
        # Lisaa metatietoja
        result["total_customers"] = len(unique_customers)
        result["analyzed_customers"] = unique_customers
        
        print(f"  [OK] Luotiin {len(result.get('icps', []))} ICP:ta")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON-parsinta epaonnistui!")
        print(f"  Vastaus: {response.output_text[:500]}")
        raise
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {str(e)}")
        raise


def print_icp_summary(icp_data: dict):
    """
    Tulostaa ICP-yhteenvedon
    
    Args:
        icp_data: ICP-analyysin tulos
    """
    print("\n" + "=" * 60)
    print("ICP (IDEAL CUSTOMER PROFILE) - ANALYYSI")
    print("=" * 60)
    
    total = icp_data.get('total_customers', 0)
    icps = icp_data.get('icps', [])
    
    print(f"\nAnalysoitiin {total} asiakasta")
    print(f"Luotiin {len(icps)} ICP:ta")
    print("\n" + "=" * 60)
    
    for i, icp in enumerate(icps, 1):
        print(f"\nICP {i}: {icp.get('name', 'N/A')}")
        print("-" * 60)
        
        # Firmografia
        firmo = icp.get('firmographic', {})
        print(f"\nFIRMOGRAFIA:")
        print(f"  Yrityksen koko: {firmo.get('company_size', 'N/A')}")
        print(f"  Toimialat: {', '.join(firmo.get('industries', []))}")
        print(f"  Tyyppi: {firmo.get('org_type', 'N/A')}")
        print(f"  Maantiede: {firmo.get('geography', 'N/A')}")
        
        # Teknografia
        techno = icp.get('technographic', {})
        print(f"\nTEKNOGRAFIA:")
        print(f"  Digitaalinen kypsyys: {techno.get('digital_maturity', 'N/A')}")
        print(f"  Teknologinen taso: {techno.get('tech_sophistication', 'N/A')}")
        print(f"  Innovaatiohakuisuus: {techno.get('innovation_appetite', 'N/A')}")
        
        # Tarpeet
        needs = icp.get('needs', {})
        print(f"\nTARPEET & HAASTEET:")
        challenges = needs.get('challenges', [])
        if challenges:
            print(f"  Haasteet:")
            for challenge in challenges[:3]:
                print(f"    - {challenge}")
        
        # Kayttaytyminen
        behav = icp.get('behavioral', {})
        print(f"\nKAYTTAYTYMINEN:")
        print(f"  Paatoksenteko: {behav.get('decision_speed', 'N/A')}")
        print(f"  Budjetti: {behav.get('budget_level', 'N/A')}")
        print(f"  Kumppanuus: {behav.get('partnership_style', 'N/A')}")
        
        # Markkina-arvo
        print(f"\nMARKKINA-ARVO: {icp.get('market_value', 'N/A')}")
        reasoning = icp.get('reasoning', '')
        if reasoning:
            print(f"  {reasoning}")
        
        # Esimerkit
        examples = icp.get('example_customers', [])
        size = icp.get('estimated_size', 0)
        print(f"\nESIMERKKIASIAKKAAT ({size} kpl arvioitu):")
        for ex in examples[:6]:
            print(f"  - {ex}")
        if len(examples) > 6:
            print(f"  ... ja {len(examples) - 6} muuta")
    
    print("\n" + "=" * 60)


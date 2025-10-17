"""
Vaihe 6: Positioning-analyysi
Analysoi miten eri yritysten viestit resonoivat eri ICP:ille
"""

import os
from openai import OpenAI
import json


def analyze_positioning(
    companies: list[dict],
    icps: list[dict],
    copies_by_company: dict,
    api_key: str = None
) -> dict:
    """
    Analysoi positioning: Kenen viesti resonoi kenellekin ICP:lle
    
    Args:
        companies: Lista yrityksiä
        icps: Lista ICP:itä
        copies_by_company: {yritys: copy_data}
        api_key: OpenAI API-avain
        
    Returns:
        Positioning-analyysi per yritys per ICP
    """
    
    # Hae API-avain
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    
    if not api_key:
        raise ValueError("OpenAI API-avain puuttuu!")
    
    client = OpenAI(api_key=api_key)
    
    print("\n" + "=" * 60)
    print("POSITIONING-ANALYYSI")
    print("=" * 60)
    
    print(f"\nAnalysoidaan {len(companies)} yrityksen positioning")
    print(f"{len(icps)} ICP:lle...")
    
    # Muodosta yritysviestit
    companies_text = ""
    for company in companies:
        name = company.get('name')
        copy_data = copies_by_company.get(name, {})
        
        if copy_data.get('success'):
            hero = copy_data.get('hero_headline', '')
            value = copy_data.get('main_value_prop', '')
            full = copy_data.get('full_text', '')[:1000]  # Max 1000 merkkiä
            
            companies_text += f"\n\n=== {name} ===\n"
            companies_text += f"Hero: {hero}\n"
            companies_text += f"Value Proposition: {value}\n"
            companies_text += f"Etusivu: {full}\n"
        else:
            companies_text += f"\n\n=== {name} ===\n"
            companies_text += "Ei etusivudataa saatavilla\n"
    
    # Muodosta ICP-kuvaukset
    icps_text = ""
    for i, icp in enumerate(icps, 1):
        icps_text += f"\n{i}. {icp.get('name')}\n"
        
        firmo = icp.get('firmographic', {})
        icps_text += f"   - Koko: {firmo.get('company_size')}\n"
        icps_text += f"   - Toimialat: {', '.join(firmo.get('industries', []))}\n"
        
        needs = icp.get('needs', {})
        challenges = needs.get('challenges', [])
        if challenges:
            icps_text += f"   - Haasteet: {', '.join(challenges[:3])}\n"
    
    prompt = f"""Analysoi miten eri yritysten viestit (etusivujen copyt) resonoivat eri ICP:iden kanssa.

YRITYKSET JA HEIDÄN VIESTINSÄ:
{companies_text}

ICP:T (IDEAL CUSTOMER PROFILES):
{icps_text}

TEHTÄVÄ:
Arvioi JOKAISELLE yritykselle JOKAISEN ICP:n kohdalla:
1. SCORE (1-5): Kuinka hyvin yrityksen viesti resonoi tämän ICP:n kanssa?
   - 1 = Ei lainkaan relevantia
   - 2 = Vähän relevanttia
   - 3 = Kohtuullisen relevantia
   - 4 = Erittäin relevantia
   - 5 = Täydellinen match

2. REASONING: Miksi tämä pisteet? (2-3 lausetta)

3. STRENGTHS: Vahvuudet tämän ICP:n näkökulmasta

4. WEAKNESSES: Heikkoudet tämän ICP:n näkökulmasta

KRITEERIT PISTEILLE:
- Mainitaanko ICP:n toimialoja eksplisiittisesti?
- Puhutaanko ICP:n haasteista?
- Onko case-esimerkkejä tästä ICP:stä?
- Onko viesti linjassa ICP:n digitaalisen kypsyyden kanssa?
- Onko tarjonta relevanttia ICP:n tarpeille?

PALAUTA JSON:
{{
    "analysis": [
        {{
            "company": "Yritys A",
            "positioning_by_icp": [
                {{
                    "icp_name": "ICP 1 nimi",
                    "score": 4,
                    "reasoning": "Vahva fokus finanssialaan...",
                    "strengths": ["Vahvuus 1", "Vahvuus 2"],
                    "weaknesses": ["Heikkous 1"]
                }}
            ]
        }}
    ],
    "icp_leaders": {{
        "ICP 1 nimi": "Vahvin yritys tälle",
        "ICP 2 nimi": "Vahvin yritys tälle"
    }},
    "overall_insights": "2-3 lauseen yhteenveto löydöksistä"
}}

TÄRKEÄÄ: Palauta VAIN JSON, ei muuta."""
    
    print("  - Analysoidaan GPT-5:llä...")
    print("  - Tämä vie ~30-60 sekuntia...")
    
    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        # Parsi JSON
        result = json.loads(response.output_text)
        
        print("  [OK] Positioning-analyysi valmis!")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON-parsinta epaonnistui!")
        print(f"  Vastaus: {response.output_text[:500]}")
        raise
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {str(e)}")
        raise


def print_positioning_summary(positioning_data: dict, icps: list[dict]):
    """Tulostaa positioning-analyysin yhteenvedon"""
    print("\n" + "=" * 60)
    print("POSITIONING-ANALYYSI - TULOKSET")
    print("=" * 60)
    
    analysis = positioning_data.get('analysis', [])
    icp_leaders = positioning_data.get('icp_leaders', {})
    insights = positioning_data.get('overall_insights', '')
    
    # 1. ICP:n vahvimmat toimijat
    print("\nVAHVIMMATTOIMIJAT PER ICP:")
    print("-" * 60)
    for icp_name, leader in icp_leaders.items():
        print(f"\n{icp_name}:")
        print(f"  Vahvin: {leader}")
    
    # 2. Yrityskohtainen analyysi
    print("\n\nYRITYSKOHTAINEN ANALYYSI:")
    print("=" * 60)
    
    for company_analysis in analysis:
        company = company_analysis.get('company', 'N/A')
        print(f"\n{company}")
        print("-" * 60)
        
        for icp_pos in company_analysis.get('positioning_by_icp', []):
            icp_name = icp_pos.get('icp_name', 'N/A')
            score = icp_pos.get('score', 0)
            reasoning = icp_pos.get('reasoning', '')
            
            # Score visualisointi
            stars = "★" * score + "☆" * (5 - score)
            
            print(f"\n  {icp_name}: {score}/5 {stars}")
            print(f"    {reasoning}")
            
            strengths = icp_pos.get('strengths', [])
            if strengths:
                print(f"    Vahvuudet: {', '.join(strengths[:2])}")
    
    # 3. Yleiset oivallukset
    print("\n" + "=" * 60)
    print("KESKEISET OIVALLUKSET:")
    print("=" * 60)
    print(f"\n{insights}")
    
    print("\n" + "=" * 60)


def create_positioning_matrix(positioning_data: dict) -> dict:
    """
    Luo matriisi-muotoisen esityksen positioning-datasta
    
    Returns:
        {
            "matrix": [[score1, score2, ...], ...],
            "companies": ["Yritys 1", ...],
            "icps": ["ICP 1", ...]
        }
    """
    analysis = positioning_data.get('analysis', [])
    
    if not analysis:
        return {}
    
    # Kerää yritykset ja ICP:t
    companies = [comp.get('company') for comp in analysis]
    
    # Oletetaan että kaikilla on samat ICP:t
    first_company = analysis[0]
    icps = [icp.get('icp_name') for icp in first_company.get('positioning_by_icp', [])]
    
    # Luo matriisi
    matrix = []
    for company_analysis in analysis:
        row = []
        for icp_pos in company_analysis.get('positioning_by_icp', []):
            row.append(icp_pos.get('score', 0))
        matrix.append(row)
    
    return {
        "matrix": matrix,
        "companies": companies,
        "icps": icps
    }


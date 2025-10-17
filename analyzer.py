"""
Kilpailija-analyysi-työkalu
Analysoi yrityksen ja sen kilpailijoiden positioning eri asiakassegmenteissä
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# Lataa ympäristömuuttujat
load_dotenv()

# Importit omista moduuleista
from src.competitor_finder import (
    analyze_target_company, 
    find_competitors, 
    validate_competitor_data, 
    print_company_analysis,
    print_competitor_summary
)


def main():
    """Pääfunktio"""
    
    # Komentoriviparseri
    parser = argparse.ArgumentParser(
        description="Analysoi yrityksen ja kilpailijoiden positioning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esimerkit:
  python analyzer.py --url https://reaktor.com
  python analyzer.py --url https://meom.fi --competitors 3 --output meom-analyysi.html
        """
    )
    
    parser.add_argument(
        "--url",
        required=True,
        help="Analysoitavan yrityksen URL"
    )
    
    parser.add_argument(
        "--competitors",
        type=int,
        default=5,
        help="Kilpailijoiden määrä (oletus: 5)"
    )
    
    parser.add_argument(
        "--output",
        default="report.html",
        help="HTML-raportin tiedostonimi (oletus: report.html)"
    )
    
    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="Aja vain tietty vaihe (testaus)"
    )
    
    args = parser.parse_args()
    
    # Tulosta otsikko
    print("\n" + "=" * 60)
    print(" " * 15 + "KILPAILIJA-ANALYYSI")
    print("=" * 60)
    print(f"\nKohdeyritys: {args.url}")
    print(f"Kilpailijoita haetaan: {args.competitors}")
    print(f"Raportti tallennettaan: {args.output}")
    print("\n" + "=" * 60)
    
    # Tarkista API-avain
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
    if not api_key:
        print("\nVIRHE: OpenAI API-avain puuttuu!")
        print("Lisää .env-tiedostoon: OPENAI_API_KEY=your-api-key")
        return 1
    
    print(f"\n[OK] API-avain löydetty (pituus: {len(api_key)} merkkiä)")
    
    try:
        # VAIHE 1A: Yritysanalyysi
        print("\n" + "=" * 60)
        print("VAIHE 1A/7: Kohdeyrityksen analyysi")
        print("=" * 60 + "\n")
        
        company_analysis = analyze_target_company(
            target_url=args.url,
            api_key=api_key
        )
        
        # Tulosta yritysanalyysi
        print_company_analysis(company_analysis)
        
        # VAIHE 1B: Kilpailijoiden haku
        print("\n" + "=" * 60)
        print("VAIHE 1B/7: Kilpailijoiden haku")
        print("=" * 60 + "\n")
        
        competitor_data = find_competitors(
            target_url=args.url,
            count=args.competitors,
            api_key=api_key,
            company_analysis=company_analysis
        )
        
        # Validoi data
        if not validate_competitor_data(competitor_data):
            print("\nVIRHE: Kilpailijoiden data on virheellinen!")
            return 1
        
        # Tulosta yhteenveto
        print_competitor_summary(competitor_data)
        
        # Jos testataan vain vaihetta 1, lopeta tähän
        if args.step == 1:
            print("\n[TESTI] Vaihe 1 (1A + 1B) suoritettu. Lopetetaan.")
            return 0
        
        # TODO: Vaihe 2: URL-validointi
        print("\n[INFO] Vaihe 2: URL-validointi (tulossa...)")
        
        # TODO: Vaihe 3: Asiakasreferenssien haku
        print("[INFO] Vaihe 3: Asiakasreferenssien haku (tulossa...)")
        
        # TODO: Vaihe 4: Asiakassegmentointi
        print("[INFO] Vaihe 4: Asiakassegmentointi (tulossa...)")
        
        # TODO: Vaihe 5: Etusivujen copyt
        print("[INFO] Vaihe 5: Etusivujen copyt (tulossa...)")
        
        # TODO: Vaihe 6: Positioning-analyysi
        print("[INFO] Vaihe 6: Positioning-analyysi (tulossa...)")
        
        # TODO: Vaihe 7: HTML-raportti
        print("[INFO] Vaihe 7: HTML-raportti (tulossa...)")
        
        print("\n" + "=" * 60)
        print("ANALYYSI VALMIS (osittain - kehityksessä)")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Analyysi keskeytetty käyttäjän toimesta.")
        return 130
    except Exception as e:
        print(f"\n[VIRHE] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


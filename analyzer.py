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
from src.customer_extractor import (
    extract_all_companies_customers,
    print_customer_summary
)
from src.segmentation import (
    create_icps,
    print_icp_summary
)
from src.copy_extractor import (
    extract_all_companies_copy,
    print_copy_summary
)
from src.positioning import (
    analyze_positioning,
    print_positioning_summary,
    create_positioning_matrix
)
from src.report_generator import (
    generate_html_report,
    print_report_summary
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
        choices=[1, 3, 4, 5, 6, 7],
        help="Aja vain tietty vaihe (testaus): 1=kilpailijat, 3=asiakkaat, 4=ICP, 5=copyt, jne."
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
        
        # VAIHE 3: Asiakasreferenssien haku
        print("\n" + "=" * 60)
        print("VAIHE 3/7: Asiakasreferenssien haku")
        print("=" * 60 + "\n")
        
        # Yhdistä kohdeyritys ja kilpailijat
        all_companies = [
            {
                "name": competitor_data.get('target_company'),
                "url": competitor_data.get('target_url')
            }
        ]
        all_companies.extend([
            {
                "name": comp.get('name'),
                "url": comp.get('url')
            }
            for comp in competitor_data.get('competitors', [])
        ])
        
        # Hae asiakkaat kaikilta
        customers_by_company = extract_all_companies_customers(
            companies=all_companies,
            api_key=api_key
        )
        
        # Tulosta yhteenveto
        print_customer_summary(customers_by_company)
        
        # Jos testataan vain vaiheeseen 3, lopeta tähän
        if args.step == 3:
            print("\n[TESTI] Vaihe 3 suoritettu. Lopetetaan.")
            return 0
        
        # VAIHE 4: ICP-analyysi
        print("\n" + "=" * 60)
        print("VAIHE 4/7: ICP (Ideal Customer Profile) -analyysi")
        print("=" * 60 + "\n")
        
        icp_data = create_icps(
            customers_by_company=customers_by_company,
            api_key=api_key
        )
        
        # Tulosta yhteenveto
        print_icp_summary(icp_data)
        
        # Jos testataan vain vaiheeseen 4, lopeta tähän
        if args.step == 4:
            print("\n[TESTI] Vaihe 4 suoritettu. Lopetetaan.")
            return 0
        
        # VAIHE 5: Etusivujen copyjen haku
        print("\n" + "=" * 60)
        print("VAIHE 5/7: Etusivujen copyjen haku")
        print("=" * 60 + "\n")
        
        # Käytä samaa all_companies -listaa kuin vaiheessa 3
        copies_by_company = extract_all_companies_copy(
            companies=all_companies
        )
        
        # Tulosta yhteenveto
        print_copy_summary(copies_by_company)
        
        # Jos testataan vain vaiheeseen 5, lopeta tähän
        if args.step == 5:
            print("\n[TESTI] Vaihe 5 suoritettu. Lopetetaan.")
            return 0
        
        # VAIHE 6: Positioning-analyysi
        print("\n" + "=" * 60)
        print("VAIHE 6/7: Positioning-analyysi")
        print("=" * 60 + "\n")
        
        positioning_data = analyze_positioning(
            companies=all_companies,
            icps=icp_data.get('icps', []),
            copies_by_company=copies_by_company,
            api_key=api_key
        )
        
        # Tulosta yhteenveto
        print_positioning_summary(
            positioning_data=positioning_data,
            icps=icp_data.get('icps', [])
        )
        
        # Luo matriisi (käytetään HTML-raportissa)
        matrix = create_positioning_matrix(positioning_data)
        
        # Jos testataan vain vaiheeseen 6, lopeta tähän
        if args.step == 6:
            print("\n[TESTI] Vaihe 6 suoritettu. Lopetetaan.")
            return 0
        
        # VAIHE 7: HTML-raportti
        print("\n" + "=" * 60)
        print("VAIHE 7/7: HTML-raportin generointi")
        print("=" * 60 + "\n")
        
        output_file = generate_html_report(
            company_analysis=company_analysis,
            competitor_data=competitor_data,
            customers_by_company=customers_by_company,
            icp_data=icp_data,
            copies_by_company=copies_by_company,
            positioning_data=positioning_data,
            output_file=args.output
        )
        
        # Tulosta yhteenveto
        print_report_summary(output_file)
        
        print("\n" + "=" * 60)
        print("ANALYYSI VALMIS!")
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


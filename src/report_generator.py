"""
Vaihe 7: HTML-raportin generointi
Käyttää MEOM:n style guidea
"""

from datetime import datetime


def generate_html_report(
    company_analysis: dict,
    competitor_data: dict,
    customers_by_company: dict,
    icp_data: dict,
    copies_by_company: dict,
    positioning_data: dict,
    output_file: str = "report.html"
) -> str:
    """
    Generoi HTML-raportti kaikesta datasta
    
    Args:
        company_analysis: Kohdeyrityksen analyysi
        competitor_data: Kilpailijat
        customers_by_company: Asiakkaat
        icp_data: ICP-analyysi
        copies_by_company: Etusivujen copyt
        positioning_data: Positioning-analyysi
        output_file: Tiedostonimi
        
    Returns:
        Polku luotuun tiedostoon
    """
    
    # Luo HTML
    html = create_html_structure(
        company_analysis=company_analysis,
        competitor_data=competitor_data,
        customers_by_company=customers_by_company,
        icp_data=icp_data,
        copies_by_company=copies_by_company,
        positioning_data=positioning_data
    )
    
    # Kirjoita tiedostoon
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] HTML-raportti luotu: {output_file}")
    
    return output_file


def create_html_structure(
    company_analysis,
    competitor_data,
    customers_by_company,
    icp_data,
    copies_by_company,
    positioning_data
) -> str:
    """Luo HTML-dokumentti"""
    
    target_company = competitor_data.get('target_company', 'Yritys')
    competitors = competitor_data.get('competitors', [])
    icps = icp_data.get('icps', [])
    analysis = positioning_data.get('analysis', [])
    icp_leaders = positioning_data.get('icp_leaders', {})
    insights = positioning_data.get('overall_insights', '')
    
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    html = f"""<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kilpailija-analyysi: {target_company}</title>
    <style>
{get_meom_styles()}
    </style>
</head>
<body>

<header class="site-header">
    <div class="container nav">
        <div class="logo">MEOM Analyysi</div>
        <div style="font-size: 0.9rem; color: var(--muted-ink);">{now}</div>
    </div>
</header>

<section class="hero">
    <div class="container">
        <h1>Kilpailija-analyysi</h1>
        <p class="lead">Positioning-analyysi: {target_company} ja {len(competitors)} kilpailijaa Suomen markkinassa</p>
    </div>
</section>

<!-- EXECUTIVE SUMMARY -->
<section class="section">
    <div class="container">
        <h2>Keskeiset oivallukset</h2>
        <div class="card">
            <p>{insights}</p>
        </div>
    </div>
</section>

<!-- ICP LEADERS -->
<section class="section section--tight">
    <div class="container">
        <h2>Vahvimmat toimijat per ICP</h2>
        <div class="grid grid--2">
{generate_icp_leaders_cards(icp_leaders)}
        </div>
    </div>
</section>

<!-- POSITIONING MATRIX -->
<section class="section" style="background:#f9fafb; padding: var(--s6) 0;">
    <div class="container">
        <h2>Positioning-matriisi</h2>
        <p class="lead">Pisteet 1-5: Kuinka hyvin kunkin yrityksen viesti resonoi eri ICP:iden kanssa</p>
        <div style="overflow-x: auto; margin-top: var(--s4);">
{generate_positioning_matrix_table(analysis, icps)}
        </div>
    </div>
</section>

<!-- YRITYSKOHTAINEN ANALYYSI -->
<section class="section">
    <div class="container">
        <h2>Yrityskohtainen analyysi</h2>
{generate_company_analyses(analysis, customers_by_company)}
    </div>
</section>

<!-- ICP PROFIILIT -->
<section class="section section--tight" style="background:#f9fafb; padding: var(--s6) 0;">
    <div class="container">
        <h2>ICP-profiilit</h2>
        <p class="lead">{len(icps)} tunnistettua Ideal Customer Profile -profiilia</p>
        <div class="grid grid--2" style="margin-top: var(--s4);">
{generate_icp_cards(icps)}
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer class="site-footer">
    <div class="container">
        <p style="text-align: center; color: var(--muted-ink);">
            Analyysi luotu {now} | MEOM Competitor Analysis Tool
        </p>
    </div>
</footer>

</body>
</html>"""
    
    return html


def get_meom_styles() -> str:
    """MEOM:n tyylit"""
    return """
:root {
  --ink: #221f1f;
  --bg: #ffffff;
  --muted-ink: #4a4a4a;
  --divider: #e9e9eb;
  --accent: #00C389;
  --accent-ink: #ffffff;
  --font-sans: ui-sans-serif, system-ui, -apple-system, "Inter", "Helvetica Neue", Arial, sans-serif;
  --h1: clamp(2.2rem, 3.2vw, 3.5rem);
  --h2: clamp(1.6rem, 2.4vw, 2.25rem);
  --h3: clamp(1.25rem, 1.6vw, 1.5rem);
  --body: 1rem;
  --lead: 1.125rem;
  --lh-tight: 1.15;
  --lh-normal: 1.6;
  --s0: 8px; --s1: 12px; --s2: 16px; --s3: 24px;
  --s4: 32px; --s5: 48px; --s6: 64px; --s7: 96px;
  --radius: 14px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
  --shadow-md: 0 6px 16px rgba(0,0,0,.08);
}

html, body { margin:0; padding:0; background:var(--bg); color:var(--ink); font-family:var(--font-sans); font-size:16px; }
.container { width:100%; max-width:1280px; margin:0 auto; padding-left:24px; padding-right:24px; }
h1 { font-size:var(--h1); line-height:var(--lh-tight); font-weight:700; margin:0 0 var(--s3); }
h2 { font-size:var(--h2); line-height:1.2; font-weight:700; margin:0 0 var(--s2); }
h3 { font-size:var(--h3); line-height:1.25; font-weight:600; margin:0 0 var(--s2); }
p { font-size:var(--body); line-height:var(--lh-normal); color:var(--muted-ink); margin:0 0 var(--s2); }
.lead { font-size:var(--lead); line-height:var(--lh-normal); max-width:68ch; color:var(--ink); }
hr { border:0; height:1px; background:var(--divider); margin:var(--s4) 0; }

.site-header { position:sticky; top:0; z-index:50; background:rgba(255,255,255,.92); backdrop-filter:blur(8px); border-bottom:1px solid var(--divider); }
.nav { height:68px; display:flex; align-items:center; justify-content:space-between; }
.logo { font-weight:700; letter-spacing:.2px; }

.card { background:#fff; border:1px solid var(--divider); border-radius:var(--radius); box-shadow:var(--shadow-sm); padding:var(--s4); }
.card h3 { margin-bottom:var(--s2); }
.card__meta { font-size:.9rem; color:var(--muted-ink); margin-bottom: var(--s2); }

.section { padding:var(--s6) 0; }
.section--tight { padding:var(--s4) 0; }
.hero { padding:var(--s7) 0 var(--s6); }

.grid { display:grid; gap:var(--s3); }
@media (min-width:768px) { 
  .grid--2 { grid-template-columns:repeat(2,1fr); } 
  .grid--3 { grid-template-columns:repeat(3,1fr); }
}

.badge { display:inline-block; padding:6px 12px; font-size:.85rem; border-radius:999px; background:var(--divider); color:var(--ink); margin-right:8px; margin-bottom:8px; }
.badge--accent { background:var(--accent); color:var(--accent-ink); }

.table { width:100%; border-collapse:separate; border-spacing:0; margin:var(--s3) 0; }
.table th, .table td { padding:12px 14px; border-bottom:1px solid var(--divider); text-align:left; }
.table th { font-weight:600; color:var(--ink); background:#f9fafb; }
.table td { color:var(--ink); }

.score { display:inline-block; padding:4px 10px; border-radius:6px; font-weight:600; font-size:0.9rem; }
.score--5 { background:#00C389; color:#fff; }
.score--4 { background:#4ade80; color:#fff; }
.score--3 { background:#fbbf24; color:#000; }
.score--2 { background:#fb923c; color:#fff; }
.score--1 { background:#ef4444; color:#fff; }

.site-footer { margin-top:var(--s7); padding:var(--s5) 0; border-top:1px solid var(--divider); background:#f9fafb; }

ul.list { list-style: none; padding:0; margin:0; }
ul.list li { padding:4px 0; color:var(--muted-ink); }
ul.list li:before { content:"•"; color:var(--accent); margin-right:8px; }
"""


def generate_icp_leaders_cards(icp_leaders: dict) -> str:
    """Generoi kortit ICP-johtajista"""
    cards = ""
    for icp_name, leader in icp_leaders.items():
        cards += f"""
            <div class="card">
                <div class="card__meta">ICP</div>
                <h3>{icp_name}</h3>
                <p><strong style="color:var(--accent);">Vahvin: {leader}</strong></p>
            </div>"""
    return cards


def generate_positioning_matrix_table(analysis: list, icps: list) -> str:
    """Generoi positioning-matriisi taulukkona"""
    if not analysis or not icps:
        return "<p>Ei dataa saatavilla</p>"
    
    # Taulukon header
    table = '<table class="table">\n<thead><tr><th>Yritys</th>'
    
    for icp in icps:
        icp_name = icp.get('name', 'N/A')
        table += f'<th>{icp_name}</th>'
    
    table += '</tr></thead>\n<tbody>'
    
    # Rivit per yritys
    for company_analysis in analysis:
        company = company_analysis.get('company', 'N/A')
        table += f'<tr><td><strong>{company}</strong></td>'
        
        for icp_pos in company_analysis.get('positioning_by_icp', []):
            score = icp_pos.get('score', 0)
            table += f'<td><span class="score score--{score}">{score}/5</span></td>'
        
        table += '</tr>'
    
    table += '</tbody></table>'
    
    return table


def generate_company_analyses(analysis: list, customers_by_company: dict) -> str:
    """Generoi yrityskohtaiset analyysit"""
    html = ""
    
    for company_analysis in analysis:
        company = company_analysis.get('company', 'N/A')
        customers = customers_by_company.get(company, [])
        
        html += f"""
        <div class="card" style="margin-bottom:var(--s4);">
            <h3>{company}</h3>
            <div class="card__meta">{len(customers)} asiakasta tunnistettu</div>
            
            <h4 style="margin-top:var(--s3); margin-bottom:var(--s2); font-size:1rem;">Positioning per ICP:</h4>
"""
        
        for icp_pos in company_analysis.get('positioning_by_icp', []):
            icp_name = icp_pos.get('icp_name', 'N/A')
            score = icp_pos.get('score', 0)
            reasoning = icp_pos.get('reasoning', '')
            strengths = icp_pos.get('strengths', [])
            weaknesses = icp_pos.get('weaknesses', [])
            
            html += f"""
            <div style="margin-bottom:var(--s3); padding-bottom:var(--s3); border-bottom:1px solid var(--divider);">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:var(--s2);">
                    <strong>{icp_name}</strong>
                    <span class="score score--{score}">{score}/5</span>
                </div>
                <p style="margin-bottom:var(--s2);">{reasoning}</p>
                
                {f'<div><strong style="font-size:0.9rem;">Vahvuudet:</strong> ' + ', '.join(strengths[:3]) + '</div>' if strengths else ''}
                {f'<div style="margin-top:4px;"><strong style="font-size:0.9rem;">Heikkoudet:</strong> ' + ', '.join(weaknesses[:2]) + '</div>' if weaknesses else ''}
            </div>
"""
        
        html += """
        </div>
"""
    
    return html


def generate_icp_cards(icps: list) -> str:
    """Generoi ICP-kortit"""
    html = ""
    
    for icp in icps:
        name = icp.get('name', 'N/A')
        firmo = icp.get('firmographic', {})
        needs = icp.get('needs', {})
        examples = icp.get('example_customers', [])
        market_value = icp.get('market_value', 'N/A')
        
        html += f"""
            <div class="card">
                <h3>{name}</h3>
                <div class="card__meta">Markkina-arvo: {market_value}</div>
                
                <p><strong>Koko:</strong> {firmo.get('company_size', 'N/A')}</p>
                <p><strong>Toimialat:</strong> {', '.join(firmo.get('industries', [])[:3])}</p>
                
                <div style="margin-top:var(--s2);">
                    <strong style="font-size:0.9rem;">Haasteet:</strong>
                    <ul class="list" style="margin-top:8px;">
                        {''.join([f'<li>{ch}</li>' for ch in needs.get('challenges', [])[:3]])}
                    </ul>
                </div>
                
                {f'<div style="margin-top:var(--s2);"><strong style="font-size:0.9rem;">Esimerkit:</strong><br/>' + ', '.join(examples[:5]) + '</div>' if examples else ''}
            </div>
"""
    
    return html


def print_report_summary(output_file: str):
    """Tulostaa yhteenveto raportista"""
    print("\n" + "=" * 60)
    print("HTML-RAPORTTI LUOTU")
    print("=" * 60)
    print(f"\nTiedosto: {output_file}")
    print("\nAvaa selaimessa:")
    print(f"  file:///{os.path.abspath(output_file)}")
    print("\nTai kaksoisklikkaa tiedostoa Explorerissa")
    print("\n" + "=" * 60)


import os


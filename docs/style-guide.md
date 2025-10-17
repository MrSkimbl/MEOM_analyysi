You are a senior frontend engineer. Implement UI that matches MEOM.fi’s style based on the following SPEC. Do not invent new tokens. Reuse components. Keep code minimal and production-ready.

# DESIGN TOKENS
:root {
  /* Colors */
  --ink: #221f1f;            /* primary text (near-black) */
  --bg: #ffffff;             /* page background */
  --muted-ink: #4a4a4a;      /* secondary text */
  --divider: #e9e9eb;        /* borders/dividers */
  --accent: #00C389;         /* PRIMARY ACCENT (confirm against live brand if needed) */
  --accent-ink: #ffffff;     /* text on accent */

  /* Typography */
  --font-sans: ui-sans-serif, system-ui, -apple-system, "Inter", "Helvetica Neue", Arial, "Noto Sans", sans-serif;
  --h1: clamp(2.2rem, 3.2vw, 3.5rem);
  --h2: clamp(1.6rem, 2.4vw, 2.25rem);
  --h3: clamp(1.25rem, 1.6vw, 1.5rem);
  --body: 1rem;
  --lead: 1.125rem;
  --lh-tight: 1.15;
  --lh-normal: 1.6;

  /* Spacing (8pt scale) */
  --s-1: 4px; --s0: 8px; --s1: 12px; --s2: 16px; --s3: 24px;
  --s4: 32px; --s5: 48px; --s6: 64px; --s7: 96px;

  /* Radius & Shadows */
  --radius: 14px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
  --shadow-md: 0 6px 16px rgba(0,0,0,.08);
}

# GLOBAL CSS (inject into globals.css)
html,body { margin:0; padding:0; background:var(--bg); color:var(--ink); font-family:var(--font-sans); font-size:16px; }
.container { width:100%; max-width:1280px; margin:0 auto; padding-left:24px; padding-right:24px; }
h1{ font-size:var(--h1); line-height:var(--lh-tight); font-weight:700; margin:0 0 var(--s3); }
h2{ font-size:var(--h2); line-height:1.2; font-weight:700; margin:0 0 var(--s2); }
h3{ font-size:var(--h3); line-height:1.25; font-weight:600; margin:0 0 var(--s2); }
p{ font-size:var(--body); line-height:var(--lh-normal); color:var(--muted-ink); margin:0 0 var(--s2); }
.lead{ font-size:var(--lead); line-height:var(--lh-normal); max-width:68ch; color:var(--ink); }
img{ max-width:100%; height:auto; border-radius:8px; display:block; }
hr{ border:0; height:1px; background:var(--divider); margin:var(--s4) 0; }

a{ color:inherit; text-decoration:underline; text-underline-offset:3px; }
a.button{ text-decoration:none; }

.grid{ display:grid; gap:var(--s3); }
@media (min-width:768px){ .grid--2{ grid-template-columns:repeat(2,1fr); } .grid--3{ grid-template-columns:repeat(3,1fr);} .grid--4{ grid-template-columns:repeat(4,1fr);} }

.hidden-visually{ position:absolute !important; height:1px; width:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }

# HEADER / NAV
.site-header{ position:sticky; top:0; z-index:50; background:rgba(255,255,255,.92); backdrop-filter:saturate(180%) blur(8px); border-bottom:1px solid var(--divider); }
.nav{ height:68px; display:flex; align-items:center; justify-content:space-between; }
.logo{ display:inline-flex; align-items:center; gap:10px; font-weight:700; letter-spacing:.2px; text-decoration:none; }

# BUTTONS
.button{ display:inline-flex; align-items:center; gap:10px; padding:12px 18px; border-radius:var(--radius); font-weight:600; transition:transform .05s ease, box-shadow .2s ease, background .2s ease, color .2s ease; }
.button--primary{ background:var(--accent); color:var(--accent-ink); box-shadow:var(--shadow-sm); border:1px solid rgba(0,0,0,0); }
.button--primary:hover{ transform:translateY(-1px); box-shadow:var(--shadow-md); }
.button--ghost{ background:transparent; color:var(--ink); border:1px solid var(--divider); }
.button--link{ background:transparent; padding:0; border:0; color:var(--ink); text-decoration:underline; text-underline-offset:3px; }

# CARDS
.card{ background:#fff; border:1px solid var(--divider); border-radius:var(--radius); box-shadow:var(--shadow-sm); padding:var(--s4); }
.card h3{ margin-bottom:var(--s2); }
.card__meta{ font-size:.9rem; color:var(--muted-ink); }

# SECTIONS
.section{ padding:var(--s6) 0; }
.section--tight{ padding:var(--s4) 0; }
.hero{ padding:var(--s7) 0 var(--s6); }
.hero__actions{ display:flex; gap:var(--s2); flex-wrap:wrap; margin-top:var(--s3); }

# LISTS
.list{ display:grid; gap:var(--s2); padding:0; margin:0; list-style:none; }
.list--bullets li{ position:relative; padding-left:20px; }
.list--bullets li::before{ content:"•"; position:absolute; left:0; top:0; color:var(--accent); }

# BADGES / TAGS
.badge{ display:inline-flex; align-items:center; gap:8px; padding:6px 10px; font-size:.9rem; border-radius:999px; border:1px solid var(--divider); background:#fff; }

# TABLE (simple)
.table{ width:100%; border-collapse:separate; border-spacing:0; }
.table th, .table td{ padding:12px 14px; border-bottom:1px solid var(--divider); text-align:left; }
.table th{ font-weight:600; color:var(--ink); }

# FOOTER
.site-footer{ margin-top:var(--s7); padding:var(--s6) 0 var(--s5); border-top:1px solid var(--divider); background:#fff; }
.footer-grid{ display:grid; gap:var(--s3); }
@media(min-width:768px){ .footer-grid{ grid-template-columns:2fr 1fr 1fr 1fr; } }

# ACCESSIBILITY
/* Always provide accessible names, focus styles, and sufficient contrast */
:focus-visible{ outline:2px solid var(--accent); outline-offset:3px; }
button, [role="button"], a.button{ cursor:pointer; }

# TAILWIND (optional). If using Tailwind, extend using these values:
# tailwind.config.js
# module.exports = {
#   content: ["./src/**/*.{ts,tsx,js,jsx,html}"],
#   theme: {
#     container: { center: true, padding: "1.5rem" },
#     extend: {
#       colors: { ink: "#221f1f", accent: "#00C389", divider: "#e9e9eb" },
#       borderRadius: { xl: "14px" },
#       boxShadow: { sm:"0 1px 2px rgba(0,0,0,.06)", md:"0 6px 16px rgba(0,0,0,.08)" },
#       fontFamily: { sans: ["Inter","ui-sans-serif","system-ui","-apple-system","Helvetica Neue","Arial","Noto Sans","sans-serif"] },
#       fontSize: {
#         h1: ["clamp(2.2rem,3.2vw,3.5rem)", { lineHeight:"1.15", fontWeight:"700" }],
#         h2: ["clamp(1.6rem,2.4vw,2.25rem)", { lineHeight:"1.2", fontWeight:"700" }],
#         h3: ["clamp(1.25rem,1.6vw,1.5rem)", { lineHeight:"1.25", fontWeight:"600" }],
#       },
#       spacing: { "1.5":"0.375rem","4.5":"1.125rem","7.5":"1.875rem" }
#     }
#   }
# }

# COMPONENT BLUEPRINTS (HTML skeletons the model should fill with content/data)

## Header
<header class="site-header">
  <div class="container nav">
    <a href="/" class="logo">MEOM</a>
    <nav aria-label="Primary">
      <a href="/palvelut" class="button button--link">Palvelut</a>
      <a href="/referenssit" class="button button--link">Referenssit</a>
      <a href="/ota-yhteytta" class="button button--primary">Ota yhteyttä</a>
    </nav>
  </div>
</header>

## Hero
<section class="hero">
  <div class="container">
    <h1>Selkeä B2B-verkkosivusto, joka tuottaa mitattavaa arvoa</h1>
    <p class="lead">Ytimekäs kuvaus. Max 2 lausetta. ~68 merkkiä/ rivi.</p>
    <div class="hero__actions">
      <a class="button button--primary" href="#cta">Pyydä arvio</a>
      <a class="button button--ghost" href="#learn">Tutustu palveluun</a>
    </div>
  </div>
</section>

## Feature grid (3 cols desktop)
<section class="section">
  <div class="container grid grid--3">
    <article class="card">
      <h3>Selkeä rakenne</h3>
      <p>Ytimekäs hyötylause. 1–2 virkettä.</p>
    </article>
    <article class="card">
      <h3>Nopea toteutus</h3>
      <p>Lyhyt kuvaus. Ei markkinahöttöä.</p>
    </article>
    <article class="card">
      <h3>Mitattavat tulokset</h3>
      <p>Konversiot, NPS, orgaaninen kasvu.</p>
    </article>
  </div>
</section>

## Case grid
<section class="section section--tight">
  <div class="container grid grid--3">
    <a class="card" href="/case/example">
      <img src="/img/case.jpg" alt="Case-nosto" />
      <h3>Case: Yritys X</h3>
      <p class="card__meta">B2B / Verkkosivusto / 2025</p>
      <p>1–2 virkkeen tulos/vaikutus.</p>
    </a>
    <!-- toista kortteja -->
  </div>
</section>

## CTA band
<section class="section" style="background:#f9fafb; border-top:1px solid var(--divider); border-bottom:1px solid var(--divider); ">
  <div class="container" style="display:flex; gap:var(--s3); align-items:center; justify-content:space-between; flex-wrap:wrap;">
    <div>
      <h2>Valmis nostamaan sivustosi tasoa?</h2>
      <p class="lead">Pysyvä parannus konversioon ja sisältöön.</p>
    </div>
    <a class="button button--primary" href="/ota-yhteytta">Varaa keskustelu</a>
  </div>
</section>

## Footer
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <strong>MEOM</strong>
      <p class="card__meta">B2B-verkkosivut ja jatkuva kehitys.</p>
    </div>
    <div>
      <h3>Palvelut</h3>
      <ul class="list">
        <li><a href="/verkkosivut">Verkkosivut</a></li>
        <li><a href="/jatkokehitys">Jatkokehitys</a></li>
      </ul>
    </div>
    <div>
      <h3>Yritys</h3>
      <ul class="list">
        <li><a href="/referenssit">Referenssit</a></li>
        <li><a href="/yhteystiedot">Yhteystiedot</a></li>
      </ul>
    </div>
    <div>
      <h3>Ota yhteyttä</h3>
      <a class="button button--ghost" href="/ota-yhteytta">Lähetä viesti</a>
    </div>
  </div>
</footer>

# IMPLEMENTATION RULES
- Use semantic HTML. Keep headings ≤ 12 words. No excessive text.
- Max content width: 1280px; mobile padding 24px; desktop 24–32px.
- Grid gaps use --s3. Section paddings use --s6 (tight: --s4).
- Buttons only the three variants defined. No custom ad-hoc styles.
- Images: rounded corners 8–16px; subtle shadows only via tokens.
- Keep contrast AA+. Accent on white or on ink with sufficient contrast.
- Do not introduce additional colors, radii, or shadows.
- Keep bundle light; no external UI kits unless explicitly allowed.
- If using React, export default components; props for title, lead, items.
- If using Tailwind, mirror tokens via theme.extend (see snippet).

# OUTPUT
Return complete, ready-to-run code (HTML/CSS or React + CSS) that strictly follows the above tokens and components.

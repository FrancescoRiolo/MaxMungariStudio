# Full SEO Audit — maxmungaristudio.com
**Updated:** 2026-06-22 (post-fix pass)  
**Previous score:** 66/100  
**Current score:** 72/100 (+6)

---

## Executive Summary

**Business type:** Local Service (hybrid) — Recording Studio & Online Mixing/Mastering, Crotone IT  
**Pages audited:** 4 (index.html IT, index.html EN, privacy.html IT, privacy.html EN)

### Score by category

| Category | Weight | Score | Δ |
|---|---|---|---|
| Technical SEO | 22% | 60/100 | +0 |
| Content Quality | 23% | 72/100 | +2 |
| On-Page SEO | 20% | 65/100 | +3 |
| Schema / Structured Data | 10% | 80/100 | +10 |
| Performance (CWV) | 10% | 48/100 | +0 |
| AI Search Readiness | 10% | 78/100 | +20 |
| Images | 5% | 70/100 | +5 |

**Overall: 72/100**

---

## Fixed Since Previous Audit ✅

- Meta description shortened (192 → 138 chars) — IT + EN
- `<meta name="keywords">` removed — IT + EN
- Schema `openingHours` → array format
- Schema `areaServed` added (City/Calabria/IT)
- Schema `Person.knowsAbout` added
- Schema `Person.url` → `#bio` (anchor exists at line 388)
- `#quote-strip` `aria-hidden` removed — Audiofader quote now indexable
- Alt text differentiated: eko2, vanguard2 no longer duplicate
- `llms.txt` created at root — AI crawler ready
- `main.js`: dead bio carousel block removed (-44 lines)
- `abc-player.js`: XHR → fetch, drawBars refactor (-28 lines)

---

## Remaining Issues

### 🔴 CRITICAL

#### C1 — Hero LCP: no static img candidate
`index.html:282` — `<div class="hero-carousel" id="heroCarousel" aria-hidden="true"></div>` is empty. All slide images injected via JS (`main.js:108-131`). Googlebot sees no img above the fold. LCP candidate is undefined or body text.

**Fix:** Add static `<img src="newassets/hero1.webp" fetchpriority="high">` before `#heroCarousel`. JS then manages slides 2+.  
**Risk:** Medium — need to verify `#hero` CSS has `position: relative; overflow: hidden`.

#### C2 — Splash screen blocks Googlebot
`main.js:232-235`: `if (sessionStorage.getItem('introPlayed')) { screen.style.display='none'; return; }` — Googlebot ignores sessionStorage, sees the splash on every crawl. Splash covers `#hero` and all content below it. LCP destroyed.

**Fix:** Modify `main.js` startTransition / intro flow — NOT with a separate inline script. The scroll-lock (`document.body.style.overflow='hidden'`) is released inside `startTransition()`. Any external script that hides the splash without calling `startTransition()` leaves scroll locked.

**Correct approach:**  
```js
// In the intro IIFE, before the sessionStorage check:
if (!document.getElementById('intro-screen')) return; // safety
if (sessionStorage.getItem('introPlayed')) {
  screen.remove();        // remove instead of display:none
  document.body.style.overflow = '';  // ensure scroll unlocked
  return;
}
```
This is already correct in `main.js:232-235` for the `display:none` path. The remaining issue is Googlebot, which never sets sessionStorage and therefore always sees the splash. **No CSS-only fix exists for this.** Options:
- A) Remove `#intro-screen` entirely — most impactful for SEO, breaks the brand animation
- B) Accept the Googlebot penalty — splash is a deliberate brand choice

#### C3 — H1 not keyword-optimized
`index.html:289-291`: `<h1 class="hero-title">Max<br />Mungari<br /><em>Studio</em></h1>` — branded H1. Primary keyword "Mixing & Mastering Professionale Online" appears only in `<title>` and `<p class="hero-eyebrow">`.

**Fix:**
```html
<h1 class="hero-eyebrow">Mixing &amp; Mastering Professionale Online</h1>
<p class="hero-title">Max<br />Mungari<br /><em>Studio</em></p>
```
Style via CSS, no visual change if `hero-eyebrow` and `hero-title` keep same classes.

---

### 🟠 HIGH

#### H1 — Unminified CSS/JS in production
`index.html:173`: `style.css?v=20260618` — unminified  
`index.html:967`: `main.js?v=20260618` — unminified  
`style.min.css` and `main.min.js` exist but are **outdated** (not synced with current source). Cannot switch until regenerated.

**Fix:** Run minification (e.g. `npx lightningcss style.css -o style.min.css` + `npx terser main.js -o main.min.js`), then switch references.

#### H2 — Vimeo API loaded eagerly
`index.html:159`: `<script src="https://player.vimeo.com/api/player.js" defer>` — loads on every page visit. Adds ~45KB + DNS lookup even for users who close the tab before the hero video plays.

**Fix:** Remove from `<head>`. In `main.js` hero carousel IIFE, load dynamically when hero enters viewport:
```js
// Before initPlayer(), add:
function loadVimeoAPI(cb) {
  if (typeof Vimeo !== 'undefined') { cb(); return; }
  var s = document.createElement('script');
  s.src = 'https://player.vimeo.com/api/player.js';
  s.onload = cb;
  document.head.appendChild(s);
}
// Then: loadVimeoAPI(initPlayer);
```

#### H3 — Partner logos as PNG
`newassets/avid1.png`, `avid3.png`, `eko.png`, `eko2.png`, `vanguard1.png`, `vanguard2.png` — PNG format. WebP typically 40-60% smaller at same quality.

**Fix:** `cwebp -q 85 avid1.png -o avid1.webp` for each, update `src` in HTML.

#### H4 — No reviews/testimonials
Zero on-page client reviews. Google's E-E-A-T signals depend heavily on third-party validation. Audiofader quote is present but uncredited to a client.

**Fix:** 3-5 real reviews (name + project type + quote) + `AggregateRating` schema once collected.

---

### 🟡 MEDIUM

#### M1 — TODO.txt exposed at root
`maxmungaristudio.com/TODO.txt` is publicly accessible. Contains internal project notes and client track names. Not a security risk but unprofessional for a client-facing domain. Add to `robots.txt` `Disallow: /TODO.txt` or delete from public root.

#### M2 — OG/Twitter description not synced with meta description
`og:description` (line 18): "Mixing, Mastering e Music Production professionale da Studio 1976, Crotone. Invia i tuoi brani, ottieni un suono da radio." — different from updated meta description. Update to match.

#### M3 — No `favicon.ico` at root
Only PNG favicons. Some crawlers and older browsers request `/favicon.ico`. A missing `/favicon.ico` generates a 404.

**Fix:** Place 16×16 + 32×32 ICO at root. Free tools: favicon.io, realfavicongenerator.net.

#### M4 — Audio on Dropbox CDN
ABC player tracks loaded from `dl.dropboxusercontent.com`. Dropbox is not a CDN — rate limits apply, and URLs can expire if Dropbox account settings change.

**Fix:** Host audio on own server or proper CDN (Cloudflare R2, Backblaze B2, Bunny CDN).

#### M5 — CLS risk: showcase/studio carousel images without intrinsic dimensions
Image tags in carousels lack `width`/`height` attributes. Browser can't reserve space before image loads → layout shifts.

---

### 🟢 LOW

#### L1 — `hasMap` uses query URL not Place ID
Schema `hasMap: "https://maps.google.com/?q=Via+Lina+Merlin+1,+Crotone"` — Google prefers Place ID URL for precise disambiguation.

#### L2 — No Google Business Profile verification signal
No `sameAs` link to GBP URL in LocalBusiness schema. After GBP verification, add the profile URL to `sameAs`.

#### L3 — Service sub-pages missing
No `/servizi/mixing-professionale/`, `/servizi/mastering-online/` etc. Long-tail keyword coverage is zero at page level.

---

## What's Working Well ✅

- Canonical + hreflang correctly implemented (IT/EN/x-default)
- robots.txt correct (Allow: /, sitemap declared)
- sitemap.xml correct (4 URLs with hreflang xhtml:link)
- OpenGraph fully implemented (title, description, image, locale, alternate)
- Twitter Card implemented
- Geo meta tags (geo.region, geo.placename, ICBM)
- LocalBusiness schema: complete address, geo coords, sameAs, hasOfferCatalog
- Person schema: knowsAbout, worksFor cross-reference
- Navigation schema (ItemList with SiteNavigationElement)
- Audiofader quote now indexable (aria-hidden removed)
- llms.txt at root — AI citation ready
- Map consent gate (GDPR compliant)
- WhatsApp button with scroll-reveal
- Passive scroll listeners throughout
- IntersectionObserver-based reveal + carousel pause
- Self-hosted fonts (no Google Fonts dependency)

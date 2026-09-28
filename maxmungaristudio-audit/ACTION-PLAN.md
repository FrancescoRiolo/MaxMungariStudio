# Action Plan — maxmungaristudio.com
**Updated:** 2026-06-22 (post-fix pass)

---

## Phase 1: Critical — Before Launch

### 1.1 — H1 keyword optimization ⭐ SAFE, 5 MIN
**File:** `index.html:287-291`, `en/index.html:287-291`
```html
<!-- IT: cambia da: -->
<p class="hero-eyebrow">Produzioni Musicali</p>
<h1 class="hero-title">Max<br />Mungari<br /><em>Studio</em></h1>

<!-- a: -->
<h1 class="hero-eyebrow">Mixing &amp; Mastering Professionale Online</h1>
<p class="hero-title">Max<br />Mungari<br /><em>Studio</em></p>
```
```html
<!-- EN: -->
<h1 class="hero-eyebrow">Professional Online Mixing &amp; Mastering</h1>
<p class="hero-title">Max<br />Mungari<br /><em>Studio</em></p>
```

### 1.2 — Hero LCP static img ⭐ MEDIUM RISK
**File:** `index.html:281-282`, `en/index.html:281-282`
Verify `#hero` has `position: relative` + `overflow: hidden` in `style.css` first.
```html
<section id="hero" aria-label="Max Mungari Studio — Homepage">
  <img
    src="newassets/hero1.webp"
    alt=""
    aria-hidden="true"
    fetchpriority="high"
    decoding="sync"
    width="1920" height="1080"
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"
  />
  <div class="hero-carousel" id="heroCarousel" aria-hidden="true"></div>
```

### 1.3 — Splash screen Googlebot fix ⭐ RICHIEDE DISCUSSIONE
**Decision needed:** Remove splash entirely (max SEO gain) or accept Google penalty (preserve brand animation)?  
If remove: delete `#intro-screen` div from both HTML files, delete the intro IIFE from `main.js`.  
If keep: no code fix available — Googlebot always sees splash.

### 1.4 — Lazy-load Vimeo API
**File:** `index.html:159` (remove), `main.js:197-202` (replace)
Remove: `<script src="https://player.vimeo.com/api/player.js" defer></script>`

In `main.js`, replace the `if (typeof Vimeo !== 'undefined') { initPlayer(); } else { ... }` block:
```js
function loadVimeoAPI(cb) {
  if (typeof Vimeo !== 'undefined') { cb(); return; }
  var s = document.createElement('script');
  s.src = 'https://player.vimeo.com/api/player.js';
  s.onload = cb;
  document.head.appendChild(s);
}
loadVimeoAPI(initPlayer);
```
Remove the `document.addEventListener('DOMContentLoaded', initPlayer)` fallback — no longer needed.

### 1.5 — Regenerate minified assets, switch references
```powershell
npx lightningcss style.css --minify -o style.min.css
npx terser main.js -o main.min.js
npx terser abc-player.js -o abc-player.min.js
```
Then in both HTML files: `style.css` → `style.min.css`, `main.js` → `main.min.js`, `abc-player.js` → `abc-player.min.js`.

---

## Phase 2: High-Impact (Week 2–3)

### 2.1 — OG/Twitter description sync
`index.html:18` and `en/index.html:18` — update `og:description` to match meta description.

### 2.2 — Convert PNG partner logos to WebP
```powershell
# From newassets/:
cwebp -q 85 avid1.png -o avid1.webp
cwebp -q 85 avid3.png -o avid3.webp
cwebp -q 85 eko.png   -o eko.webp
cwebp -q 85 eko2.png  -o eko2.webp
cwebp -q 85 vanguard1.png -o vanguard1.webp
cwebp -q 85 vanguard2.png -o vanguard2.webp
```
Update `src` in both HTML files.

### 2.3 — Add reviews / testimonials
Collect 3–5 real client reviews (name, project type, quote).
Add to HTML before `#contatti`. Add `AggregateRating` to LocalBusiness schema.

### 2.4 — Migrate audio to proper CDN
Move ABC player tracks from Dropbox to Cloudflare R2, Backblaze B2, or Bunny CDN.
Update URLs in `window.ABC_TRACKS_*` objects in both HTML files.

---

## Phase 3: Medium Fixes (Month 2)

### 3.1 — Remove/protect TODO.txt
Either: delete from public root, or add to `robots.txt`:
```
Disallow: /TODO.txt
```

### 3.2 — Add favicon.ico at root
Generate at realfavicongenerator.net. Place `favicon.ico` at `maxmungaristudio.com/favicon.ico`.

### 3.3 — Fix carousel image CLS
Add `width`/`height` to images inside `.showcase-grid`, `.lavori-img-carousel`, `.svc-img-carousel`, `.studio-carousel`.

### 3.4 — Create service sub-pages
- `/servizi/mixing-professionale/`
- `/servizi/mastering-online/`
- `/servizi/stem-mixing/`
- `/servizi/music-production-crotone/`

---

## Phase 4: Monitoring (Ongoing)

### 4.1 — Google Search Console
Submit sitemap, request indexing of IT + EN homepage.

### 4.2 — Verify schema in Rich Results Test
After deploy: test `https://maxmungaristudio.com/` at search.google.com/test/rich-results.

### 4.3 — GBP verification
Add GBP URL to schema `sameAs` after verification.

### 4.4 — Monitor AI citation
Search "Max Mungari" and "mixing mastering Crotone" in ChatGPT, Perplexity, Google AI Overviews.

---

## Effort / Impact Matrix

| Fix | Effort | Impact | Risk |
|---|---|---|---|
| H1 keyword | XS (5 min) | High (Rankings) | Zero |
| OG description sync | XS (2 min) | Low (Social CTR) | Zero |
| TODO.txt robots | XS (1 min) | Low | Zero |
| Lazy-load Vimeo | S (30 min) | High (Performance) | Low |
| Hero LCP img | S (30 min) | Critical (LCP) | Medium |
| Regen + switch min assets | S (30 min) | High (Performance) | Low |
| PNG → WebP logos | S (1 hr) | Medium (Performance) | Low |
| Reviews section | M (4 hr) | Critical (E-E-A-T) | Zero |
| Service sub-pages | L (2-3 days) | Very High (Rankings) | Zero |
| Remove splash | M (1 hr) | Critical (LCP, UX) | High (brand) |

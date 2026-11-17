# design.dreamour.in

Website for **Dreamour Design**, the architecture, interior, landscape and product design studio founded by architect Ramyaa Yuvanesan in Chennai.

It's a fast static site: plain HTML, CSS and JavaScript with no framework, database or plugins. It is hosted free on GitHub Pages at **https://design.dreamour.in**.

## What's inside

| Path | Page |
|---|---|
| `/` | Home: parallax hero, services, featured works, process |
| `/about/` | Studio story, ventures (Amazon cookware, RYST Toys), philosophy |
| `/services/` | Architecture, Interior, Landscape and Product design |
| `/works/` | Portfolio with filters |
| `/works/<project>/` | One page per project, with a photo gallery and lightbox |
| `/contact-us/` | Address, phone, email, map, enquiry form |
| `/dream-builder/` | Step-by-step design questionnaire |
| `/terms-conditions/`, `/home/privacy-policy/`, `/cookie-policy/`, `/return-and-cancellation/` | Policies |

The old WordPress URLs are kept, so existing links and Google results still work.

Forms don't need a server. Visitors send their answers by **WhatsApp** (+91 96001 25599) or **email** (info@dreamour.in).

## SEO

- A unique title and description on every page, plus canonical URLs and Open Graph/Twitter share images
- Structured data: business (ProfessionalService), services, breadcrumbs, project pages (CreativeWork)
- `sitemap.xml` with image entries, and `robots.txt`
- WebP images in responsive sizes, lazy loading, a preloaded hero image, and no render-blocking JS

After going live, add the site to [Google Search Console](https://search.google.com/search-console) and submit `https://design.dreamour.in/sitemap.xml`.

## Editing content

All pages are generated from one file, so the header, footer and SEO stay consistent:

```bash
python3 _build/build.py      # needs Python 3 and Pillow (pip install pillow)
```

- **Contact details, services and projects** are at the top of `_build/build.py`.
- **Policy text** is in `_build/legal/`.
- **Styles** are in `assets/css/site.css`, and **interactions** in `assets/js/site.js`.
- **Photos** are in `assets/img/p/`. Each photo needs `name-800.webp`, `name-1600.webp`, `name-1600.jpg` and optionally `name-2400.webp`.

Commit and push to `main`. GitHub Pages republishes within a minute or two.

## Hosting setup (one time)

1. **GitHub:** go to repo → Settings → Pages → *Build and deployment*. Set Source to **Deploy from a branch**, Branch to **main**, and folder to **/ (root)**. Under *Custom domain*, enter `design.dreamour.in` (the `CNAME` file already contains it). Once the certificate is issued, tick **Enforce HTTPS**.
2. **DNS** (wherever dreamour.in is managed): replace the existing record for `design` with
   `CNAME  design  →  yuvanesanm.github.io`
3. Email (info@dreamour.in) runs on the main `dreamour.in` domain, so changing the `design` record doesn't affect it.

## Privacy & compliance

- No cookies, analytics or trackers. Fonts are self-hosted, and the Google Map loads only when a visitor clicks it.
- Policies (Terms, Privacy, Cookies, Returns) are in `_build/legal/`. They reference the DPDP Act 2023, the IT Act 2000 and the Consumer Protection Act 2019. When you change one, update `POLICY_DATE` in `_build/build.py`.
- If you ever add analytics or ads, update the Cookie Policy and add a consent banner first.

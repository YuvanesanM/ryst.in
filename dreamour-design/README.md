# design.dreamour.in — Dreamour Design

A static rebuild of the Dreamour Design WordPress site: plain HTML, CSS and JS with no build step and no database.
It uses the same content, photos, logo colours (purple `#7e4ca5`, grey `#5c5c5c`) and fonts (Josefin Sans, Crimson Text).

## Deploy

Upload everything in this folder to the web root of `design.dreamour.in` (GitHub Pages, Netlify, Cloudflare Pages or any static host).
Old WordPress URLs keep working because each page lives at the same path:

| Page | Path |
|---|---|
| Home | `/` |
| About Us | `/about/` |
| Services | `/services/` |
| Our Works | `/works/` |
| Contact Us | `/contact-us/` |
| Dream Builder questionnaire | `/dream-builder/` |
| Terms & Conditions | `/terms-conditions/` |
| Privacy Policy | `/home/privacy-policy/` |
| Return and Cancellation | `/return-and-cancellation/` |

`404.html` is the not-found page. `CNAME` is only used by GitHub Pages.

## Forms

The Contact form and the Dream Builder questionnaire have no server. Visitors choose:
- **WhatsApp** — opens a chat with +91 96001 25599 with their answers typed in, or
- **Email** — opens their email app addressed to info@design.dreamour.in.

Phone, WhatsApp number and email are set at the top of `assets/site.js` and appear in the page footers.

## Editing

- Text lives directly in each page's `index.html`.
- Project photos are in `assets/img/works/` (`name.jpg` is 1600px wide, `name-800.jpg` is 800px).
- Styles are in `assets/style.css`.

## Not carried over

- The WooCommerce cart (it was empty and there was no shop page).
- The Facebook Messenger chat widget and Jetpack/Google tracking scripts. The floating WhatsApp button replaces the chat widget.

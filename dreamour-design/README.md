# design.dreamour.in — Dreamour Design website

Static site (plain HTML/CSS/JS, no build step). Upload the contents of this folder to the web root of `design.dreamour.in`.

## Before going live — replace placeholders

Search the folder for `EDIT_` and replace:

| Placeholder | Where | Replace with |
|---|---|---|
| `EDIT_CITY` | index.html (hero, FAQ, contact, footer, JSON-LD) | Your city, e.g. `Chennai` |
| `EDIT_STREET_ADDRESS` | index.html (contact, JSON-LD) | Studio street address |
| `EDIT_EMAIL` | index.html (contact, form `data-email`, JSON-LD) | Enquiry email — the form sends to this |
| `EDIT_INSTAGRAM` | index.html (gallery button, contact, JSON-LD) | Instagram handle without `@` |
| `EDIT: project name · area` | index.html gallery captions | e.g. `Villa in Adyar · 3BHK` |

Also review the **Services** list and **FAQ** answers so they match what you actually offer.

## Project photos

Put JPGs (about 1600px wide, under ~400 KB each) in `assets/projects/` with these names:

`living-1.jpg`, `living-2.jpg`, `kitchen-1.jpg`, `kitchen-2.jpg`, `bedroom-1.jpg`, `bedroom-2.jpg`, `commercial-1.jpg`, `commercial-2.jpg`

Until a photo is added, its tile shows a soft colour block. `living-1` is a tall tile and `commercial-1` is a wide tile.

## Hosting notes

- Paths are root-relative (`/assets/...`), so serve it at the domain root.
- `CNAME` is for GitHub Pages; other hosts can ignore it.
- `404.html` is picked up automatically by GitHub Pages, Netlify and Cloudflare Pages.
- The enquiry form opens the visitor's email app (no server needed). To receive submissions directly instead, point the form at a service like Formspree.

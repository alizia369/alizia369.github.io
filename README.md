# ali-zia.me

Source for Ali Zia's research website. The same files are published in two places:

- **https://alizia369.github.io** by GitHub Pages, straight from this repository
- **https://ali-zia.me** on Solid Hosting, uploaded by `.github/workflows/deploy-ftp.yml` on every push to `main`

## Updating the site

Most updates only touch the data files, then rebuild:

| To change | Edit |
|---|---|
| News | `data/news.json` (newest first; the first six show, the rest sit behind "Show older news") |
| Publications | `data/publications.json` (set `"featured": true` and add an entry in `FEATURED_COPY` in `build.py` to show it on the home page) |
| Research projects | `data/projects.json` (images go in `assets/img/projects/`) |
| Page text (bio, Teaching, CV) | the matching `build_*` function in `build.py` |
| Look and feel | `assets/css/site.css` |

Then run `python3 build.py` (Python 3.12 or newer, standard library only) and commit the generated `index.html` files along with your edits.

## Files

- `build.py` generates `index.html`, `research/`, `publications/`, `teaching/` and `cv/`
- `assets/` holds styles, scripts, images, CV PDFs and the livestock video
- `acml2026-tdl` and `horl2026` are separate repositories served under this site's address

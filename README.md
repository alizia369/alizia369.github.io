# ali-zia.me

Source for Ali Zia's research website. The same files are published in two places:

- **https://alizia369.github.io** by GitHub Pages, straight from this repository
- **https://ali-zia.me** on Solid Hosting, uploaded by `.github/workflows/deploy-ftp.yml` on every push to `main`

## Updating the site

Most updates only touch the data files, then rebuild:

| To change | Edit |
|---|---|
| News | `data/news.json` (newest first; the first six show, the rest sit behind "Show older news") |
| Publications | `data/publications.json` (`"selected": true` puts a paper in the home page list; featured cards are set in `FEATURED_COPY` in `build.py`) |
| Research projects | `data/projects.json` (images go in `assets/img/projects/`) |
| Grants | `data/grants.json` (the summary line and the table on the Grants page) |
| Page text (bio, Teaching, Resume) | the matching `build_*` function in `build.py` |
| Look and feel | `assets/css/site.css` |

Then run `python3 build.py` (Python 3.12 or newer, standard library only) and commit the generated `index.html` files along with your edits.

## Files

- `build.py` generates `index.html`, `research/`, `publications/`, `teaching/`, `grants/` and `resume/` (plus a redirect from the old `cv/` address)
- `assets/` holds styles, scripts, images, CV PDFs and the livestock video
- `acml2026-tdl` and `horl2026` are separate repositories served under this site's address

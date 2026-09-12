# builtbyduke.de

Production-ready static multi-page website for deployment on GitHub Pages.

## Tech Stack

- HTML5 (multi-page)
- CSS3 (single global stylesheet)
- Vanilla JavaScript (single global script)

## Project Structure

.
|-- 404.html
|-- index.html
|-- netlify.toml
|-- portfolio.html
|-- staff.html
|-- style.css
|-- script.js
|-- .gitignore
|-- assets
|	 |-- icons
|	 |   |-- discord.svg
|	 |   |-- email.svg
|	 |   |-- github.svg
|	 |   `-- globe.svg
|	 `-- images
|		  |-- background.jpg
|		  `-- profile.jpg
`-- devlog                    (dev.log — Minecraft/coding build-notes sub-site)
	 |-- index.html
	 |-- build.py           (regenerates pages/ from content/*.md)
	 |-- content            (markdown source)
	 |-- pages              (generated HTML pages)
	 `-- assets              (its own style.css/nav.js, separate from the root site)

## Sub-site: dev.log

`devlog/` is a self-contained static sub-site (linked from the main nav as "Dev Log") with its
own stylesheet and layout. It's generated from Markdown in `devlog/content/` via `devlog/build.py`.
To add or edit a page: edit/add a `.md` file in `devlog/content/`, wire it into `MANIFEST` in
`devlog/build.py`, then run:

```bash
pip install markdown
python3 devlog/build.py
```

This rebuilds `devlog/pages/*.html` and `devlog/index.html` in place.

## Run Locally

Because this is a static site, you can open `index.html` directly.

For a local server (recommended):

```bash
npx serve .
```

Then open the URL printed in your terminal.

## Deploy to Netlify

1. Push this repository to GitHub.
2. In Netlify, click "Add new site" -> "Import an existing project".
3. Select this repo.
4. Build command: leave empty.
5. Publish directory: `.`
6. Deploy.

`netlify.toml` is already included and production-ready for this static setup.

## Deploy to GitHub Pages

This repository includes a workflow at `.github/workflows/deploy-pages.yml` that publishes to the `gh-pages` branch.

1. Push to `main`.
2. In GitHub, open Settings -> Pages.
3. Under Build and deployment, set Source to `Deploy from a branch`.
4. Select branch `gh-pages` and folder `/(root)`.
5. The `Deploy static site to GitHub Pages` workflow will update `gh-pages` on each push to `main`.

Your site URL will be:

- `https://calebclub.github.io/bbde/` (project pages)

Since this site uses relative paths (for `index.html`, `staff.html`, `portfolio.html`, CSS, JS, and assets), all pages work correctly under the repository subpath.

## Customize Content Quickly

1. Update display name and hero text:
	- `index.html`
2. Update social/contact links:
	- `index.html`
	- footer links on all pages
3. Update staff resume details:
	- `staff.html`
4. Update project cards:
	- `portfolio.html`
5. Update color/style system:
	- `style.css` CSS variables in `:root`

## Notes

- The small AI lock label text has been set to exactly: `password needed (CAI)`.
- The CAI label links to: `https://nexus-coder-4.preview.emergentagent.com/`.
- The script keeps the passphrase check as `FISHERTHECAT` for the local demo widget.
- Your provided images are wired as:
  - `assets/images/profile.jpg`
  - `assets/images/background.jpg`

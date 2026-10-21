# SOMaR data format (draft)

Draft community standard for data formats used by the *Sensing the Ocean with Marine Radar* (SOMaR) community: NetCDF conventions for sharing and post-processing marine radar products at different processing levels, from raw radar recordings to derived geophysical variables. The formats follow the NetCDF Climate and Forecast (CF) conventions wherever possible, use the Attribute Convention for Data Discovery (ACDD) for discovery metadata and follow WMO FM 301 (and CfRadial for moving platforms) for radar data in polar coordinates, and define what these standards leave open, in particular how gridded products from a moving vessel are stored.

The specification is a [Jekyll] site using the [Just the Docs] theme, published at
<https://sensing-the-ocean-with-marine-radar.github.io/somar-format-draft>.
For more about the community, see the [SOMaR GitHub organization](https://github.com/sensing-the-ocean-with-marine-radar).

## Repository layout

| Path | Content |
| --- | --- |
| `index.md` | Home page / abstract |
| `contents/introduction/` | Scope, motivation, terms, and document structure |
| `contents/metadata_attributes/` | Mandatory and recommended global attributes, variable attributes, Level 2 variables, radar parameters, georeference correction parameters, wave calibration parameters |
| `contents/georeferencing/` | Polar coordinates, georeference correction application, antenna offsets, CRS variables, time-bounded local grids, analysis windows |
| `contents/product_types/` | Level 1 products (polar raw data, regularized polar images, Cartesian images) and the two categories of Level 2 products (gridded and spatially averaged), with the product-type tables |
| `contents/annex/` | Informative example files of all products, with descriptions of the Level 2 products and their retrieval |
| `contents/file_naming/` | File naming pattern recommendations |
| `contents/references/` | Scientific literature and the standards SOMaR builds on |
| `contents/about/` | About the SOMaR community |
| `scripts/check_examples.py` | Builds and checks the CDL examples (see [Checking the examples](#checking-the-examples)) |
| `scripts/build_pdf.py` | Builds the PDF of the whole specification from the built site (see [Building the PDF](#building-the-pdf)) |
| `_config.yml`, `Gemfile` | Site and theme configuration |
| `.github/workflows/` | `ci.yml` builds the site on pushes and pull requests; `pages.yml` deploys it to GitHub Pages |

## Building the site locally

Requires [Ruby] (3.3 is used in CI) and [Bundler].

```sh
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. The built site is written to `_site/`.

## Checking the examples

The CDL examples on the pages are built with `ncgen` and checked against the CF standard name table, UDUNITS, and the SOMaR rules for global attributes and file names:

```sh
pip install cf-units   # optional locally; without it, the unit checks are skipped
python3 scripts/check_examples.py
```

The script requires `ncgen` and `ncdump` (e.g. from the `netcdf-bin` package) and runs in CI on every push and pull request. CI runs it as `python3 scripts/check_examples.py --strict`, which fails instead of skipping the unit checks when `cf-units` is missing; run it the same way locally to get the same result. On its first run, the script downloads the CF standard name table (version 95) from cfconventions.org and caches it in the system temporary directory, so it needs network access once. Every code block is checked except those whose first line is `// excerpt`. A line `group: <name> { ... }` stands for the example of that group on its Metadata page and is expanded before the build. Dimension lengths are capped at 3, so the `data:` sections of the examples must hold scalars only.

## Building the PDF

The PDF linked from the top bar of every page (`somar-format.pdf`) is built from the built site, with a table of contents and the pages in the order of the navigation:

```sh
pip install beautifulsoup4 pypdf playwright
playwright install chromium
bundle exec jekyll build
python3 scripts/build_pdf.py _site
```

The script writes `_site/somar-format.pdf`. It prints the pages with headless Chromium and needs network access to load MathJax and the fonts (Noto Sans and Source Code Pro, from jsDelivr). The page footer uses an installed Noto Sans (`fonts-noto-core` on Debian and Ubuntu) and falls back to the default sans-serif font without it. `pages.yml` builds the PDF before deploying the site, and `ci.yml` builds it on every push and pull request and uploads it as the `somar-format-pdf` artifact of the run.

## Releasing a version

1. Set `somar_version` and `somar_status` in `_config.yml` (`"draft"` for a draft, `"released"` for a release).
2. Update the `Conventions` attribute of the examples to match, e.g. `SOMaR-0.6-draft` or `SOMaR-1.0`; `scripts/check_examples.py` fails until they do.
3. Tag the commit `v<major>.<minor>` (with a third number for corrections that change no file, e.g. `v1.0.1`) and publish it as a GitHub release whose notes list the changes that affect files. From version 1.0 on, also add an entry to a revision history page.

Releases are archived with a DOI once the repository is enabled in [Zenodo's GitHub integration](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content).

## Editing the specification

- Pages are Markdown files. The front matter (`title`, `parent`, `nav_order`) determines the page's place in the navigation.
- Each Level 1 product type has its own page under `contents/product_types/level1/`. A Level 2 product type is a row in the product-type table of its category under `contents/product_types/level2/`, its variables are defined in `contents/metadata_attributes/level2_variables.md`, and its example file is a page under `contents/annex/`, as is that of each Level 1 product. Attributes and variables shared by more than one product belong in `contents/metadata_attributes/`.
- Please propose changes through issues or pull requests.

## License and attribution

This repository is licensed under the [MIT License](LICENSE). The site is based on the [just-the-docs template](https://github.com/just-the-docs/just-the-docs-template), and the deployment workflow is based on GitHub's [starter workflows].

[Jekyll]: https://jekyllrb.com
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[Ruby]: https://www.ruby-lang.org
[Bundler]: https://bundler.io
[starter workflows]: https://github.com/actions/starter-workflows/blob/main/pages/jekyll.yml

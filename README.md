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
| `contents/metadata_attributes/` | Mandatory and recommended global attributes, variable attributes, processing parameters, quality flags, radar parameters, georeference correction parameters, wave calibration parameters |
| `contents/georeferencing/` | Polar coordinates, georeference correction application, antenna offsets, CRS variables, time-bounded local grids, analysis windows |
| `contents/product_types/` | The processing levels, the three categories of products, polar, gridded, and spatially averaged, each with its product-type table, and the product variables |
| `contents/annex/` | Informative example files of all products, with descriptions of the Level 2 products and their retrieval |
| `contents/file_naming/` | File naming pattern recommendations |
| `contents/references/` | Scientific literature and the standards SOMaR builds on |
| `contents/about/` | About the SOMaR community |
| `scripts/check_examples.py` | Builds and checks the CDL examples (see [Checking the examples](#checking-the-examples)) |
| `scripts/build_pdf.py` | Builds the PDF of the whole specification from the built site (see [Building the PDF](#building-the-pdf)) |
| `scripts/check_links.py` | Checks the internal links and anchors of the built site (see [Building the PDF](#building-the-pdf)) |
| `scripts/link_items.py` | Links the names of attributes and variables, in the tables and in the text, to the rows that define them, and checks the links of the text against the rule under [Links](#links); with `--check`, as in CI, it lists the missing links instead |
| `scripts/time_bounded_grids_figure.py` | Draws the figure of the time-bounded grids on the Georeferencing page, `assets/images/time_bounded_grids.svg`, to scale |
| `_config.yml`, `Gemfile` | Site and theme configuration |
| `.github/workflows/` | `ci.yml` builds the site and the PDF and checks the examples and links on pushes and pull requests; `pages.yml` checks and deploys them to GitHub Pages |

## Building the site locally

Requires [Ruby] (3.3 is used in CI) and [Bundler].

```sh
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000/somar-format-draft/> (the site is served under its `baseurl`). The built site is written to `_site/`.

## Checking the examples

The CDL examples on the pages are built with `ncgen` and checked against the CF standard name table, UDUNITS, the CF rules for references between variables, `cell_methods`, and bounds, and the SOMaR rules for global attributes, file names, tier markers, the required, recommended, and conditional items of each product, the types, dimensions, and units of the variables, the file contents tables of the annex, the rules of rotated local grids, and the agreement of times, flags, and spatial bounds; the script also checks that the attribute tables are in alphabetical order and that every page listing the product types lists the same ones:

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
Then `python3 scripts/check_links.py _site` checks that every internal link and anchor of the built site, the PDF link included, resolves; CI runs it after building the PDF.

## Releasing a version

1. Set `somar_version` and `somar_status` in `_config.yml` (`"draft"` for a draft, `"released"` for a release).
2. Update the `Conventions` attribute of the examples to match, e.g. `SOMaR-0.6-draft` or `SOMaR-1.0`; `scripts/check_examples.py` fails until they do.
3. Tag the commit `v<major>.<minor>-draft` for a draft (e.g. `v0.5-draft`) or `v<major>.<minor>` for a release (with a third number for corrections that change no file, e.g. `v1.0.1`), and publish it as a GitHub release whose notes list the changes that affect files. From version 1.0 on, also add an entry to a revision history page.
4. Right after tagging a draft, set `somar_version` to the next minor version (e.g. `"0.6"`) and update the `Conventions` of the examples to match, so that the working copy no longer declares the string of the tagged draft.

Releases are archived with a DOI once the repository is enabled in [Zenodo's GitHub integration](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content).

## Editing the specification

- Pages are Markdown files. The front matter (`title`, `parent`, `nav_order`) determines the page's place in the navigation.
- A product type is a row in the product-type table of its category page under `contents/product_types/` (polar, gridded, or spatially averaged), its variables are defined in `contents/product_types/product_variables.md`, and its example file is a page under `contents/annex/`. Attributes and variables shared by more than one product belong in `contents/metadata_attributes/`.
- Each product page of the annex begins with its file contents, the layout of the file and a table of its items, which summarize the definitions of the product for readers; its items link to the rows that define them (every row of an attribute or variable table has an id, see `_plugins/table_rows.rb`). The annex is informative: its prose describes the products and states no requirements.
- Links follow the rule under [Links](#links).
- A tier that depends on the file is written in the fixed form described under [Requirements](contents/product_types/index.md#requirements), such as "Required on the local grid; recommended on the geographic grid.", so that `scripts/check_examples.py` can resolve it for each example.
- Please propose changes through issues or pull requests.

### Links

1. In each section (one `##` heading), the first mention of a target outside the section is linked, and no target is linked twice.
2. A link points to the closest anchor: the row of an item, the section of a topic, the top of a page only for the page as a whole. A group name, such as `radar_parameters`, links to its page.
3. An attribute or variable is linked on its first mention: in the description of a table row, if another table defines it; in the text, per section, if another page defines it. The link text is the name alone, as `` [`name`](…) ``. Every row of an attribute or variable table has an id for this (see `_plugins/table_rows.rb`).
4. The conventions (CF, the CF standard name table, ACDD, FM 301, CfRadial, UDUNITS) are linked reference-style, as `[CF][cf]` with the URL at the foot of the page, with one URL each, for the version SOMaR pins: CF 1.13, the standard name table of the version the example check uses, ACDD 1.3. UDUNITS, of which SOMaR pins no version, links to its current documentation. Other external links are inline.
5. Literature is cited as author and linked year, such as "Young et al. [1985](contents/references/index.md#young-1985)", to its entry on the References page.
6. A "see …" reference uses the heading of its target as its link text.

`python3 scripts/link_items.py` adds the links of rule 3, and `--check`, which CI runs, fails on a missing one, on a repeated link (rule 1), on a link text that mixes code and words (rule 3), and on an inline or unversioned link to a convention (rule 4). A name that the script cannot resolve, such as `time`, which several tables define, stays plain. A value is written in quotes, such as `"trajectory"`, and a product type follows the words "product type", so that neither is taken for the name of an item. Which topics to link (rule 1), the anchor (rule 2), and the text of a "see …" reference (rule 6) are left to the author.

### Checklist for a change to a definition

- [ ] The examples, minimal forms, and file contents tables of the affected products are updated; `python3 scripts/check_examples.py --strict` passes.
- [ ] The descriptions of the affected products in the annex are reread and still agree with the definitions.
- [ ] A new conditional tier uses the fixed form; a new condition is added to the description under Requirements and to `scripts/check_examples.py`.
- [ ] A new section of a category page whose tables apply to some of its products only, such as the sweeps of Level 1a on the page of the polar products, is added to `SECTION_SCOPES` in `scripts/check_examples.py`; otherwise its rows apply to every product of the category.
- [ ] `python3 scripts/link_items.py` is run after editing tables or text, so that the names link to their definitions; "see …" references use the heading of their target.
- [ ] `bundle exec jekyll build` and `python3 scripts/check_links.py _site` pass, so that the links to the definitions resolve.

## License and attribution

This repository is licensed under the [MIT License](LICENSE). The site is based on the [just-the-docs template](https://github.com/just-the-docs/just-the-docs-template), and the deployment workflow is based on GitHub's [starter workflows].

[Jekyll]: https://jekyllrb.com
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[Ruby]: https://www.ruby-lang.org
[Bundler]: https://bundler.io
[starter workflows]: https://github.com/actions/starter-workflows/blob/main/pages/jekyll.yml

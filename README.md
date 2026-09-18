# SOMaR data format (draft)

Draft community standard for data formats used by the *Sensing the Ocean with Marine Radar* (SOMaR) community: NetCDF conventions for sharing and post-processing marine radar products at different processing levels, from raw radar recordings to derived geophysical variables. The formats follow the NetCDF Climate and Forecast (CF) conventions wherever possible and document the extensions SOMaR needs (for example, time-bounded local grids).

The specification is a [Jekyll] site using the [Just the Docs] theme, published at
<https://sensing-the-ocean-with-marine-radar.github.io/somar-format-draft>.
For more about the community, see the [SOMaR GitHub organization](https://github.com/sensing-the-ocean-with-marine-radar).

## Repository layout

| Path | Content |
| --- | --- |
| `index.md` | Home page / abstract |
| `contents/introduction/` | Scope, motivation, and document structure |
| `contents/metadata_attributes/` | Mandatory and optional global attributes, radar parameters, file naming, georeferencing |
| `contents/data_types/` | Level 0, Level 1 (polar raw data, regularized polar images, Cartesian images), and Level 2 products (gridded maps and images, trajectory wave spectra and parameters) |
| `contents/about/` | About the SOMaR community |
| `_config.yml`, `Gemfile` | Site and theme configuration |
| `.github/workflows/` | `ci.yml` builds the site on pushes and pull requests; `pages.yml` deploys it to GitHub Pages |

## Building the site locally

Requires [Ruby] (3.3 is used in CI) and [Bundler].

```sh
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. The built site is written to `_site/`.

## Editing the specification

- Pages are Markdown files. The front matter (`title`, `parent`, `nav_order`) determines the page's place in the navigation.
- Each data type has its own page under `contents/data_types/`, documenting its dimensions, variables, and attributes with a minimal CDL example. Attributes shared by all products belong in `contents/metadata_attributes/`.
- Please propose changes through issues or pull requests.

## License and attribution

This repository is licensed under the [MIT License](LICENSE). The site is based on the [just-the-docs template](https://github.com/just-the-docs/just-the-docs-template), and the deployment workflow is based on GitHub's [starter workflows].

[Jekyll]: https://jekyllrb.com
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[Ruby]: https://www.ruby-lang.org
[Bundler]: https://bundler.io
[starter workflows]: https://github.com/actions/starter-workflows/blob/main/pages/jekyll.yml

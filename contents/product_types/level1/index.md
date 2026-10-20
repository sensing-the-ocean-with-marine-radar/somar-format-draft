---
title: "Level 1: Radar data"
layout: default
parent: SOMaR product types
nav_order: 1
has_children: true
---

# Level 1: Radar data

Level 1 products contain the radar measurement itself, in the analog-to-digital converter units of the instrument and without geophysical interpretation.
They differ only in geometry: Level 1a data preserve the raw ray sequence in polar sensor coordinates ([polar radar "raw" data](level1a.md)), while Level 1b data organize individual antenna revolutions as images, either in polar coordinates with a regularized azimuth axis ([regularized polar images](level1b_polar.md)) or on a Cartesian grid centered on the platform ([Cartesian images](level1b_cartesian.md)).
Level 1b images are formed from revolutions and are not defined for data recorded in pointing mode, which exist at Level 1a only.
Level 1 files serve as the input for the Level 2 retrievals.

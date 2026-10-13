---
title: Level 1 data
layout: default
parent: SOMaR data types
#nav_order: 2
---

# Level 1 data

Level 1 products contain the radar measurement itself, in the analog-to-digital converter units of the instrument and without geophysical interpretation.
They differ only in geometry: Level 1a data preserve the raw pulse sequence in polar sensor coordinates ([polar radar "raw" data](level1a.md)), while Level 1b data organize individual antenna revolutions as images, either in polar coordinates with a regularized azimuth axis ([regularized polar images](level1b_polar.md)) or on a Cartesian grid centered on the platform ([Cartesian images](level1b_cartesian.md)).
Level 1 files serve as the input for the Level 2 retrievals.

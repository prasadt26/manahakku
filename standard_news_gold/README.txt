STANDARD NEWS — GOLD (optional add-on)
======================================

A single-theme Standard News poster with a cream-and-gold vertical header gradient
and the transparent Mana Hakku logo laid over it.

Palette:
  - Header background: cream/gold vertical gradient (#fef7d8 -> #fceeb5 -> #f0d4a0)
  - Header text (samachar patrika, date, location): deep navy #1e3a8a
  - Headline bar: dark navy gradient with gold accent strips
  - ID line: warm amber #b45309
  - Description body: dark #1e293b
  - Footer link, reporter: navy #1e3a8a
  - Border: gold-to-brown-to-gold gradient

Files:
  - standard_news_gold.html   The canvas poster generator.
  - README.txt                This file.

Logo used: ../Idi_Mana_Hakku_Logo_Transparent.png (at the repo root). app.py inlines
it as a base64 data URI via the shared transparent-logo injection block.

To COMPLETELY REMOVE this feature:
  1. Delete this entire "standard_news_gold" folder.
  2. In app.py, remove:
       a. The "✨ Standard News — Gold" entry from the poster_type radio list.
       b. The `elif poster_type == "✨ Standard News — Gold":` branch.

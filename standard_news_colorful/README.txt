STANDARD NEWS — COLORFUL (optional add-on)
==========================================

This folder holds a color-themed variant of the Standard News poster. Same layout as
poster_gem6.html, but the yellow header is replaced with a themed gradient, and every
element (header, headline bar, description, footer link, reporter, border) is repainted
from a THEME object. The control panel offers:

  - 3 preset color themes (click a card to apply): Ocean Teal, Royal Purple, Emerald Forest.
  - Custom color pickers under a collapsible section to override any individual element.
  - Live re-render on every theme click or picker change (after a photo is cropped).

Files:
  - standard_news_colorful.html   The canvas poster generator.
  - README.txt                    This file.

Logo used: ../logo-final1.png (the enhanced logo at the repo root). app.py inlines it
as a base64 data URI at serve time, matching the pattern used for logo.png and
breaking_news/Final_Logo.png.

To COMPLETELY REMOVE this feature:
  1. Delete this entire "standard_news_colorful" folder.
  2. In app.py, remove:
       a. The "🎨 Standard News — Colorful" entry from the poster_type radio list.
       b. The `elif poster_type == "🎨 Standard News — Colorful":` branch.
       c. The block that reads logo-final1.png and swaps the ../logo-final1.png src.
     The "# --- BREAKING NEWS FEATURE ---" boundaries and defaults above stay intact.

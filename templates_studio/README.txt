Mana Hakku — Multi-Template Poster Studio
=========================================

A standalone poster generator with a TEMPLATE SELECTOR. Fully separate from
poster_gem6.html and breaking_news/ so it cannot affect or crash them.

Open:  templates_studio/poster_studio.html  (double-click, or serve the folder)

Shared assets:
  - Uses the project logo via "../logo.png" (root of the repo).

Templates (switch with the cards at the top of the control panel):
  1. Classic    – bright yellow header + blue headline bar (matches house style)
  2. Bold Dark  – TV-news look, dark navy + gold frame + red BREAKING flag
  3. Magazine   – editorial layout, full-bleed hero photo, serif accents

Capabilities (same as the original, plus a Location field):
  - Photo upload + crop/rotate (Cropper.js)
  - Headline / Description with live character counters
  - Location + Date
  - Auto-fit text sizing so long copy always fits
  - Social footer (Facebook, Instagram, WhatsApp, YouTube, Web) -> /idimanahakku.in
  - Reporter credit
  - News ID (reads localStorage 'newsCounter')
  - Download high-res PNG (1500 x 2600)

Switching a template after cropping re-renders instantly with the same content.

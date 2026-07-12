BREAKING NEWS POSTER — optional add-on feature
================================================

This folder contains the "Breaking News" poster. It offers two styles you pick from
the "POSTER STYLE" option in the control panel (both: masthead + big image + full
headline only, no description body):
  - TV Lower-Third    : glossy red BREAKING ticker, image, headline in a navy band.
  - Full-Bleed Dramatic: photo fills the poster, headline sits large over a dark
                         scrim at the bottom, with a red BREAKING pill top-left.

Files:
  - breaking_news.html   The canvas poster generator for breaking news.
  - Final_Logo.png       The logo used ONLY by this design (independent of the main
                         app's logo.png).

To COMPLETELY REMOVE this feature:
  1. Delete this entire "breaking_news" folder.
  2. In app.py, delete the block marked between:
         # --- BREAKING NEWS FEATURE (delete this block to remove) ---
         ...
         # --- END BREAKING NEWS FEATURE ---
     The two default lines just above that block
         poster_file = "poster_gem6.html"
         logo_file = "logo.png"
     should stay — they keep the standard poster working on its own.

The app will then behave exactly as it did before.

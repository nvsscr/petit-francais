# Petit Français

A picture-and-voice app that helps a 3-year-old learn the French he needs at *école maternelle*. There is almost no text to read: he taps pictures, hears clear recorded voices, and plays short games.

## What's inside

- **Les 50 essentiels**: the 50 most useful phrases for a first year of maternelle.
  - **Je dis (20)**: what he needs to be able to say (Bonjour, J'ai soif, Je peux aller aux toilettes ?…)
  - **La maîtresse dit (20)**: what he needs to understand (Assieds-toi, Mets-toi en rang, Lave-toi les mains…)
  - **Mon école (10)**: people and things at school (la maîtresse, l'ATSEM, le doudou…)
- **Le grand jeu**: a quiz mixing all 50 phrases.
- **Bouge avec Poussin**: a movement game with 12 commands (Saute !, Tourne !, Danse !…).
- Each phrase has its own illustrated scene showing the same little boy, so the situation is clear at a glance.
- Two recorded voices: *Petit garçon* (the default) and *Maîtresse*. Switch between them in the **Parents** panel.
- The Parents panel also sets the speed, the number of pictures per question, and whether to show the written word.
- A playful animated background: Poussin the chick, a sun you can tap, and picture bubbles you can pop.

## Run it

It's a static site, so open `index.html` through any web server, for example:

```bash
python -m http.server 8765
```

Then go to http://localhost:8765. It also works on GitHub Pages: in Settings → Pages, deploy from the `main` branch.

## Files

| Path | What |
|---|---|
| `petit-francais.html` | The whole app (HTML, CSS and JS in one file). Phrases are in the `/*DATA*/` block. |
| `scene/` | Illustrated scenes, one per phrase (generated with ChatGPT, cropped to 400×400). |
| `img/` | Decoration and fallback pictures: [Microsoft Fluent Emoji](https://github.com/microsoft/fluentui-emoji), MIT licence. |
| `audio/boy/`, `audio/teacher/` | Recorded clips as JSON files mapping each phrase to a base64 MP3 (Microsoft Edge neural voices). |
| `tools/` | Scripts that rebuild the audio (`gen_audio.py`, needs `pip install edge-tts`), crop 2×2 image sheets (`crop_grid.py`, needs Pillow) and fetch Fluent pictures (`fetch-images.mjs`). |

## Add or change a phrase

1. Edit the item in the `/*DATA*/` block of `petit-francais.html`. The format is `["French text", "Fluent emoji name", "scene/file.jpg"]`.
2. Add a 400×400 picture in `scene/`.
3. Re-record the audio:

   ```bash
   python tools/gen_audio.py petit-francais.html audio
   ```

# Petit Français

A picture-and-voice app that helps a 3-year-old learn the French he needs at *école maternelle*. There is almost no text to read: he taps pictures, hears clear recorded voices, and plays short games.

## What's inside

- **Je dis (20)**: what he needs to be able to say (Bonjour, J'ai soif, Je peux aller aux toilettes ?…)
- **Avec les copains (13)**: playing with friends and feelings (Tu veux jouer avec moi ?, À mon tour !, Je suis triste…)
- **La maîtresse dit (20)**: what he needs to understand (Assieds-toi, Mets-toi en rang, Lave-toi les mains…)
- **En classe (12)**: more of the teacher's words (On chante !, Ferme les yeux, Mouche ton nez…)
- **Mon école (17)**: people, places and things at school (la maîtresse, l'ATSEM, la cour, le toboggan…)
- **Les couleurs (8)** and **Je compte (1–8)**
- **Le grand jeu**: a quiz mixing every phrase.
- **Bouge avec Poussin**: a movement game with 16 commands (Saute !, Tourne !, Vole comme un oiseau !…).
- Each phrase has its own illustrated scene showing the same little boy and the same maîtresse.
- **One voice, lots of noise:** every phrase is read by the same young voice. There's no spoken praise: right answers, wins, Poussin and the sun set off sound effects, confetti and a dancing chick instead.
- **Smart games:** each phrase remembers how well he knows it. Known phrases come back less often, mistakes come back 2 questions later, and the same phrase is never asked twice in a row (even across games).
- The Parents panel sets the speed, the number of pictures per question, and whether to show the written word.

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
| `audio/clips.json` | Every recorded clip: a JSON map from phrase to base64 MP3 (Microsoft Edge neural voices). |
| `tools/` | Scripts that rebuild the audio (`gen_audio.py`, needs `pip install edge-tts`), crop 2×2 image sheets (`crop_grid.py`, needs Pillow) and fetch Fluent pictures (`fetch-images.mjs`). |

## Add or change a phrase

1. Add the item to a category in the `/*DATA*/` block of `petit-francais.html`: `["French text", "", "scene/file.jpg"]`.
2. Add a 400×400 picture in `scene/`.
3. Re-record the audio:

   ```bash
   python tools/gen_audio.py petit-francais.html audio/clips.json
   ```

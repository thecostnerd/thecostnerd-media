# The Cost Nerd render tools

Renderers used to make the Instagram Reels, carousels and TikToks in `ig/`.

- `art.py`: flat illustration library (no brand logos). `ART` maps names to drawing functions.
- `reel2.py`: illustration-led Reels (1080x1920) and carousels (1080x1350) from a JSON script. `python3 reel2.py script.json outdir [slug]`
- `reel.py`: music bed generator (`music`, `write_wav`) used by `reel2.py`; original synthesized music, no samples.
- `render.py`: older text-only carousel renderer.
- `examples/`: the scripts behind the Nov 2026 posts. Copy one as a template.

Needs Python 3 with Pillow and NumPy, ffmpeg, Inter / Inter Display fonts (`/usr/share/fonts/opentype/inter/`) and DejaVu Sans Mono.
To add Kokoro narration: render, then mux the narration WAV over the video with the music bed ducked to about -18 dB.

## Long-form and Shorts from narration (added Nov 11, 2026)

`python3 longform.py <episode.py> <voice_dir> <out_dir> h|v` renders a narration-timed explainer: `h` = 1920x1080 long-form with chapter stings, music bed and a 14 s end-screen hold; `v` = 1080x1920 Short with the finished hook on frame 1. It also writes `<name>.srt` (digits, £/$ and % restored by `srtnum.py`; exact per-line fixes go in the episode file's `SRT` dict) and `<name>-meta.json` with chapter timestamps. Episode files define `LINES` (the Kokoro JSON), `SCENES`, optional `CHAPTERS`, `END`, `SRT`. Example: `examples/bonus-black-friday/`. Preview every scene first with a contact sheet; QC frames after rendering (counters, overlaps).

`thumbs.py`: thumbnail colourways `specs` (Cent Specs dark), `paper`, `red`, `yellow`. Highlighted text is dark on yellow, cream on red.

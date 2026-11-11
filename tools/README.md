# The Cost Nerd render tools

Renderers used to make the Instagram Reels, carousels and TikToks in `ig/`.

- `art.py`: flat illustration library (no brand logos). `ART` maps names to drawing functions.
- `reel2.py`: illustration-led Reels (1080x1920) and carousels (1080x1350) from a JSON script. `python3 reel2.py script.json outdir [slug]`
- `reel.py`: music bed generator (`music`, `write_wav`) used by `reel2.py`; original synthesized music, no samples.
- `render.py`: older text-only carousel renderer.
- `examples/`: the scripts behind the Nov 2026 posts. Copy one as a template.

Needs Python 3 with Pillow and NumPy, ffmpeg, Inter / Inter Display fonts (`/usr/share/fonts/opentype/inter/`) and DejaVu Sans Mono.
To add Kokoro narration: render, then mux the narration WAV over the video with the music bed ducked to about -18 dB.

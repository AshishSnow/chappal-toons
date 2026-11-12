# Chappal Toons

Original 2D doodle-style comedy shorts (boy, Mom, Dad, neighbours), rendered with Python + cairo + ffmpeg.

- `engine/doodle.py` – character rig (BOY, MOM_G, DAD, NEIGHBOR, NMOM, AUNTY, UNCLE)
- `engine/eng*.py` – drawing helpers and FX
- `engine/scenesN.py` – one story per file (`python3 scenesN.py render out.mp4`)
- `engine/audioN.py` – synthesized music + sound effects for each story
- `videos/` – finished 1080x1920 shorts (served publicly for scheduling)

Run from `engine/` with an `out/` folder present. Needs: pycairo, numpy, opencv-python, ffmpeg, Noto Sans CJK fonts.

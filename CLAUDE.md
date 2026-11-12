# Chappal Toons – hourly Shorts production guide

You are making one new original animated comedy Short per run for the Chappal Toons YouTube channel, then scheduling it via Metricool.

## Workflow (every run)
1. `cd engine && mkdir -p out` (run everything from `engine/`).
2. Install if missing: `pip install --break-system-packages pycairo numpy opencv-python-headless`; ffmpeg; fonts "Noto Sans CJK JP Black" (`apt-get install -y fonts-noto-cjk` if `fc-list | grep "CJK"` is empty).
3. Read `TOPICS.md`. Pick a NEW topic not in the list (see rules below). Append it to `TOPICS.md`.
4. Write `engine/scenesNN.py` (+ `engine/audioNN.py`), copying the structure of the latest scenes/audio file (e.g. `scenes11.py`, `audio11.py`): ~1050 frames (35 s) at 30 fps, 7 shots, `card()` captions, `label()` key-moment words, `cam()` camera moves, synced synth audio.
5. Render test frames first (`python3 scenesNN.py test ...`), make a contact sheet, LOOK at it, fix framing/overlaps, then `python3 audioNN.py && python3 scenesNN.py render out/<slug>.mp4`.
6. Copy the mp4 to `videos/<slug>.mp4`, commit (author "Claude"), `git pull --rebase` then push to `main`.
7. Schedule on Metricool (`createScheduledPost`): blogId **8048380** (brand "Chappal toon"), network youtube, type "short", privacy public, category COMEDY, madeForKids false, isAiGeneratedContent false, media = `https://raw.githubusercontent.com/AshishSnow/chappal-toons/main/videos/<slug>.mp4`, title ending with ` #shorts`, 6-8 tags, description 2-4 lines + ~7 hashtags. Time: the next free full hour (check `getScheduledPosts` for the brand so you never double-book an hour; posts with `draft: true` are old already-posted videos and do NOT count as booked), timezone Asia/Calcutta.

## Content rules
- Universal, global humour (US/UK/everyone). NOT India-specific: no Indian names, rupees, chappal-throwing as the main gag, bindi/kurta mom (use `doodle.MOM_G`). English captions only, plain and instantly clear.
- Original characters only (`doodle.BOY`, `MOM_G`, `DAD`, `NEIGHBOR`, `NMOM`, `UNCLE`/`AUNTY` in general outfits). Never draw or name copyrighted characters, brands, logos or real people. No other creators' audio/footage.
- Story shape: hook in first 3 s (visual + one clear caption, often a question/"WHEN I..."), 4-6 escalating beats, a twist, a punchline/loop ending.
- Style: clean flat doodle look, bold outlines, vibrant colours, varied camera (ECU, wide, low angle, push-in, split screen), screen shake on impacts, sound effect per moment, no emoji on screen, no persistent counters.
- Reels safe zone: nothing important in top 250 px, bottom 420 px, right 120 px, left 60 px. Text centred.
- Family-friendly; madeForKids stays false.
- Try something new each video (new set, new prop, new camera trick) – don't repeat the same structure.

## Topic ideas backlog (use, then move to TOPICS.md)
First day at the gym vs day 3 · Online shopping: expectation vs delivery · "5 more minutes" in bed · Dad trying to fix the Wi-Fi · Waiting for food delivery · Group project: who actually works · Kid vs vegetables at dinner · Last cookie in the jar · Mom says "we have food at home" · Parents vs new technology · Road trip "are we there yet?" · Monday morning vs Friday evening · Phone battery at 1% · Cleaning room: hiding everything in the closet · Diet starts tomorrow · Siblings fighting over the TV remote · Pretending to sleep when parents check · Exam: knew everything at home, blank in class · Homework eaten by the dog (cat) · New Year's resolutions by February · Grandma: "you look so thin, eat more"

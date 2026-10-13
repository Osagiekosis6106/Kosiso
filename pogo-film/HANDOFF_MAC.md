# Rebuild the Pogo 4K on the Mac (for a Claude session running on the Mac)

Why: the finished 4K (2.9 GB) was made in a cloud session that can't send files that large or create GitHub releases. Everything needed to rebuild it is in this repo on branch `claude/convair-pogo`.

Goal: save `Pogo_FINAL_4K.mp4` (and the 3 Shorts) in `~/Downloads/Hangar Physics/`.

## 1. Setup (macOS)
```
brew install ffmpeg python@3.12
brew install --cask font-inter font-dejavu font-liberation
python3 -m pip install numpy pillow
git clone https://github.com/Osagiekosis6106/Kosiso.git && cd Kosiso && git checkout claude/convair-pogo
```
**Fonts:** `pogo-film/gfx.py` and `pogo-film/gfx2.py` use Linux font paths (`/usr/share/fonts/...`). Point them at the Mac copies, usually `~/Library/Fonts/` (`InterDisplay-Bold.otf`, `InterDisplay-Black.otf`, `Inter-SemiBold.otf`, `Inter-Medium.otf`, `LiberationMono-Bold.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSansMono-Bold.ttf`). Find them with `find ~/Library/Fonts /Library/Fonts -name "Inter*"`.

## 2. Render the picture (in parallel chunks) and the sound
```
cd pogo-film
OUT=~/pogo_build; mkdir -p $OUT
N=8; for k in $(seq 0 $((N-1))); do python3 build12.py $OUT $k $N & done; wait
python3 audio12.py $OUT/audio
ls $OUT/v_*.mp4 | sort | sed "s/^/file '/; s/$/'/" > $OUT/list.txt
ffmpeg -f concat -safe 0 -i $OUT/list.txt -c copy $OUT/master_v.mp4
```
Check: `master_v.mp4` should have 17,050 frames (9:28.3 at 30 fps).

## 3. Encode the final files
```
ffmpeg -i $OUT/master_v.mp4 -i $OUT/audio/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v 11M -maxrate 14M -bufsize 22M -profile:v high -pix_fmt yuv420p -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart $OUT/Pogo_FINAL_1080p.mp4
mkdir -p ~/Downloads/"Hangar Physics"
ffmpeg -i $OUT/Pogo_FINAL_1080p.mp4 -vf "scale=3840:2160:flags=lanczos,unsharp=5:5:0.4:5:5:0" -c:v libx264 -preset medium -b:v 40M -maxrate 50M -bufsize 80M -profile:v high -level 5.1 -pix_fmt yuv420p -c:a copy -movflags +faststart ~/Downloads/"Hangar Physics"/Pogo_FINAL_4K.mp4
```
(On Apple Silicon, `-c:v hevc_videotoolbox -b:v 40M -tag:v hvc1` is much faster and YouTube accepts it.)

## 4. Shorts (optional: the user already has phone copies)
```
OUT13=$OUT   # make_shorts.py expects master_v.mp4 and audio/ here
python3 make_shorts.py $OUT13 stt ~/Downloads/"Hangar Physics"/Shorts
```

## 5. Also copy into `~/Downloads/Hangar Physics/`
`upload/Pogo_Thumbnail_A_channel_style.jpg`, `upload/Pogo_Thumbnail_B_premium_studio.jpg`, `upload/Pogo_subtitles_EN.srt`, `upload/Pogo_UPLOAD_PACK.md`.

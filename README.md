# osu! beater
osu! beater is a tool to play osu beatmaps with note sounds

# Install
1. Install ffplay and add it to PATH
2. `pip install requests`
3. `git clone https://github.com/MrCheatEugene/osubeater && cd osubeater` or clone this repo and navigate to folder with osu!beater
4. `python beater.py h` or `python3 beater.py h`

# Usage
```
Syntax: python beater.py MODE path/to/beatmap MAPID VOLUME HITSOUND SLIDERDELAY

Path to beatmap - full path to folder where .osu files are placed, along with the music.
Map ID - Number of .osu file to play
Hitsound - path to sound that will play when beater will hit the note (if you don't have any - use -1)
Volume - volume of music itself
Mode - p/h/l
Slider Delay - a delay between slider ticks. Use -1 to leave it for software, or -2 to disable slider sounds at all

p - Play music
h - Show help
l - List available .osu files
```

# Already-known issues
- Slider delay is buggy
- Only osu! original mode maps are supported

If you know how to fix these, please fork this repo, add your modifications and create a pull request! Thanks!

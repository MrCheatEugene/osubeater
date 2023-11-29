import os
import time
import threading
import subprocess
import sys
import requests

print("osu! beater\n\nA tool to play music from already-downloaded osu! maps, with hitsounds!\n\nSyntax: python beater.py MODE path/to/beatmap MAPID VOLUME HITSOUND SLIDERDELAY\n\nPath to beatmap - full path to folder where .osu files are placed, along with the music.\nMap ID - Number of .osu file to play\nHitsound - path to sound that will play when beater will hit the note (if you don't have any - use -1)\nVolume - volume of music itself\nMode - p/h/l\nSlider Delay - a delay between slider ticks. Use -1 to leave it for software, or -2 to disable slider sounds at all\n\np - Play music\nh - Show help\nl - List available .osu files\n\n")

args = sys.argv
if len(args)<7 or args[1] == 'h':
    os.abort()

sliderdelay = float(args[6])
hitsound = args[5]
volume = int(args[4])
mapid = int(args[3])
mapfolder = args[2]

files = os.listdir(mapfolder)
files1 = []
for file in files:
    if file.split('.')[-1] == 'osu':
        files1.append(file)

if args[1] == 'l':
    ll = 0
    for file in files1:
        print(f'{ll} - {file}')
        ll+=1
    os.abort()

if hitsound.strip() == '-1':
    if not os.path.exists('hitsound.wav'):
        with open('./hitsound.wav', 'wb+') as f:
            f.write(requests.get('http://up.ppy.sh/files/bass-dry.wav', stream=True).content)
    hitsound = os.path.join(os.getcwd(), 'hitsound.wav')
    print("WARN: No hitsound was provided - using the default one!")

os.system('taskkill /f /im ffplay.exe')
os.system('pkill ffplay')
def playsound(filepath, vol=100):
    subprocess.call(f'ffplay "{filepath}" -showmode 0 -autoexit -volume {vol} -loglevel quiet', stdout=subprocess.DEVNULL)

def playThreaded(filepath, vol=100):
    threading.Thread(target=playsound, args=[filepath, vol]).start()

targetFile = os.path.join(mapfolder, files1[mapid])
lines = ''
with open(targetFile, encoding='utf8') as f:
    lines = f.read()

diff = lines.split('[Difficulty]\n')[1].split('\n\n[Events]')[0].splitlines()
objects = lines.split('[HitObjects]\n')[1].split('\n\n')[0]
editor = lines.split('[Editor]\n')[1].split('\n\n')[0].splitlines()

mul = float(diff[4].split(':')[1])
tr = float(diff[5].split(':')[1])
bd = int(editor[2].split(': ')[1])
passedTime=0
beat = 0
combo = False
playThreaded(os.path.join(mapfolder, "audio.mp3"), volume)
for line in objects.splitlines():
    t = int(line.split(',')[2])
    type = int(line.split(',')[3])
    if line.count('|')>0:
        combo = True
    if combo and sliderdelay != -2:
        slides = int(line.split(',')[6])
        subt = passedTime
        ogsubt = passedTime
        while subt <= t:
            if sliderdelay == -1:
                subt+=(float(line.split(',')[7])*(tr+(mul/bd)))
            else:
                subt+=sliderdelay
            time.sleep(abs(passedTime-subt)/1000)
            playThreaded(hitsound)
            passedTime=subt
            beat+=1
            print(f"Total beats: {beat}")
        combo= False
        continue
    time.sleep(abs((passedTime-t)/1000))
    passedTime=t
    sound =  line.split(',')[4]
    playThreaded(hitsound)
    beat+=1
    print(f"Total beats: {beat}")

print("Done..")
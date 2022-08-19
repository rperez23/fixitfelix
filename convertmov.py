#! /usr/bin/python3

import sys
import re
import moviepy.editor as mp

parts = sys.argv[1].split('.')
pre = parts[0]
outf = pre + ".mp3"

my_clip = mp.VideoFileClip(sys.argv[1])

try:
    my_clip.audio.write_audiofile(outf)
except:
    sys.exit(1)
sys.exit(0)

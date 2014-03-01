#!/usr/bin/env python3
import sys
import hashlib
import re
import math
#from itertools import imap
#from itertools import izip
from itertools import count
from itertools import islice
import itertools
import wave
import struct

# Identitione

# I want to:
#  put this on github
#  make infinite seed generator
#  add option to select number of distinct sounds in an identitone

# Have a power of two (32) for the number of notes for perfectionism's sake
# It will take 5 bits to identify a random note from this list
used_notes = ["E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6"]
notes = {"C0": 16.35, "C#0": 17.32, "D0": 18.35, "D#0": 19.45, "E0": 20.60, "F0": 21.83, "F#0": 23.12, "G0": 24.50, "G#0": 25.96, "A0": 27.50, "A#0": 29.14, "B0": 30.87,
         "C1":32.70 , "C#1": 34.65, "D1": 36.71, "D#1": 38.89, "E1": 41.20, "F1": 43.65, "F#1": 46.25, "G1": 49.00, "G#1": 51.91, "A1": 55.00, "A#1": 58.27, "B1": 61.74,
         "C2": 65.41, "C#2": 69.30, "D2": 73.42, "D#2": 77.78, "E2": 82.41, "F2": 87.31, "F#2": 92.50, "G2": 98.00, "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
         "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56, "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00, "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,
         "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,
         # Anything below 400 doesn't play very well on my Galaxy S3 speaker
         "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99, "G#5": 830.61, "A5": 880.00, "A#5": 932.33, "B5": 987.77,
         "C6": 1046.50, "C#6": 1108.73, "D6": 1174.66, "D#6": 1244.51, "E6": 1318.51, "F6": 1396.91, "F#6": 1479.98, "G6": 1567.98, "G#6": 1661.22, "A6": 1760.00, "A#6": 1864.66, "B6": 1975.53,
         # The high notes can be piercing and unpleasant
         "C7": 2093.00, "C#7": 2217.46, "D7": 2349.32, "D#7": 2489.02, "E7": 2637.02, "F7": 2793.83, "F#7": 2959.96, "G7": 3135.96, "G#7": 3322.44, "A7": 3520.00, "A#7": 3729.31, "B7": 3951.07,
         "C8": 4186.01, "C#8": 4434.92, "D8": 4698.63, "D#8": 4978.03, "E8": 5274.04, "F8": 5587.65, "F#8": 5919.91, "G8": 6271.93, "G#8": 6644.88, "A8": 7040.00, "A#8": 7458.62, "B8": 7902.13}

sample_rate = 44100
seconds_per_sound = 1.5
num_sounds_to_play = 4
num_tones_in_sound = 4
email_regex = re.compile("\A[\w+\-.]+@([a-z\d\-]+\.)+[a-z]+\Z")
phone_regex = re.compile("\A(1[-_ ]?)?([0-9][0-9][0-9][-_ ]?)?([0-9][0-9][0-9][-_ ]?)([0-9][0-9][0-9][0-9])\Z")
phone_strip_list = ['-', '_', ' ']
def sine_wave(freq=440.00, rate=sample_rate, amp = 0.9):
    if amp > 1.0:
        amp = 1.0
    if amp < 0.0:
        amp = 0.0
    per = int(rate/freq)
    interval = [float(amp) * math.sin(2.0 * math.pi * float(freq) * (float(i % per)/float(rate)))
                for i in range(per)]
    return (interval[i%per] for i in count())

tones = {name: sine_wave(freq=val) for name, val in notes.items()}
# TODO: Check if it is an email or a phone number and then deal with it accordingly
# for emails trim leading and trailing whitespace and then convert to lowercase
def sound_from_value(unfiltered_string):
    filtered = None
    trimmed = unfiltered_string.strip()
    lower = trimmed.lower()
    if phone_regex.match(lower):
        print("It's a phone number")
        numeric = lower
        for char in phone_strip_list:
            numeric = numeric.replace(char, "")
        # TODO add a 1 if it is missing, or have it remove the 1 if it starts with a 1 (lstrip('1'))
        filtered = numeric
    elif email_regex.match(lower):
        print("It's an email")
        filtered = lower
    else:
        print("It's not an email or a phone number")
        filtered = lower
    return sound_from_identifier(filtered)

# This takes in a well formated unique identifier string with filters already applied to it (e.g. trimming whitespace, converting to lowercase, etc.)
def sound_from_identifier(unhashed_string):
    # TODO: handle case of when non-ascii characters are in the string, probably should just asciify the string
    hashhexdig = hashlib.sha512(unhashed_string.encode("ascii")).hexdigest()
    return sound_from_hash(hashhexdig)


def sound_def_from_hash(hashhexdig):
    """
    Takes a hex hash digest and produces a unique sound definition based on it
    """
    binarystr = bin(int(hashhexdig, base=16))[2:]
    # List of lists of tones to produce
    sounds_defs = []
    # Bits per tone
    bpt = math.ceil(math.log(len(used_notes), 2))
    for soundnum in range(0, num_sounds_to_play):
        sound_def = []
        for tonenum in range(0, num_tones_in_sound):
            initial_bit = bpt * (soundnum * num_tones_in_sound + tonenum)
            end_bit = initial_bit + bpt
            bitstr = binarystr[initial_bit:end_bit]
            intval = int(bitstr, base=2)
            tone = used_notes[intval]
            sound_def.append(tone)
        sounds_defs.append(sound_def)
    
    return sounds_defs

def def_to_tones(sound_def):
    """
    Takes a sound definition and returns a list of lists of tone generators for that definition
    """
    return [[tones[tone_name] for tone_name in sound] for sound in sound_def]

def sound_from_def(sound_def):
    """
    Takes a sound definition (list of list of notes) and creates the sound defined by it
    """
    # average the samples
    sounds = [map(lambda x: x / num_tones_in_sound, map(sum, zip(*sound))) for sound in sound_def]
    sound = []
    slice_size = int(seconds_per_sound * sample_rate)
    for snd in sounds:
        sound = sound + list(islice(snd, slice_size))
    return sound

def sound_from_hash(hashhexdig):
    """
    Takes a hex hash digest and produces a unique sound based on it
    """
    sound_def = sound_def_from_hash(hashhexdig)
    sound_tones = def_to_tones(sound_def)
    sound = sound_from_def(sound_tones)
    return sound

def duplicate_channels(sound):
    """
    Takes a single channel sound and makes it stereo
    """
    return [(x, x) for x in sound]

def write_sound_to_file(sound, filename="soundid.wav", nframes=None, nchannels=2, sampwidth=2, framerate=sample_rate):
    """
    Takes a sound an writes it to the specified file
    """
    # Make mono sound stereo
    sound = duplicate_channels(sound)
    if not nframes:
        nframes = len(sound)
    max_amp = float(int((2 ** (sampwidth * 8)) / 2) - 1)
    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))
    frames = b''.join(b''.join(struct.pack('h', int(max_amp * sample)) for sample in channels) for channels in sound)
    w.writeframesraw(frames)
    w.close()

msound = sound_from_value("blakem@example.com")
write_sound_to_file(msound)


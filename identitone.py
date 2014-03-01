#!/usr/bin/env python3
import sys
import hashlib
import re
import math
from itertools import count, islice, starmap
import itertools
import wave
import struct
import argparse

# Identitione

# Definitions:
# tone: collection of sounds that make an identifying audio bite i.e. an identitone
# sound: collection of notes, is a homogenous repeating waveform
# note: a single pitch, chosen from the used_notes list.
# tonedef: a tone definition, consisting of snddefs
# snddef: a sound definition, consisting of a list of notes

# First makes a tonedefgen, which is an infinite generator of snddefgens
# A snddefgen is an infinite generator that yields notes using the seeder
# Second it makes a tonegen, which is an infinite generator of sndgens
# A sndgen is an infinite generator of amplitudes made from the combined notes for that sound
# Then it uses the tonegen to make an actual tone, which is a list of numbers indicating the amplitude

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

email_regex = re.compile("\A[\w+\-.]+@([a-z\d\-]+\.)+[a-z]+\Z")
phone_regex = re.compile("\A(1[-_ ]?)?([0-9][0-9][0-9][-_ ]?)?([0-9][0-9][0-9][-_ ]?)([0-9][0-9][0-9][0-9])\Z")
phone_strip_list = ['-', '_', ' ']
def sine_wave(freq=440.00, rate=44100, amp = 0.9):
    if amp > 1.0:
        amp = 1.0
    if amp < 0.0:
        amp = 0.0
    per = int(rate/freq)
    interval = [float(amp) * math.sin(2.0 * math.pi * float(freq) * (float(i % per)/float(rate)))
                for i in range(per)]
    return (interval[i%per] for i in count())

#tones = {name: sine_wave(freq=val) for name, val in notes.items()}

# Filters an identifying string into a proper seed string
def seed_from_value(seedstr):
    filtered = None
    lower = seedstr.strip().lower()
    if phone_regex.match(lower):
        numeric = lower
        for char in phone_strip_list:
            numeric = numeric.replace(char, "")
        filtered = numeric.lstrip('1')
    elif email_regex.match(lower):
        filtered = lower
    else:
        filtered = lower
    return filtered

def hash_seed(seed):
    return hashlib.sha512(seed.encode("ascii")).hexdigest()

# Takes a hash and gives an infinite generator for making pseudorandom binary based on that hash
def make_seeder(hashdigest):
    seed = hashdigest
    for i in count():
        binseed = bin(int(seed, base=16))[2:]
        for char in binseed:
            yield char
        seed = hash_seed(seed)

# Generates a random int between nmin (inclusive) and nmax (exclusive)
def generate_int(seeder, nmax, nmin=0):
    bstr = [next(seeder) for i in range(math.ceil(math.log(nmax - nmin, 2)))]
    return int(''.join(bstr), base=2)

# Makes an infinite generator that yields notes from the seeder
def make_snddefgen(seeder):
    return (used_notes[generate_int(seeder, len(used_notes))] for i in count())

# Gives an infinite generator that yields snddefgens (sound definition generators)
def make_tonedefgen(seeder):
    return (make_snddefgen(seeder) for i in count())

def make_sndgen(snddefgen, numnotes, rate):
    notestrs = [next(snddefgen) for i in range(numnotes)]
    #print(notestrs)
    notenums = [notes[i] for i in notestrs]
    notegens = map(lambda x: sine_wave(x, rate), notenums)
    # Makes a generator of tuples of the zipped notegens, then maps that into the average of that tuple
    return map(lambda x: sum(x) / numnotes, zip(*notegens))

# Makes an infinite generator that yields sndgens (sound generators)
def make_tonegen(tonedefgen, numnotes, rate):
    return (make_sndgen(snddefgen, numnotes, rate) for snddefgen in tonedefgen)

# Makes an infinite generator that yields samples of the tone
def make_tone(tonegen, numsamples):
    for sndgen in tonegen:
        for sample in range(numsamples):
            yield next(sndgen)

# Takes a single channel sound and makes it stereo    
def duplicate_channels(sound):
    return map(lambda x: (x, x), sound)

def make_identitone(identifier, filename="identitone.wav", seconds=6, numnotes=4, sounds=4, rate=44100):
    sampwidth = 2
    nchannels = 2
    seed = seed_from_value(identifier)
    print("Seed value after filtering: " + seed)
    hashdigest = hash_seed(seed)
    print("Hash for seed is: " + hashdigest)
    seeder = make_seeder(hashdigest)
    tonedefgen = make_tonedefgen(seeder)
    tonegen = make_tonegen(tonedefgen, numnotes, rate)
    nframes = int(rate * seconds)
    samples_per_sound = int(rate * (seconds / sounds))
    tone = make_tone(tonegen, samples_per_sound)
    stereotone = islice(duplicate_channels(tone), nframes)
    max_amp = float(int((2 ** (sampwidth * 8)) / 2) - 1)
    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, rate, nframes, 'NONE', 'not compressed'))
    frames = b''.join(b''.join(struct.pack('h', int(max_amp * sample)) for sample in channels) for channels in stereotone)
    w.writeframesraw(frames)
    w.close()
    return tone

def main():
    time=6
    sounds=4
    notes=4
    rate=44100
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', help="Duration of identitone, default=" + str(time), default=time, type=float)
    parser.add_argument('-s', '--sounds', help="Number of distinct parts in an identitone, default=" + str(sounds), default=sounds, type=int)
    parser.add_argument('-n', '--notes', help="Number of notes in each part of the identitone, default=" + str(notes), default=notes, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz, default=" + str(rate), default=rate, type=int)
    parser.add_argument('seed', help="Seed string for creating the hash", type=str)
    parser.add_argument('filename', help="File to generate", type=str)

    args = parser.parse_args()

    make_identitone(args.seed, args.filename, args.time, args.notes, args.sounds, args.rate)

if __name__ == "__main__":
    main()


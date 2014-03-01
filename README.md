identitone
==========

Creates a unique sound based on a hash

## Description
Source code can be found on GitHub at [https://github.com/brainwater/identitone](https://github.com/brainwater/identitone)

Identitone uses the hash of the provided seed to create a unique identitone that should be easily distinguishable from other identitones. It uses the bits of the hash to choose which notes to play, and then creates a sequence of sounds that are each the combination of a few notes selected using the hash.

Requires python 3 to run.

This was inspired by identicons, which are an excelent way to give things a visual id.

## Usage
```
usage: identitone.py [-h] [-t TIME] [-s SOUNDS] [-n NOTES] [-r RATE]
                     seed filename

positional arguments:
  seed                  Seed string for creating the hash
  filename              File to generate

optional arguments:
  -h, --help            show this help message and exit
  -t TIME, --time TIME  Duration of identitone, default=6
  -s SOUNDS, --sounds SOUNDS
                        Number of distinct parts in an identitone, default=4
  -n NOTES, --notes NOTES
                        Number of notes in each part of the identitone,
                        default=4
  -r RATE, --rate RATE  Sample rate in Hz, default=44100
```

## Acknowledgements
I would like to thank [Zach Denton](https://github.com/zacharydenton) for his tutorial and code on using python to generate sound. I made extensive use of his techniques described on his site [Generate Audio with Python](http://zacharydenton.com/generate-audio-with-python/).

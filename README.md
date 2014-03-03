identitone
==========

Creates a unique sound based on a hash

## Description
Source code can be found on GitHub at [https://github.com/brainwater/identitone](https://github.com/brainwater/identitone)

Identitone uses the hash of the provided seed to create a unique identitone that should be easily distinguishable from other identitones. It uses the bits of the hash to choose which notes to play, and then creates a sequence of sounds that are each the combination of a few notes selected using the hash.

To hear an example identitone of the empty string, go to [http://identitone.herokuapp.com/identitone](http://identitone.herokuapp.com/identitone).

Requires python 3 to run the script.

Requires pip to install server dependencies, I suggest you use [virtualenv](http://www.virtualenv.org/en/latest/) so that you have an environment specific to this app. This is set up to run with gunicorn on heroku.

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

The server can be run locally with ```$ ./manage.py runserver```. The api for the server is the address ```/{256 character hexadecimal hash}``` for getting the identitone of a specific hash, or the address ```/identitone``` for getting the identitone of an arbitrary string. For getting the identitone of an arbitrary string, use the seed variable in the url, e.g. ```/identitone?seed=your_seed```. There are more variables you can use in the url, namely 'time' the identitone length in seconds, 'sounds' the number of distinct parts in the identitone, 'notes' the number of notes that makes up each sound, and 'rate' the sample rate of the wav file. An example url that will give you a 5 second long identitone with 10 distinct parts (sounds) and each part having 3 notes making each one up for the seed 'yourseed'  ```/identitone?seed=yourseed&time=5&sounds=10&notes=3```

The default values for the server requests are time=2, sounds=16, notes=1, and rate=44100. These values seem to give the best sounding identitone based on my testing, but if you find something that sounds better I would appreciate it if you could notify me.

## Acknowledgements
I would like to thank [Zach Denton](https://github.com/zacharydenton) for his tutorial and code on using python to generate sound. I made extensive use of his techniques described on his site [Generate Audio with Python](http://zacharydenton.com/generate-audio-with-python/).

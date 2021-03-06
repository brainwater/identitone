from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import identitone

def home(request):
    """
    Redirects to identitone github page
    """
    return HttpResponseRedirect("https://github.com/brainwater/identitone")

def get_identitone(request, seed_hash):
    """
    Generates an identitone as a wav file
    """
    response = HttpResponse(content_type='audio/wav')
    response['Content-Disposition'] = 'filename="identitone.wav"'
    time = 2
    sounds = 16
    notes = 1
    rate = 44100
    if 'time' in request.GET:
        time = float(request.GET['time'])
    if 'sounds' in request.GET:
        sounds = int(request.GET['sounds'])
    if 'notes' in request.GET:
        notes = int(request.GET['notes'])
    if 'rate' in request.GET:
        rate = request.GET['rate']
    identitone.write_identitone(seed_hash, response, time, notes, sounds, rate)
    return response

def get_raw_identitone(request):
    """
    Generates an identitone from a seed that isn't a hash
    """
    response = HttpResponse(content_type='audio/wav')
    response['Content-Disposition'] = 'filename="identitone.wav"'
    time = 2
    sounds = 16
    notes = 1
    rate = 44100
    if 'time' in request.GET:
        time = float(request.GET['time'])
    if 'sounds' in request.GET:
        sounds = int(request.GET['sounds'])
    if 'notes' in request.GET:
        notes = int(request.GET['notes'])
    if 'rate' in request.GET:
        rate = request.GET['rate']

    seed_string = ''
    if 'seed' in request.GET:
        seed_string = request.GET['seed']
    seed = identitone.seed_from_value(seed_string)
    seed_hash = identitone.hash_seed(seed)
    identitone.write_identitone(seed_hash, response, time, notes, sounds, rate)
    return response


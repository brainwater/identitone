from django.shortcuts import render
from django.http import HttpResponse
import identitone


def get_identitone(request, seed_hash):
    """
    Generates an identitone as a wav file
    """
    response = HttpResponse(content_type='audio/wav')
    time = 8
    sounds = 8
    notes = 4
    rate = 44100
    if 'time' in request.GET:
        time = request.GET['time']
    if 'sounds' in request.GET:
        sounds = request.GET['sounds']
    if 'notes' in request.GET:
        notes = request.GET['notes']
    if 'rate' in request.GET:
        rate = request.GET['rate']
    identitone.write_identitone(seed_hash, response, time, notes, sounds, rate)
    return response


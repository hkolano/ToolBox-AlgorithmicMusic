"""Synthesizes a blues solo algorithmically."""

import atexit
import os
from random import choice
from psonic import *

# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

BACKING_TRACK = os.path.join(SAMPLES_DIR, "backing.wav")
sample(BACKING_TRACK, amp=2)
sleep(2.25)  # delay the solo to match up with backing track

SAMPLE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch


def play_note(note, beats=1, bpm=60, amp=1):
    """Plays note for `beats` beats. Returns when done."""
    # `note` is this many half-steps higher than the sampled note
    half_steps = note - SAMPLE_NOTE
    # An octave higher is twice the frequency. There are twelve half-steps per octave. Ergo,
    # each half step is a twelth root of 2 (in equal temperament).
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_FILE)
    # Turn sample into an absolute path, since Sonic Pi is executing from a different working directory.
    sample(os.path.realpath(SAMPLE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)


def stop():
    """Stops all tracks."""
    msg = osc_message_builder.OscMessageBuilder(address='/stop-all-jobs')
    msg.add_arg('SONIC_PI_PYTHON')
    msg = msg.build()
    synthServer.client.send(msg)

atexit.register(stop)  # stop all tracks when the program exits normally or is interrupted

# These are the piano key numbers for a 3-octave blues scale in A. See: http://en.wikipedia.org/wiki/Blues_scale
blues_scale = [40, 43, 45, 46, 47, 50, 52, 55, 57, 58, 59, 62, 64, 67, 69, 70, 71, 74, 76]
beats_per_minute = 60				# Let's make a slow blues solo

curr_note = 0
play_note(blues_scale[curr_note], 0.5, beats_per_minute)
ascending_lick = [(1, 0.85), (1, 0.15), (1, 0.85), (1, 0.15)]
desc_lick = [(-1, 0.85), (-1, 0.15), (-1, 0.85), (-1, 0.15)]
arpeggio = [(2, 0.85), (2, 0.15), (2, 0.85), (-2, 0.15)]
blip = [(1, 0.85), (1, 0.15), (1, 0.85), (-1, 0.15)]
blip2 = [(-1, 0.85), (-1, 0.15), (-1, 0.85), (1, 0.15)]
vibrate = [(1, 0.85), (-1, 0.15), (1, 0.85), (-1, 0.15)]
bolero = [(1, 0.85), (-1, 0.15), (2, 0.85), (-2, 0.15)]
bolero2 = [(-1, 0.85), (1, 0.15), (-2, 0.85), (2, 0.15)]
jumpup = [(7, 0.85), (-1, 0.15), (1, 0.85), (-1, 0.15)]
jumpdown = [(-7, 0.85), (1, 0.15), (-1, 0.85), (1, 0.15)]
upwards_licks = [ascending_lick, arpeggio, blip, vibrate, bolero, jumpup]
down_licks = [desc_lick, bolero2, blip2, jumpdown]
lick_list = [ascending_lick, desc_lick, arpeggio, blip, vibrate, bolero, bolero2, blip2, jumpup, jumpdown]
for _ in range(4):
    if 0 <= curr_note <= 3:
        lick = random.choice(upwards_licks)
    elif 15 <= curr_note <= 18:
        lick = random.choice(down_licks)
    else:
        lick = random.choice(lick_list)
    for note in lick:
        print(curr_note)
        curr_note += note[0]
        play_note(blues_scale[curr_note], note[1], beats_per_minute)
# play_note(blues_scale[0], beats=1, bpm=beats_per_minute)

import numpy
import pygame
import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121B = adafruit_mpr121.MPR121(i2c)
mpr121A = adafruit_mpr121.MPR121(i2c, 0x5B)

sampleRate = 44100

pygame.mixer.init(44100, -16, 2, 512)

# Define note frequencies for 24 different notes (spanning multiple octaves)

note_frequencies= [103.83, 138.59, 185.0, 246.94, 311.13, 415.30, #0 fret
                   123.47, 164.81, 220.0, 293.66, 369.99, 493.88, #3rd fret
                   110.0, 146.83, 196.0, 261.63, 329.63, 440.0, #1st fret
                   466.16, 349.23 , 277.18 , 207.65 , 155.56, 116.54] #2nd fret


# Create sound arrays for each note
note_sounds = []
for freq in note_frequencies:
    arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * freq * x / sampleRate) for x in range(0, sampleRate)]).astype(numpy.int16)
    arr2 = numpy.c_[arr, arr]
    note_sounds.append(pygame.sndarray.make_sound(arr2))

# Initialize note states as "OFF" for all 24 notes
note_states = [False] * 24

while True:
    for i in range(24):
        if i < 12:
            if(i<6):
                pad_value = mpr121A[5-i].value
                pad_type = "Twizzler A"
            else:
                pad_value = mpr121A[i].value
                pad_type = "Twizzler A"
        else:
            
            pad_value = mpr121B[i - 12].value
            pad_type = "Twizzler B"

        if pad_value:
            if not note_states[i]:  # If the note is currently off
                print(f"{pad_type} {i} touched!")
                note_sounds[i].play(-1)
                note_states[i] = True
        else:
            if note_states[i]:  # If the note was on but the pad is released
                note_sounds[i].stop()
                note_states[i] = False

    time.sleep(0.01)  # Adjust the sleep time as needed
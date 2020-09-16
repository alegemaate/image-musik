#
# image-musik.py
# Script to convert images to midi music!
#
# Written by Allan Legemaate
# Github: @alegemaate
#
# License: MIT
#

"""This module is the entry point of Image Musik."""

from PIL import Image
from enum import Enum
from midiutil import MIDIFile
import sys


class Colour(Enum):
    """Enumerates channels for readability."""

    RED = 0
    GREEN = 1
    BLUE = 2


def map_sample_to_midi(sample):
    """Cut sample in half to bring 8 bit range to 7 bits."""
    return sample >> 1


def map_sample_to_duration(sample):
    """Map to 4 quantizations of notes."""
    return ((sample >> 6) + 1) / 4


def map_sample_to_volume(sample):
    """Map sample to 'volume' range."""
    return (sample >> 1) + 32


def generate_midi(notes, instrument, tempo, file_name):
    """Generate midi file from notes array."""
    track = 0
    channel = 0
    time = 0

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)
    MyMIDI.addProgramChange(track, channel, 0, instrument)

    duration_counter = 0

    for pitch, duration, volume in notes:
        MyMIDI.addNote(track, channel, pitch, time + duration_counter, duration, volume)
        duration_counter = duration_counter + duration

    with open(file_name + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


def read(band):
    """Read individual band from image."""
    output = []

    for colour in band:
        output.append(colour)

    return output


def open_image(file_name, instrument, tempo):
    """Open and process image."""
    # Open and resize image
    print("Reading and converting image " + file_name)
    image = Image.open(file_name)
    resized_image = image.resize((200, 200))
    rgb_image = resized_image.convert('RGB')

    # Split channels
    print("Splitting image channels")
    r_band = list(rgb_image.getdata(Colour.RED.value))
    g_band = list(rgb_image.getdata(Colour.GREEN.value))
    b_band = list(rgb_image.getdata(Colour.BLUE.value))

    # Read channels
    print("Reading image channels")
    r_output = read(r_band)
    g_output = read(g_band)
    b_output = read(b_band)

    # Create note array
    print("Setting up notes")

    notes = []
    num_samples = len(r_output)
    # We map the 3 channels to pitch duration and volume
    for index in range(0, num_samples):
        pitch = map_sample_to_midi(r_output[index])
        duration = map_sample_to_duration(g_output[index])
        volume = map_sample_to_volume(b_output[index])
        notes.append((pitch, duration, volume))

    # Kick off midi writer
    print("Outputting midi")
    generate_midi(notes, instrument, tempo, file_name)


def parse_int_parameter(value, low, high):
    """Parse system args and cast to int."""
    value = int(value)
    if value < low or value > high:
        raise "Invalid range"
    return value


def main():
    """Entry point, does parameter validation."""
    if len(sys.argv) != 4:
        # Ensure length of args correct before using
        print("Invalid argument list, please provide path to image, \
            an instrument (0-127) and a tempo (1-1000)")
        exit()

    # Alias args
    file = sys.argv[1]
    instrument = sys.argv[2]
    tempo = sys.argv[3]

    # Check instrument range
    try:
        instrument = parse_int_parameter(instrument, 0, 127)
    except Exception:
        print("Instrument must be a number in range (0-127)")
        exit()

    # Check tempo range
    try:
        tempo = parse_int_parameter(tempo, 1, 1000)
    except Exception:
        print("Tempo must be a number in range (1-1000)")
        exit()

    # Open image
    open_image(file, instrument, tempo)


# Start program
main()

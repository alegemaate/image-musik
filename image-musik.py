from PIL import Image, ImageFilter  
from enum import Enum
from midiutil import MIDIFile
import sys

class Colour(Enum):
  RED = 0
  GREEN = 1
  BLUE = 2

def map_sample_to_midi(sample):
  # Cut in half to bring 8 bit range to 7 bits
  return sample >> 1

def map_sample_to_duration(sample):
  # 1 represents smallest fraction
  # This function can map to 4 quantizations of notes
  return ((sample >> 6) + 1) / 4

def map_sample_to_volume(sample):
  # Make sample in 'volume' range
  return (sample >> 1) + 32

def generate_midi(notes, instrument, tempo, file_name):
  # Generate midi file!
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
  # Read band from image
  output = []

  for colour in band:
    output.append(colour)

  return output

def open_image(file_name, instrument, tempo):
  # Open and process image
  print("Reading and converting image " + file_name)
  image = Image.open(file_name)
  resized_image = image.resize((200, 200))
  rgb_image = resized_image.convert('RGB')

  print("Splitting image channels")
  r_band = list(rgb_image.getdata(Colour.RED.value))
  g_band = list(rgb_image.getdata(Colour.GREEN.value))
  b_band = list(rgb_image.getdata(Colour.BLUE.value))

  print("Reading image channels")
  r_output = read(r_band)
  g_output = read(g_band)
  b_output = read(b_band)

  print("Setting up notes")
  notes = []
  num_samples = len(r_output)

  # We map the 3 channels to pitch duration and volume
  for index in range(0, num_samples):
    pitch = map_sample_to_midi(r_output[index])
    duration = map_sample_to_duration(g_output[index])
    volume = map_sample_to_volume(b_output[index])
    notes.append((pitch, duration, volume))

  print("Outputting midi")
  generate_midi(notes, instrument, tempo, file_name)

# Parameter validation
def main():
  if len(sys.argv) != 4:
    # Ensure length of args correct before using
    print("Invalid argument list, please provide path to image, an instrument (0-127) and a tempo (1-1000)")
  else:
    # Alias args
    file = sys.argv[1]
    instrument = sys.argv[2]
    tempo = sys.argv[3]

    # Check instrument range
    try:
      instrument = int(instrument)
      if instrument < 0 or instrument > 127:
        raise "Invalid range" 
    except:
      print("Instrument must be a number in range (0-127)")
      exit()

    # Check tempo range
    try:
      tempo = int(tempo)
      if tempo < 1 or tempo > 1000:
        raise "Invalid range" 
    except:
      print("Tempo must be a number in range (1-1000)")
      exit()

    # Open image
    open_image(file, instrument, tempo)


# Start program
main()
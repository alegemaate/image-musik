# Image Musik

Note! This is still work in progress, expect a few bugs!

![Build Status](https://github.com/alegemaate/image-musik/workflows/flake8/badge.svg)

## Installation

Install the required dependencies using pip with the following command

```sh
pip install midiutil pillow
```

## Using

You can run the program with the following arguments

```
python image-musik <path to file> <instrument> <tempo>
```

### Path To File

A valid path to an image format supported by pillow.
For a list of these go [here](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)

### Instrument

A standard midi instrument in the range of 0-127
For a list of valid instruments go [here](https://en.wikipedia.org/wiki/General_MIDI#Program_change_events)

### Tempo

Tempo of the outputted track. Can be anywhere from 1 to 1000 bpm

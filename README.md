# Image Musik

![Flake8](https://github.com/alegemaate/image-musik/workflows/flake8/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/8b56ded2e30dd170b7e8/maintainability)](https://codeclimate.com/github/alegemaate/image-musik/maintainability)

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

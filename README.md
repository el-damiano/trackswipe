# Trackswipe

A thumb-friendly keyboard for the Steam Controller on Linux. Swipe comfortably
across the trackpads for fast typing thanks to letters being grouped in a 3x3
grid. Faster typing means more time for gaming :)

[demo.webm](https://github.com/user-attachments/assets/bb199a8d-d5dd-41a5-b968-6d1c78df7758)

## Motivation

While the default Steam client already provides a good on-screen keyboard, I
wanted something that:

- runs without the Steam client being open
- doesn't take up screen space
- is intuitive to use without seeing the on-screen-keyboard

*The chosen layout does involve a learning curve, but once I got used to it, I
found it to be  more comfortable and faster.*

## Usage

See [setup](#setup-and-contributing) on how to run it.

Layout chart below (watch the demo to see it in action):

```
    +-----+-----+-----+      +-----+-----+-----+
    |S    |  R  |    O|      |S    |  R  |    O|
    |  W  |  G  |  U  |      |  W  |  G  |  U  |
    |     |     |     |      |     |     |     |
    +-----+-----+-----+      +-----+-----+-----+
    |     |J Q B|  ↳  |      |     |J Q B|  ↳  |
    |N M  |K H P|  L A|      |N M  |K H P|  L A|
    |     |V X Y|⬅   _|      |     |V X Y|⬅   _|
    +-----+-----+-----+      +-----+-----+-----+
    |     |     |     |      |     |     |     |
    |  C  |. F /|  D  |      |  C  |. F /|  D  |
    |T    |, I Z|    E|      |T    |, I Z|    E|
    +-----+-----+-----+      +-----+-----+-----+

```

- *_ means Space bar*
- *↳ means Enter*
- *⬅ means Backspace*

## Setup and Contributing

```bash
git clone https://github.com/el-damiano/trackswipe
cd trackswipe

### Create a virtual environment and install requirements
python -m venv venv
source venv/bin/activate  # <--- needs to be sourced each time it's used
pip intall -r requirements.txt

python3 main.py
```

I relied on `pygame` to handle joystick input and `evdev` to interface with the
Linux input subsystem.

## Inspirations

The main inspirations were 2 Android keyboards, 12-Key Japanese input Gboard
and [Thumb-Key](https://github.com/dessalines/thumb-key), go check them out!

## Roadmap

Things to implement/consider:

- integrate with Steam Input!
- make it portable (Python was a bad idea haha)
- add more keys and modifiers
- research optimal layout utilizing more than just trackpads
- gestures (select text, delete entire words, copy pasting)
- design to be configurable
- on-screen visualization?
- uninterrupted text input while playing the game
- buffer that holds a message waiting to be sent
- Windows/Mac?

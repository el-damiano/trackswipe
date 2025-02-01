
[demo.webm](https://github.com/user-attachments/assets/bb199a8d-d5dd-41a5-b968-6d1c78df7758)

Just a simple proof of concept of how a more thumb-friendly keyboard would work
with the Steam Controller and Steam Deck. It's rough around the edges, but has
got great potential.

The main inspirations were the 12-Key Japanese input GBoard and this [great
Android keyboard project](https://github.com/dessalines/thumb-key), go check it
out!

The chosen layout does involve a learning curve, but once I got used to it on
my phone, I found it to be  more comfortable and I spent much less time typing.

The benefit for the Steam Controller is way less time spent on typing and more on gaming :)

Things to implement/consider:
- integrate with Steam Input!
- make it portable (Python was a bad idea haha)
- add more keys and modifiers
- research optimal layout utilizing more than just trackpads
- gestures (select text, delete entire words, copy pasting)
- design to be configurable
- GUI representation?
- uninterrupted text input while playing the game
- buffer that holds the not-yet-sent message

I relied on `pygame` to handle joystick input and `evdev` to interface with the
Linux input subsystem. It's fine for the scope I intended.

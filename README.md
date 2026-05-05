# Basics

Git clone the repository anywhere you want

```
git clone git@github.com:ITT-26/assignment-02-dsp-PatrickGraf99.git (works only for SSH)
```

Open up a terminal and navigate to the project folder

inside the project folder, set up a virtualenv if you do not want to use your system python

install all required packages 

```
pip install requirements.txt
```

And you are ready to go

# Important Notice

Launching from console behaves weirdly for me, launching from within PyCharm works perfectly fine which is why I'd 
recommend trying that if you have trouble

# Whistle Input

```
python ./whistle_input/main.py
```

runs the whistle selector, displaying twio rectangles. When the program recognizes upwards or downwards input the 
rectangle will turn green for 5 seconds. After 5 seconds, the program resets.
Unluckily the detection is very very janky and I could not get it to work properly.


# Karaoke

use 

```
python ./karaoke_game/game.py path/to/midi
```

two midi files, berge.mid and freude.mid are already in the karaoke_game dir. Once the window has opened up you can 
press Enter to start the game.



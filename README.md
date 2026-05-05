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

# Whistle Input

```
python3 ./whistle_input/main.py
```

runs the whistle selector, displaying twio rectangles. When the program recognizes upwards or downwards input the 
rectangle will turn green for 5 seconds. After 5 seconds, the program resets.
Unluckily the detection is very very janky and I could not get it to work properly.


# Karaoke



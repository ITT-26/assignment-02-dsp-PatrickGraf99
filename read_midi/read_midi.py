import mido
from mido import MidiFile

for msg in MidiFile('../karaoke_game/berge.mid').play():
    print(msg)

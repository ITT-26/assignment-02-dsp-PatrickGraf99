import mido
from mido import MidiFile
from pyqtgraph.exceptionHandling import handler


class MidiReader:

    def __init__(self, filename, handler):
        self.filename = filename
        self.handler = handler

    def play(self):
        for msg in MidiFile(self.filename).play():
            self.handler(msg.type, msg.note)




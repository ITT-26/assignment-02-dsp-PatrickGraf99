import pyglet
from mido import MidiFile
from pyglet import window, shapes
from pyglet.window import key
import threading
import argparse

from midi_reader import MidiReader
from pich_detector import PitchDetector

class Musigame:

    def __init__(self, file):
        self.score_label = None
        self.WINDOW_DIMENSIONS = (640, 480)

        self.currently_detected_freq = None

        self.score = 0

        

        self.freqs = []
        self.voice_points = []
        self.midi_points = []
        self.midinotes = []

        self.midi_reader = MidiReader(file, handler=self.midi_handler)

        self.voice_color = (255, 0, 0)
        self.midi_color = (0, 255, 0)

        self.gamestate = 'running'


        self.PITCH_DETECTOR = PitchDetector(handler=self.voice_input_handler)

    # Set frequency to the one that was last recorded
    def voice_input_handler(self, freq):
        pyglet.clock.schedule_once(self._update_graph, 0, freq)
        # very ugly synchronization attempt
        pyglet.clock.schedule_once(self._update_midi, 0)
        pyglet.clock.schedule_once(self._update_score, 0)

    def midi_handler(self, note_type, note):
        if note_type == 'note_on':
            print(f'Adding note {note} to list')
            self.midinotes.append(note)
        else:
            print(f'Removing note {note} from list')
            self.midinotes.remove(note)

    def _update_graph(self, dt, freq):
        if self.gamestate == 'paused':
            return
        self.currently_detected_freq = freq
        self.freqs.append(freq)

        for point in self.voice_points:
            point.x -= 2

        # Remove points outside of screen
        self.voice_points = [p for p in self.voice_points if p.x > 0]

        self.voice_points.append(shapes.Rectangle(
            self.WINDOW_DIMENSIONS[0],
            freq / 10,
            1,
            1,
            (255, 0, 0)
        ))

    def _update_midi(self, dt):
        if self.gamestate == 'paused':
            return

        for point in self.midi_points:
            point.x -= 2

        self.midi_points = [m for m in self.midi_points if m.x > 0]

        for note in self.midinotes:
            freq = self.midi_to_freq(note)
            self.midi_points.append(shapes.Rectangle(
                self.WINDOW_DIMENSIONS[0],
                freq / 10,
                1,
                1,
                (0, 255, 0)
            ))

    def _update_score(self, dt):
        # Calc difference between last midi and voice point
        try:
            last_voice = self.voice_points[-1]
            last_midi = self.midi_points[-1]
            diff = abs(last_voice.y - last_midi.y)
            # if freqs are more than 100hz apart -> no points
            points = 100 - diff if diff > 0 else 0

            self.score += points
            self.score = int(self.score)
            self.score_label.text = f'Score: {self.score:d}'
            print(f'Score: {self.score}')
        except Exception:
            pass

    def midi_to_freq(self, note):
        return 440 * (2 ** ((note - 69) / 12))

    def draw_voice(self):
        for point in self.voice_points:
            point.draw()

    def draw_midi(self):
        for point in self.midi_points:
            point.draw()

    def start(self):
        win = window.Window(self.WINDOW_DIMENSIONS[0], self.WINDOW_DIMENSIONS[1])

        self.score_label = pyglet.text.Label(
            text=f'Score: {self.score}',
            x=50,
            y=(self.WINDOW_DIMENSIONS[1] - 20),
            anchor_x='left',
            anchor_y='top',
            font_size=16,
            color=(255, 255, 255)
        )

        @win.event
        def on_draw():
            win.clear()
            self.draw_voice()
            self.draw_midi()
            self.score_label.draw()

        @win.event
        def on_key_press(symbol, modifiers):
            if symbol == key.SPACE:
                self.gamestate = 'paused' if self.gamestate != 'paused' else 'running'
            if symbol == key.ENTER:
                self.gameloop_start()

        pyglet.app.run()


    def gameloop_start(self):
        self.PITCH_DETECTOR.start('freq')
        threading.Thread(target=self.midi_reader.play, daemon=True).start()
        # Missing: Play Midi music to sing along




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Karaoke Game")

    parser.add_argument(
        "midi_file",
        type=str,
        help="Path to the MIDI file to play"
    )

    args = parser.parse_args()

    game = Musigame(args.midi_file)
    game.start()
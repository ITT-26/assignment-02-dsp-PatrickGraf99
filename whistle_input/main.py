import pyglet
from pyglet import window, shapes
from whistle_input.pich_detector import PitchDetector

class VoiceSelector:

    def __init__(self):
        self.WINDOW_DIMENSIONS = (640, 480)
        self.RECT_COLOR = (255, 0 , 0)
        self.RECT_BORDER_SIZE = 20
        self.RECT_DIMENSIONS = (600, 200)

        self.upper_rectangle = None
        self.lower_rectangle = None

        self.PITCH_DETECTOR = PitchDetector(handler=self.voice_input_handler)
        self.is_on_cooldown = False

    def voice_input_handler(self, state):
        if state == "UP":
            self.color_with_cooldown(True)
        elif state == "DOWN":
            self.color_with_cooldown(False)

    def start(self):
        win = window.Window(self.WINDOW_DIMENSIONS[0], self.WINDOW_DIMENSIONS[1])
        self.upper_rectangle = shapes.Rectangle(20, 20, self.RECT_DIMENSIONS[0], self.RECT_DIMENSIONS[1], self.RECT_COLOR)
        self.lower_rectangle = shapes.Rectangle(20, 260, self.RECT_DIMENSIONS[0], self.RECT_DIMENSIONS[1], self.RECT_COLOR)

        @win.event
        def on_draw():
            win.clear()
            self.upper_rectangle.draw()
            self.lower_rectangle.draw()

        self.PITCH_DETECTOR.start('trend')

        pyglet.app.run()

    def color_with_cooldown(self, upper):
        if self.is_on_cooldown:
            return

        self.is_on_cooldown = True
        if upper:
            self.upper_rectangle.color = (0, 255, 0)
        else:
            self.lower_rectangle.color = (0, 255, 0)

        # Reset after 5 seconds
        pyglet.clock.schedule_once(self.reset_colors, 5.0)

    def reset_colors(self, dt):
        self.is_on_cooldown = False
        self.upper_rectangle.color = (255, 0, 0)
        self.lower_rectangle.color = (255, 0, 0)


voice_selector = VoiceSelector()
voice_selector.start()
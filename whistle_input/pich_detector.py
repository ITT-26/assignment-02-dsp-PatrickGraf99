# Used chatGPT to rewirte the audio_ample as a class

import sounddevice as sd
import numpy as np
import pyqtgraph as pg


class PitchDetector:
    def __init__(self, handler):
        # Audio settings
        self.stream = None
        self.CHUNK_SIZE = 1024
        self.RATE = 44100
        self.CHANNELS = 1

        # Smoothing
        self.smoothed_freq = None
        self.SMOOTHING = 0.2

        # State tracking
        self.last_freqs = []
        self.last_state = None

        # External handler (callback)
        self.handler = handler

        # Select input device
        self.input_device = self.select_input_device()

        # Setup UI
        #self.app = pg.mkQApp("Audio Visualizer")
        #self.win = pg.GraphicsLayoutWidget(title="Live Audio")
        #self.plot = self.win.addPlot()
        #self.plot.setYRange(-1, 1)
        #self.curve = self.plot.plot(pen='w')
        #self.win.show()

    def select_input_device(self):
        print("Available input devices:\n")
        devices = sd.query_devices()

        input_devices = []
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                print(f"{i}: {dev['name']}")
                input_devices.append(i)

        return int(input("\nSelect input device: "))

    def get_dominant_freq(self, data):
        windowed = data * np.hanning(len(data))

        fft = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(len(windowed), 1 / self.RATE)

        magnitude = np.abs(fft)

        idx = np.argmax(magnitude[10:]) + 10
        return freqs[idx]

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)

        data = indata[:, 0]
        #self.curve.setData(data)

        freq = self.get_dominant_freq(data)

        # smoothing
        if self.smoothed_freq is None:
            self.smoothed_freq = freq
        else:
            self.smoothed_freq = (
                self.SMOOTHING * freq +
                (1 - self.SMOOTHING) * self.smoothed_freq
            )

        self.last_freqs.append(self.smoothed_freq)

        # analyze last values
        relevant_freqs = self.last_freqs[-10:]

        if len(relevant_freqs) < 10:
            return

        freqs = np.array(relevant_freqs)

        diffs = np.diff(freqs)
        consistency = np.mean(np.sign(diffs))

        x = np.arange(len(freqs))
        slope = np.polyfit(x, freqs, 1)[0]

        state = "Stable"

        if slope > 5 and consistency > 0.6:
            state = "UP"
        elif slope < -5 and consistency < -0.6:
            state = "DOWN"

        if state != self.last_state:
            # USed for debugging
            # print(state)
            self.last_state = state

            # call external handler
            if self.handler:
                self.handler(state)

    def audio_callback_freq(self, indata, frames, time, status):
        if status:
            print(status)

        data = indata[:, 0]
        #self.curve.setData(data)

        freq = self.get_dominant_freq(data)

        # smoothing
        if self.smoothed_freq is None:
            self.smoothed_freq = freq
        else:
            self.smoothed_freq = (
                self.SMOOTHING * freq +
                (1 - self.SMOOTHING) * self.smoothed_freq
            )

        if self.handler:
            self.handler(self.smoothed_freq)

    def start(self, mode='trend'):
        if mode == "trend":
            self.stream = sd.InputStream(
                device=self.input_device,
                channels=self.CHANNELS,
                samplerate=self.RATE,
                blocksize=self.CHUNK_SIZE,
                callback=self.audio_callback,
                latency='low'
            )
        else:
            self.stream = sd.InputStream(
                device=self.input_device,
                channels=self.CHANNELS,
                samplerate=self.RATE,
                blocksize=self.CHUNK_SIZE,
                callback=self.audio_callback_freq,
                latency='low'
            )

        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()


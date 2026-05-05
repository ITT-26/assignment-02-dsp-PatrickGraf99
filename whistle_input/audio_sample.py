import sounddevice as sd
import numpy as np
import pyqtgraph as pg


# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024 # Number of audio frames per buffer
RATE = 44100 # Audio sampling rate (HZ)
CHANNELS = 1 # Mono audio

smoothed_freq = None
SMOOTHING = 0.2  # 0.1 = very smooth, 0.3 = more responsive

# print info about audio devices
print("Available input devices:\n")
devices = sd.query_devices()

input_devices = []
for i, dev in enumerate(devices):
    if dev['max_input_channels'] > 0:
        print(f"{i}: {dev['name']}")
        input_devices.append(i)

# let user select audio device
input_device = int(input("\nSelect input device: "))


# set up interactive plot
app = pg.mkQApp("Audio Visualizer")

win = pg.GraphicsLayoutWidget(title="Live Audio")
plot = win.addPlot()
plot.setYRange(-1, 1)

curve = plot.plot(pen='w')

win.show()

last_freqs = []

def get_dominant_freq(data, rate):
    # vibe coded
    # Do some transforms to get the dominant frequency
    windowed = data * np.hanning(len(data))

    fft = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(len(windowed), 1 / rate)

    magnitude = np.abs(fft)


    idx = np.argmax(magnitude[10:]) + 10
    return freqs[idx]


last_state = None

# audio callback to safe data
def audio_callback(indata, frames, time, status, handler):
    if status:
        print(status)


    data = indata[:, 0]  # mono
    curve.setData(data)

    # This right here was really me
    global smoothed_freq

    freq = get_dominant_freq(data, RATE)

    if smoothed_freq is None:
        smoothed_freq = freq
    else:
        smoothed_freq = SMOOTHING * freq + (1 - SMOOTHING) * smoothed_freq

    last_freqs.append(smoothed_freq)

    #print(f"Frequency: {freq:.1f} Hz")

    # Look at the last 10 freqs
    relevant_freqs = last_freqs[-10:]

    if len(relevant_freqs) < 10:
        return

    # Vibe coded
    freqs = np.array(relevant_freqs)
    diffs = np.diff(freqs)
    consistency = np.mean(np.sign(diffs))

    # Slope regression

    # create x-axis (time steps)
    x = np.arange(len(freqs))

    # slope of best-fit line
    slope = np.polyfit(x, freqs, 1)[0]

    state = "Stable"

    if slope > 5 and consistency > 0.6:
        state = "UP"
    elif slope < -5 and consistency < -0.6:
        state = "DOWN"

    global last_state
    if state != last_state:
        print(state)
        last_state = state
        handler.get(state)


# open audio input stream
stream = sd.InputStream(
    device=input_device,
    channels=CHANNELS,
    samplerate=RATE,
    blocksize=CHUNK_SIZE,
    callback=audio_callback,
    latency='low'
)


# continously capture and plot audio signal
with stream:
    print("\nStreaming... (Ctrl+C to stop)")
    pg.exec()
import numpy as np
import sounddevice as sd

# Set up parameters
fs = 44100
duration = 1
update_frequency = 1000  # Hz
update_duration = 0.1  # seconds

# Calculate frequency range for detection
min_frequency = update_frequency - 100
max_frequency = update_frequency + 100

while True:
    print("Hören Sie zu...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
    recording = np.array(recording).flatten()

    # Detect frequencies in range
    fft = np.fft.fft(recording)
    frequencies = np.fft.fftfreq(len(fft), 1 / fs)
    detected_frequencies = [int(round(freq)) for freq in frequencies[(min_frequency <= np.abs(frequencies)) & (np.abs(frequencies) <= max_frequency) & (np.abs(fft) > 5000)]]

    # Check if update tone was detected
    if update_frequency in detected_frequencies:
        binary_value = ""
        for i in range(1, 8):
            if (update_frequency * i) in detected_frequencies:
                binary_value += "1"
            else:
                binary_value += "0"
        decimal_number = int(binary_value, 2)
        decoded_char = chr(decimal_number)
        print("Empfangen:", decoded_char)

    # Wait for update tone to finish
    sd.wait(int(update_duration * fs))

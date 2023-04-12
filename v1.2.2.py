import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

fs = 44100
duration = 1

while True:
    input_value = input("Bitte geben Sie einen String aus Buchstaben und/oder Zahlen zwischen 0 und 127 ein (oder 'q' zum Beenden): ")
    if input_value == 'q':
        break
    for char in input_value:
        binary_result = ""
        waveforms = []
        if char.isdigit():
            decimal_number = int(char)
        else:
            decimal_number = ord(char)
        binary_value = bin(decimal_number)[2:].zfill(7)
        binary_result += binary_value + "\n"
        frequencies = [(i + 1) * 1000 for i, bit in enumerate(binary_value) if bit == '1']
        if frequencies:
            t = np.linspace(0, duration, int(fs * duration), False)
            waveforms = [np.sin(2 * np.pi * frequency * t) for frequency in frequencies]
        if waveforms:
            waveform = np.sum(waveforms, axis=0)
            sd.play(waveform, fs, blocking=True)
            #plt.specgram(waveform, Fs=fs)
            #plt.show()
        print("Die 7-Bit-Binärzahl für", char, "lautet:\n" + binary_result)

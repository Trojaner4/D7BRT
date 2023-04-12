import numpy as np
import sounddevice as sd

fs = 44100
duration = 1

#while True:
 #   input_value = input("Bitte geben Sie einen String aus Buchstaben und/oder Zahlen zwischen 0 und 127 ein (oder 'q' zum Beenden): ")
  #  if input_value == 'q':
  ##      break
   # for char in input_value:
   #     binary_result = ""
   #     waveforms = []
   #     if char.isdigit():
   ##         decimal_number = int(char)
   #     else:
   #         decimal_number = ord(char)
    #    binary_value = bin(decimal_number)[2:].zfill(7)
     #   binary_result += binary_value + "\n"
      #  frequencies = [(i + 1) * 1000 for i, bit in enumerate(binary_value) if bit == '1']
       # if frequencies:
        #    t = np.linspace(0, duration, int(fs * duration), False)
         #   waveforms = [np.sin(2 * np.pi * frequency * t) for frequency in frequencies]#
 #       if waveforms:
#            waveform = np.sum(waveforms, axis=0)
  #          sd.play(waveform, fs, blocking=True)
    #        #plt.specgram(waveform, Fs=fs)
 #  #         #plt.show()
  #      print("Die 7-Bit-Binärzahl für", char, "lautet:\n" + binary_result)

# Empfangen und Decodieren
while True:
    print("Hören Sie zu...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
    recording = np.array(recording).flatten()
    fft = np.fft.fft(recording)
    frequencies = np.fft.fftfreq(len(fft), 1 / fs)
    detected_frequencies = [int(round(freq)) for freq in frequencies[np.abs(fft) > 5000]]
    binary_value = ""
    for i in range(1, 8):
        if i * 1000 in detected_frequencies:
            binary_value += "1"
        else:
            binary_value += "0"
    decimal_number = int(binary_value, 2)
    decoded_char = chr(decimal_number)
    print("Empfangen:", decoded_char)

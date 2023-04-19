# Copyright 2023: Jan Joshua Laub, Rajan Zhabjaku

import sounddevice as sd
import numpy as np
import tkinter as tk

fs = 44100
duration = 1

def toggle_dark_mode():
    if root.cget('bg') == 'white':
        root.config(bg='black')
        label.config(bg='black', fg='white')
        button.config(bg='white', fg='black', activebackground='white', activeforeground='black')
        option_menu.config(bg='black', fg='white', activebackground='white', activeforeground='black')
        volume_scale.config(bg='black', fg='white')
    else:
        root.config(bg='white')
        label.config(bg='white', fg='black')
        button.config(bg='black', fg='white', activebackground='black', activeforeground='white')
        option_menu.config(bg='white', fg='black', activebackground='black', activeforeground='white')
        volume_scale.config(bg='white', fg='black')

def play_sound():
    input_value = text_entry.get()
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
            volume = volume_scale.get() / 100.0
            sd.play(waveform * volume, fs, blocking=True, device=selected_device.get())
        print("Die 7-Bit-Binärzahl für", char, "lautet:\n" + binary_result)
    text_entry.delete(0, 'end')

root = tk.Tk()
root.config(bg='white')

label = tk.Label(root, text="Text eingeben:")
label.config(bg='white', fg='black', font=('Helvetica', 16))
label.pack(pady=20)

text_entry = tk.Entry(root, width=40)
text_entry.config(font=('Helvetica', 14))
text_entry.pack(pady=10)

play_button = tk.Button(root, text="Play Sound", command=play_sound)
play_button.config(bg='black', fg='white', font=('Helvetica', 12), activebackground='black', activeforeground='white')
play_button.pack(pady=10)

devices = sd.query_devices()
device_names = [d['name'] for d in devices]
selected_device = tk.StringVar(root)
selected_device.set(device_names[0])
option_menu = tk.OptionMenu(root, selected_device, *device_names)
option_menu.config(bg='white', fg='black', font=('Helvetica', 12))
option_menu.pack(pady=10)

volume_scale = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Volume', length=300)
volume_scale.config(font=('Helvetica', 12), bg='white', fg='black')
volume_scale.pack(pady=10)
button = tk.Button(root, text="Dark Mode", command=toggle_dark_mode)
button.config(bg='black', fg='white', font=('Helvetica', 12), activebackground='black', activeforeground='white')
button.pack()
def on_slider_move(value):
    volume = float(value) / 100.0
    sd.default.device.volume = volume
root.mainloop()

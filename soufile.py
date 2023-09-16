import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def generate_waveform(wave_type, frequency, duration_ms, sample_rate=44100):
    num_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, num_samples, endpoint=False)
    
    if wave_type == "Sine":
        waveform = np.sin(2 * np.pi * frequency * t)
    elif wave_type == "Square":
        waveform = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == "Triangle":
        waveform = 2 * np.abs(2 * (frequency * t - np.floor(0.5 + frequency * t))) - 1
    else:
        raise ValueError("Invalid wave type")

    return waveform

def generate_and_save_wave():
    try:
        wave_type = wave_type_var.get()
        frequency = float(freq_entry.get())
        duration_ms = int(duration_entry.get())

        # Open a file dialog to select the save directory and file name
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

        if not output_file:
            return  # User canceled the save dialog

        waveform = generate_waveform(wave_type, frequency, duration_ms)

        sf.write(output_file, waveform, 44100, 'PCM_24')

        result_label.config(text=f"{wave_type} wave with {frequency} Hz saved as {output_file}")
    except ValueError as e:
        result_label.config(text=str(e))

# Create the main window
root = tk.Tk()
root.title("Waveform Generator")

# Create and layout widgets
frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

wave_type_label = ttk.Label(frame, text="Select Wave Type:")
wave_type_label.grid(column=0, row=0, sticky=tk.W)

wave_type_options = ["Sine", "Square", "Triangle"]
wave_type_var = tk.StringVar(value=wave_type_options[0])

wave_type_dropdown = ttk.Combobox(frame, textvariable=wave_type_var, values=wave_type_options)
wave_type_dropdown.grid(column=1, row=0)

freq_label = ttk.Label(frame, text="Frequency (Hz):")
freq_label.grid(column=0, row=1, sticky=tk.W)

freq_entry = ttk.Entry(frame)
freq_entry.grid(column=1, row=1)

duration_label = ttk.Label(frame, text="Duration (ms):")
duration_label.grid(column=0, row=2, sticky=tk.W)

duration_entry = ttk.Entry(frame)
duration_entry.grid(column=1, row=2)

generate_button = ttk.Button(frame, text="Generate and Save", command=generate_and_save_wave)
generate_button.grid(column=0, row=3, columnspan=2)

result_label = ttk.Label(frame, text="")
result_label.grid(column=0, row=4, columnspan=2)

# Start the tkinter main loop
root.mainloop()

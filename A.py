import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, filedialog

class AudioToImage:
    def __init__(self, root):
        self.root = root
        self.root.title('Audio to Image')

        self.audio_file = tk.StringVar()
        self.image_file = tk.StringVar()
        self.fft_size = tk.StringVar()
        self.overlap = tk.StringVar()
        self.window = tk.StringVar()
        self.color_map = tk.StringVar()

        self.audio_file.set('')
        self.image_file.set('output_image.png')
        self.fft_size.set('2048')
        self.overlap.set('0.5')
        self.window.set('hann')
        self.color_map.set('inferno')

        self.create_widgets()

    def create_widgets(self):
        # Create input frames
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill='x')

        tk.Label(input_frame, text='Audio File').pack(side='left')
        tk.Entry(input_frame, textvariable=self.audio_file).pack(side='left')
        tk.Button(input_frame, text='Browse', command=self.browse_audio_file).pack(side='left')

        # Create options frames
        options_frame = tk.Frame(self.root)
        options_frame.pack(fill='x')

        tk.Label(options_frame, text='FFT Size').pack(side='left')
        fft_size_option = tk.OptionMenu(options_frame, self.fft_size, '256', '512', '1024', '2048')
        fft_size_option.pack(side='left')

        tk.Label(options_frame, text='Overlap').pack(side='left')
        overlap_option = tk.OptionMenu(options_frame, self.overlap, '0.25', '0.5', '0.75')
        overlap_option.pack(side='left')

        tk.Label(options_frame, text='Window').pack(side='left')
        window_option = tk.OptionMenu(options_frame, self.window, 'hann', 'hamming', 'blackman')
        window_option.pack(side='left')

        tk.Label(options_frame, text='Color Map').pack(side='left')
        color_map_option = tk.OptionMenu(options_frame, self.color_map, 'inferno', 'viridis', 'plasma')
        color_map_option.pack(side='left')

        # Create button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill='x')

        tk.Button(button_frame, text='Convert', command=self.convert_audio).pack(side='left')
        tk.Button(button_frame, text='Export', command=self.export_image).pack(side='left')

        # Create plot frame
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill='both', expand=True)

    def browse_audio_file(self):
        filename = filedialog.askopenfilename(filetypes=[('WAV Files', '*.wav')])
        self.audio_file.set(filename)

    def convert_audio(self):
        # Read the audio file
        sample_rate, samples = wavfile.read(self.audio_file.get())

        # Generate a spectrogram
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg=int(self.fft_size.get()), noverlap=int(int(self.fft_size.get())*float(self.overlap.get())), window=self.window.get())

        # Plot the spectrogram
        self.figure = Figure()
        axis = self.figure.add_subplot(111)
        axis.imshow(spectrogram, aspect='auto', cmap=self.color_map.get(), origin='lower')
        axis.set_title('Spectrogram')
        axis.set_ylabel('Frequency')
        axis.set_xlabel('Time')

        # Display the plot
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def export_image(self):
        self.figure.savefig(self.image_file.get())

root = tk.Tk()
app = AudioToImage(root)
root.mainloop()
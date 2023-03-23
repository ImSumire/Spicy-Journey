import librosa.filters
import librosa.effects
import librosa.util
import librosa

import soundfile as sf

from scipy import signal
from scipy.signal import butter, filtfilt

import os
import numpy as np

source_dir = "tests/music/"
destination_dir = "tests/radio/"

filter_order = 4
cutoff_freq = 3000
distortion_amount = 0.5
noise_level = -45

music_files = [f for f in os.listdir(source_dir) if f.endswith(".mp3")]

for file in music_files:
    audio_data, sr = librosa.load(os.path.join(source_dir, file), sr=None, mono=True)
    print('Music getted')

    audio_data = librosa.util.normalize(audio_data)
    print('Music normalized')

    audio_data = np.tanh(distortion_amount * audio_data) / np.tanh(distortion_amount)
    print('Distortion applied')

    noise_amp = 0.005 * np.max(audio_data)
    noise = np.random.normal(0, noise_amp, len(audio_data))
    audio_data = audio_data + noise
    print('Grain applied')

    audio_data = librosa.effects.pitch_shift(audio_data, sr=sr, n_steps=2)
    print('Music pitch shifted')
    

    new_file = file.replace(".mp3", "_radio.mp3")
    sf.write(os.path.join(destination_dir, new_file), audio_data, sr)
    print('Music done')

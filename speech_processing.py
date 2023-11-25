import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import wave


def openfile(file_name):
    with wave.open(file_name, 'r') as wav_file:
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        rate = wav_file.getframerate()

        if wav_file.getnchannels() == 2:
            print("Stereo file detected, using only one channel.")
            signal = signal[::2]
        return signal, rate


def fft(signal, fs):
    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    fft_spectrum = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(fft_spectrum), 1 / fs)
    return Time, fft_spectrum, freq


def stft(signal, fs, start_time, end_time):
    f, t, Zxx = sp.signal.stft(signal, fs=fs, nperseg=256)
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(t, f, 20 * np.log10(np.abs(Zxx)), shading="gouraud", cmap="gnuplot2")
    plt.title("STFT Spectrogram")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (sec)")
    plt.xlim(start_time, end_time)
    plt.ylim(0, 8000)
    plt.colorbar(label="Intensity (dB)")
    plt.show()


def spectrogram(freq, fs, start_time, end_time):
    plt.figure(figsize=(12, 6))
    plt.specgram(freq, Fs=fs, NFFT=1024, noverlap=900, cmap="gnuplot2")
    plt.clim(0, 50)
    plt.xlabel("Time (sec)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectrogram")
    plt.xlim(start_time, end_time)
    plt.ylim(0, 8000)
    plt.colorbar(label="Intensity (dB)")
    plt.show()


# Open /k/ speech sound file
signal_k, fs_k = openfile("recordings/-k-.wav")
t0_k = 0.95
t1_k = 1.15

# Plot Spectrogram of /k/ sound
spectrogram(signal_k, fs_k, t0_k, t1_k)

# Open /f/ speech sound file
signal_f, fs_f = openfile("recordings/-f-.wav")
t0_f = 1.08
t1_f = 1.45

# Plot Spectrogram of /f/ sound
spectrogram(signal_f, fs_f, t0_f, t1_f)

# open alphabet speech sound file
signal_alpha, fs_alpha = openfile("recordings/alpha.wav")
t0_alpha = 0
t1_alpha = 23

# Plot Spectrogram of alphabet sound
spectrogram(signal_alpha, fs_alpha, t0_alpha, t1_alpha)

# stft(signal_k, fs_k, t0_k, t1_k)

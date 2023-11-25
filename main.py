import matplotlib.pyplot as plt
import numpy as np
import wave


def openfile(file_name):
    with wave.open(file_name, 'r') as wav_file:
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        rate = wav_file.getframerate()

        if wav_file.getnchannels() == 2:
            print("Stereo file detected, using only one channel.")
            signal = signal[::2]

        fft_spectrum = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(fft_spectrum), 1 / rate)
        return signal, freq, rate


def spectrogram(freq, rate, start_time, end_time):
    plt.figure(figsize=(12, 6))
    plt.specgram(freq, Fs=rate, NFFT=1024, noverlap=900, cmap="jet")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.title("Spectrogram")
    plt.xlim(start_time, end_time)
    plt.ylim(0, 8000)
    plt.colorbar(label="Intensity [dB]")
    plt.show()


signal_k, freq_k, rate_k = openfile("-k-.wav")
plt.figure(figsize=(12, 6))
plt.plot(signal_k)
plt.show()
t0_k = 0.95
t1_k = 1.20
spectrogram(signal_k, rate_k, t0_k, t1_k)

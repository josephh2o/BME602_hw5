import numpy as np
import matplotlib.pyplot as plt
import wave
from scipy.signal import butter, filtfilt


def openfile(file_name):
    with wave.open(file_name, 'r') as wav_file:
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        rate = wav_file.getframerate()

        if wav_file.getnchannels() == 2:
            signal = signal[::2]

        return signal, rate


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def fft_segment(signal, fs):
    fft_spectrum = np.fft.fft(signal)
    return np.abs(fft_spectrum)


def average_amplitude_per_band(signal, fs, segment_duration, frequency_bands):
    num_segments = int(len(signal) / (segment_duration * fs))
    time_steps = np.arange(num_segments) * segment_duration
    avg_amplitudes_over_time = {band: [] for band in frequency_bands}

    for band in frequency_bands:
        filtered_signal = bandpass_filter(signal, band[0], band[1], fs)
        if np.isnan(filtered_signal).any():
            print(f"NaN values detected in the band: {band[0]}-{band[1]} Hz")

        for i in range(num_segments):
            start = int(i * segment_duration * fs)
            end = int(start + segment_duration * fs)
            segment = filtered_signal[start:end]
            fft_amplitude = fft_segment(segment, fs)

            avg_amplitude = np.mean(fft_amplitude)
            avg_amplitudes_over_time[band].append(avg_amplitude)

    return time_steps, avg_amplitudes_over_time


def analysis(file_name):
    segment_duration = 0.005
    frequency_bands = [(max(120, i * 800), (i + 1) * 800) for i in range(10)]

    signal, fs = openfile(file_name)

    time_steps, avg_amplitudes_over_time = average_amplitude_per_band(signal, fs, segment_duration, frequency_bands)

    plt.figure(figsize=(12, 6))
    plt.specgram(signal, Fs=fs, NFFT=1024, noverlap=900, cmap="gnuplot2")
    plt.clim(0, 50)
    plt.xlabel("Time (sec)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectrogram")
    plt.ylim(0, 8000)
    plt.colorbar(label="Intensity (dB)")
    plt.show()

    plt.figure(figsize=(15, 20))
    for idx, (band, amplitudes) in enumerate(avg_amplitudes_over_time.items(), 1):
        plt.subplot(8, 2, idx)
        plt.plot(time_steps, amplitudes, label=f'{band[0]}-{band[1]} Hz')
        plt.title(f'Average Amplitude: {band[0]}-{band[1]} Hz')
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()

    colors = plt.cm.viridis(np.linspace(0, 1, len(frequency_bands)))

    plt.figure(figsize=(12, 6))
    for (band, amplitudes), color in zip(avg_amplitudes_over_time.items(), colors):
        plt.plot(time_steps, amplitudes, label=f'{band[0]}-{band[1]} Hz', color=color)

    plt.title("Average Amplitude over Time for Frequency Bands")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()


analysis("recordings/alpha.wav")
analysis("recordings/-f-.wav")
analysis("recordings/-k-.wav")
plt.show()

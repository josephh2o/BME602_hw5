import matplotlib.pyplot as plt
import numpy as np
import wave
import scipy.fftpack


def read_and_plot_spectrogram(file_name):
    # Open the wave file
    with wave.open(file_name, 'r') as wav_file:
        # Extract Raw Audio from Wav File
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')

        # Get the frame rate
        frate = wav_file.getframerate()

        # If Stereo, use only one channel
        if wav_file.getnchannels() == 2:
            print("Stereo file detected, using only one channel.")
            signal = signal[::2]

        # Perform FFT
        Time = np.linspace(0, len(signal) / frate, num=len(signal))
        fft_spectrum = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(fft_spectrum), 1 / frate)

        # Limit the frequencies to 0-3000 Hz
        idx = np.logical_and(freq >= 0, freq <= 3000)

        # Plot the spectrogram
        plt.figure(figsize=(12, 6))
        plt.specgram(signal, Fs=frate, NFFT=1024, noverlap=900)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.title('Spectrogram (0-3000 Hz)')
        plt.xlim(0, len(signal) / frate)
        plt.ylim(0, 3000)
        plt.colorbar(label='Intensity [dB]')
        plt.show()


# Replace 'your_wave_file.wav' with the path to your wave file
read_and_plot_spectrogram("-k-.wav")

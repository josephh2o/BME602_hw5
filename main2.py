import numpy as np
import matplotlib.pyplot as plt
import wave


def plot_fft_of_frame(file_name, start_time, duration):
    """
    Plots the FFT of a specific frame in a wave file.

    :param file_name: Path to the wave file.
    :param start_time: Start time of the frame in seconds.
    :param duration: Duration of the frame in seconds.
    """
    with wave.open(file_name, 'r') as wav_file:
        # Get frame rate
        frame_rate = wav_file.getframerate()

        # Calculate start and end frames
        start_frame = int(start_time * frame_rate)
        end_frame = int(start_frame + duration * frame_rate)

        # Set position and read frames
        wav_file.setpos(start_frame)
        frames = wav_file.readframes(end_frame - start_frame)
        signal = np.frombuffer(frames, dtype='int16')

        # Perform FFT
        fft_spectrum = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(fft_spectrum), 1 / frame_rate)

        # Take only the positive frequencies
        half_n = len(fft_spectrum) // 2
        fft_spectrum_positive = fft_spectrum[:half_n]
        freq_positive = freq[:half_n]

        # Plot the FFT spectrum
        plt.figure(figsize=(12, 6))
        plt.plot(freq_positive, np.abs(fft_spectrum_positive) / len(fft_spectrum_positive))
        plt.title('FFT Spectrum of Frame')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.xlim(0.3, 8000)  # Limiting x-axis to 3000 Hz for relevance
        plt.show()


# Example usage
file_name = "recordings/-k-.wav"  # Replace with your file path
start_time = 1.00  # Start time in seconds
duration = .05  # Duration in seconds
plot_fft_of_frame(file_name, start_time, duration)

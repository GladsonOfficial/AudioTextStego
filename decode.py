import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

def decode_and_save_image(input_file, output_file):
    try:
        sample_rate, data = wavfile.read(input_file)

        if data.ndim > 1:
            data = data.mean(axis=1)

        frequencies, times, spectrogram = signal.spectrogram(data, fs=sample_rate, nperseg=1024)

        plt.figure(figsize=(12, 6))
        
        plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram + 1e-10), cmap='gray_r')
        
        plt.axis('off')
        plt.ylim([0, 20000])

        plt.savefig(output_file, bbox_inches='tight', pad_inches=0)

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    decode_and_save_image('temp_resources/output.wav', 'temp_resources/output.png')
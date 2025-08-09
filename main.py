import numpy as np
from scipy.io import wavfile
from scipy import signal
import soundfile as sf

raw_audio_filename = "temp_resources/Mera Bharat.wav"

def bandstop_bandpass(signal, Q, center_frequency, fs, bandpass=False):
    filtered = np.zeros_like(signal)

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    
    for i in range(signal.shape[0]):
        BW = center_frequency[i] / Q
        
        tan = np.tan(np.pi * BW / fs)

        c = (tan - 1) / (tan + 1)
        d = - np.cos(2 * np.pi * center_frequency[i] / fs)
        
        b = [-c, d * (1 - c), 1]
        a = [1, d * (1 - c), -c]

        x = signal[i]

        y = b[0] * x + b[1] * x1 + b[2] * x2 - a[1] * y1 - a[2] * y2
        
        y2 = y1
        y1 = y
        x2 = x1
        x1 = x
        
        filtered[i] = y
    
    sign = -1 if bandpass else 1
    output = 0.5 * (signal + sign * filtered)
    
    return output


def main():
    pass


if __name__ == "__main__":
    
    sample_rate, data = wavfile.read(raw_audio_filename)
    low_cutoff = 15000.0
    high_cutoff = 19000.0
    
    nyquist_freq = 0.5 * sample_rate
    low_cutoff_normalized = low_cutoff / nyquist_freq
    high_cutoff_normalized = high_cutoff / nyquist_freq
    print(low_cutoff_normalized, high_cutoff_normalized)
    
    order = 30

    b, a = signal.butter(N=order, Wn=[low_cutoff_normalized, high_cutoff_normalized], btype='bandstop')

    filtered_data = signal.lfilter(b, a, data)
    filtered_data = filtered_data.astype(np.int16)
    
    wavfile.write('output.wav', sample_rate, filtered_data)
    
    



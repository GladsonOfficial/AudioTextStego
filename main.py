import numpy as np
from scipy.io import wavfile
from scipy import signal


def apply_bandstop_in_pattern(pattern):
    pass    

def apply_bandstop_filter(audio_data, sample_rate, low_freq, high_freq, order=8):
    try:
        print(f'Audio Data: {audio_data}')
        original_dtype = audio_data.dtype

        if audio_data.ndim > 1:
            audio_data = audio_data.mean(axis=1)
        
        # print(f"data: {data}")

        data_float = audio_data.astype(np.float64)
        
        nyquist_freq = 0.5 * sample_rate
        low_normalized = low_freq / nyquist_freq
        high_normalized = high_freq / nyquist_freq
        
        if low_normalized >= 1.0 or high_normalized >= 1.0:
            print("Cutoff frequency is too high for given sample rate")
            return
        
        b, a = signal.butter(N=order, Wn=[low_normalized, high_normalized], btype='bandstop')
        filtered_data_float = signal.lfilter(b, a, data_float)
        
        min_val = np.iinfo(original_dtype).min
        max_val = np.iinfo(original_dtype).max
        
        filtered_data = np.clip(filtered_data_float, min_val, max_val)
        
        filtered_data = filtered_data.astype(original_dtype)
        
        return filtered_data
    
    except Exception as e:
        print(f"An error occured: {e}")
        
        


if __name__ == "__main__":
    input_filename = "temp_resources/Mera Bharat.wav" 
    output_filename = "temp_resources/output.wav"

    low_cutoff_freq = 15000.0
    high_cutoff_freq = 16000.0
    
    sample_rate, wave_file_data = wavfile.read(input_filename)
    print(sample_rate, wave_file_data)
    output_data = apply_bandstop_filter(wave_file_data, sample_rate, low_cutoff_freq, high_cutoff_freq)
    wavfile.write(output_filename, sample_rate, output_data)

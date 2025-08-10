import numpy as np
from scipy.io import wavfile
from scipy import signal
import char_patterns

def apply_bandstop_in_pattern(pattern, audio_data, sample_rate):
    for i, v in enumerate(pattern):
        if v == 1:
            audio_data = apply_bandstop_filter(audio_data, sample_rate, char_patterns.lines[i][0], char_patterns.lines[i][1])
    
    return audio_data


def trim_audio(audio_file, sample_rate, start_time, end_time):
    start_sample = start_time * sample_rate
    end_sample = end_time * sample_rate

    return audio_file[start_sample: end_sample]


def apply_bandstop_filter(audio_data, sample_rate, low_freq, high_freq, order=8):
    try:
        # print(f'Audio Data: {audio_data}')
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

    # low_cutoff_freq = 15000.0
    # high_cutoff_freq = 16000.0
    
    sample_rate, wave_file_data = wavfile.read(input_filename)

    if wave_file_data.ndim > 1:
        wave_file_data = wave_file_data.mean(axis=1).astype(wave_file_data.dtype)
        print("Convert to mono")
    
    print(sample_rate, wave_file_data)
    part1 = trim_audio(wave_file_data, sample_rate, 0, 5)
    part2 = trim_audio(wave_file_data, sample_rate, 5, 10)
    part3 = trim_audio(wave_file_data, sample_rate, 10, len(wave_file_data))

    # part2 = apply_bandstop_filter(part2, sample_rate, low_cutoff_freq, high_cutoff_freq)
    part2 = apply_bandstop_in_pattern([1,0,0,1,0,1], part2, sample_rate)
    full_audio = np.concatenate((part1, part2, part3))
    wavfile.write(output_filename, sample_rate, full_audio)

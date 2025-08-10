import numpy as np
import char_patterns
from scipy import signal
from scipy.io import wavfile

def creating_pattern_from_sentence(sentence):
    sentence_arr = []
    for i in sentence:
        sentence_arr.extend(creating_pattern_from_char(i))
    return sentence_arr

def creating_pattern_from_char(character):
    pattern = char_patterns.char_pattern[character]
    arrarr = []
    arr = []
    for i in range(len(pattern[0])):
        for j in pattern:
            arr.append(j[i])
        arrarr.append(arr)
        arr = []
    
    return arrarr 

def apply_bandstop_with_array(pattern_arr, audio_data, sample_rate):
    start_time = 3
    pattern_width_time = 1
    current_time = start_time

    start_sample = start_time * sample_rate

    output_samples_arr = []
    output_samples_arr.append(audio_data[:start_sample])
    for i in pattern_arr:
        current_start_time = current_time
        current_end_time = current_time + pattern_width_time
        trimmed_section = trim_audio(audio_data, sample_rate, current_start_time, current_end_time)
        filtered_trimmed_section = apply_bandstop_in_pattern(i, trimmed_section, sample_rate)
        output_samples_arr.append(filtered_trimmed_section)
        current_time = current_end_time
    
    output_samples_arr.append(audio_data[current_time * sample_rate:])
    output_samples = np.concatenate(output_samples_arr)
    
    return output_samples

        
    
def apply_bandstop_in_pattern(pattern, audio_data, sample_rate):
    for i, v in enumerate(pattern):
        if v == 1:
            audio_data = apply_bandstop_filter(audio_data, sample_rate, char_patterns.lines[i][0], char_patterns.lines[i][1])
    
    return audio_data

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
        

def trim_audio(audio_file, sample_rate, start_time, end_time):
    start_sample = start_time * sample_rate
    end_sample = end_time * sample_rate

    return audio_file[start_sample: end_sample]


def encode_and_write(message, input_filename, output_filename):
    # opening audio file
    sample_rate, wave_file_data = wavfile.read(input_filename)

    # converting to mono if stereo (stereo support not added yet) 
    if wave_file_data.ndim > 1:
        wave_file_data = wave_file_data.mean(axis=1).astype(wave_file_data.dtype)
        
    # TODO:  validation of message

    
    # encoding
    pattern_array = creating_pattern_from_sentence(message)
    encoded_audio_data = apply_bandstop_with_array(pattern_array, wave_file_data, sample_rate)

    wavfile.write(output_filename, sample_rate, encoded_audio_data)



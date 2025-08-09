import numpy as np
from scipy.io import wavfile
from scipy import signal

def apply_bandstop_filter_robust(input_file, output_file, low_freq, high_freq, order=8):
    """
    Applies a band-stop filter to a WAV file with robust data type handling.
    """
    try:
        sample_rate, data = wavfile.read(input_file)
        
        # Store the original data type to convert back later
        original_dtype = data.dtype
        
        # Convert to mono if it's stereo
        if data.ndim > 1:
            data = data.mean(axis=1)

        # Convert data to a floating-point type for accurate filtering
        # Using float64 is safer for filter calculations
        data_float = data.astype(np.float64)

        # Normalize cutoff frequencies
        nyquist_freq = 0.5 * sample_rate
        low_normalized = low_freq / nyquist_freq
        high_normalized = high_freq / nyquist_freq

        # Sanity check for valid normalized frequencies
        if low_normalized >= 1.0 or high_normalized >= 1.0:
            print("Error: Cutoff frequency is too high for the given sample rate.")
            return

        # Design the band-stop filter
        b, a = signal.butter(N=order, Wn=[low_normalized, high_normalized], btype='bandstop')

        # Apply the filter
        filtered_data_float = signal.lfilter(b, a, data_float)

        # Convert back to the original data type.
        # This is where the clipping and scaling need to be correct.
        
        # Get the min/max values for the original data type (e.g., -32768 to 32767 for int16)
        min_val = np.iinfo(original_dtype).min
        max_val = np.iinfo(original_dtype).max

        # Clip the float data to the integer range to prevent overflow
        filtered_data = np.clip(filtered_data_float, min_val, max_val)
        
        # Final conversion back to the original integer type
        filtered_data = filtered_data.astype(original_dtype)

        # Save the filtered audio to a new file
        wavfile.write(output_file, sample_rate, filtered_data)
        print(f"Successfully filtered '{input_file}' and saved to '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage with your desired frequencies
if __name__ == '__main__':
    input_wav = 'temp_resources/Mera Bharat.wav'
    output_wav = 'temp_resources/output.wav'
    
    # Frequencies to attenuate
    low_cutoff_freq = 15000.0
    high_cutoff_freq = 16000.0
    
    apply_bandstop_filter_robust(input_wav, output_wav, low_cutoff_freq, high_cutoff_freq)
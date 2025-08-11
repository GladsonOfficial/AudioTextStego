import numpy as np
import encoding
import decode
import os

OUTPUT_AUDIO_PATH = 'output/output.wav'
OUTPUT_IMAGE_PATH = 'output/image.png'

def encode_handler():
    print("-- Encode --")
    print("Please enter the message to encode")
    message = input("> ")
    print("Please enter the path of the audio file")
    audio_path = input("> ")
    
    encoding.encode_and_write(message, audio_path, OUTPUT_AUDIO_PATH)
    print(f"Steganography is successful. The encoded audio file can be found in: {OUTPUT_AUDIO_PATH}")
    os.system('pause')

def decode_handler():
    print("-- Deocde --")
    print("Please enter the path of the encoded audio file")
    image_path = input("> ")
    decode.decode_and_save_image(image_path, OUTPUT_IMAGE_PATH)
    print(f"Decoding completed, please check the output image in: {OUTPUT_IMAGE_PATH}")
    os.system('pause')


def show_menu():
    while True:
        print("Please select:\n\t(E)ncode\n\t(D)ecode")
        option = input("> ")
        if option.lower() == 'e':
            encode_handler() 
            break
        elif option.lower() == 'd':
            decode_handler()
            break
        else:
            print("Please enter a valid choice")
        


if __name__ == "__main__":
    # encoding.encode_and_write("AA", "temp_resources/Mera Bharat.wav", "temp_resources/output.wav")
    show_menu()
    

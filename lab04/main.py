import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
import os


# Load the audio file
def load_audio(file_path):
    sample_rate, data = wavfile.read(file_path)
    return sample_rate, data


# Plot waveform of the audio signal and save it as PNG
def plot_waveform(sample_rate, data):
    time = np.linspace(0, len(data) / sample_rate, num=len(data))
    plt.figure(figsize=(10, 4))
    plt.plot(time, data)
    plt.title("Audio Waveform")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("waveform.png")
    plt.show()


# Display basic audio properties
def display_properties(sample_rate, data):
    duration = len(data) / sample_rate
    print(f"Sampling rate: {sample_rate} Hz")
    print(f"Number of samples: {len(data)}")
    print(f"Duration: {duration:.2f} seconds")


# Play the audio
def play_audio(data, sample_rate):
    sd.play(data, samplerate=sample_rate)
    sd.wait()


# Extract first 5 seconds of the audio and save it
def extract_segment(data, sample_rate, output_path):
    segment = data[:sample_rate * 5]
    wavfile.write(output_path, sample_rate, segment)
    return segment


# Compress audio by reducing sample rate and bit depth
def compress_audio(segment, original_rate, output_path_lowrate, output_path_8bit):
    # Downsample by taking every second sample
    segment_downsampled = segment[::2]
    reduced_rate = original_rate // 2
    wavfile.write(output_path_lowrate, reduced_rate, segment_downsampled)

    # Convert to float to avoid overflow, normalize to 0-255 and convert to uint8
    segment_float = segment.astype(np.float32)
    segment_normalized = ((segment_float - segment_float.min()) / (segment_float.max() - segment_float.min()) * 255).astype(np.uint8)
    wavfile.write(output_path_8bit, original_rate, segment_normalized)


# Compare file sizes
def compare_file_sizes(*file_paths):
    for path in file_paths:
        size_kb = os.path.getsize(path) / 1024
        print(f"{path}: {size_kb:.2f} KB")


# Main function to run all steps
def main():
    input_path = "input.wav"
    segment_path = "segment.wav"
    compressed_lowrate_path = "compressed_lowrate.wav"
    compressed_8bit_path = "compressed_8bit.wav"

    sample_rate, data = load_audio(input_path)
    plot_waveform(sample_rate, data)
    display_properties(sample_rate, data)
    play_audio(data, sample_rate)
    segment = extract_segment(data, sample_rate, segment_path)
    compress_audio(segment, sample_rate, compressed_lowrate_path, compressed_8bit_path)
    compare_file_sizes(input_path, segment_path, compressed_lowrate_path, compressed_8bit_path)


if __name__ == "__main__":
    main()

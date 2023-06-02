import numpy as np
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import os


class SingingSynthesizer:
    def __init__(self, duration=2.0, modulation_range=50.0):
        self.duration = duration
        self.modulation_range = modulation_range

    def synthesize_singing(self, text):
        # Set up audio parameters
        sample_rate = 44100
        t = np.linspace(0, self.duration, int(self.duration * sample_rate), endpoint=False)
        # Generate modulating signal
        modulating_freq = self.modulation_range * 2 * np.pi
        modulating_wave = np.sin(modulating_freq * t)
        # Split the text into words
        words = text.split()
        # Synthesize and process each word
        output = np.array([])
        for word in words:
            # Synthesize speech for the word using gTTS
            tts = gTTS(text=word, lang='en', slow=False)
            tts.save('temp.mp3')
            # Load speech audio
            speech_audio, _ = sf.read('temp.mp3')
            # Define the available carrier frequencies for whole notes on a piano
            available_carrier_freqs = [
                27.50, 32.70, 36.71, 41.20, 46.25, 55.00, 65.41, 73.42, 82.41, 92.50, 110.00, 130.81, 146.83,
                164.81, 185.00, 220.00, 261.63, 293.66, 329.63, 369.99, 440.00, 523.25, 587.33, 659.25, 739.99,
                880.00, 1046.50, 1174.66, 1318.51, 1479.98, 1760.00, 2093.00, 2349.32, 2637.02, 2959.96, 3520.00,
                4186.01, 4978.03, 5587.65
            ]
            carrier_freq = np.random.choice(available_carrier_freqs)
            # Generate carrier signal
            word_duration = len(word) * self.duration / len(text)
            t_word = np.linspace(0, word_duration, int(word_duration * sample_rate), endpoint=False)
            carrier_wave = np.sin(carrier_freq * 2 * np.pi * t_word)
            # Resize carrier_wave and modulating_wave to match the length of speech_audio
            carrier_wave = np.resize(carrier_wave, len(speech_audio))
            modulating_wave = np.resize(modulating_wave, len(speech_audio))
            # Apply pitch modulation to speech
            modulated_speech = speech_audio * (1 + carrier_wave * modulating_wave)
            # Scale modulated speech to match original speech amplitude
            modulated_speech *= np.max(speech_audio) / np.max(modulated_speech)
            # Mix modulated speech with original speech
            word_output = speech_audio + modulated_speech * 1e9
            # Concatenate the word output with previous words
            output = np.concatenate((output, word_output))

        # Normalize output
        output /= np.max(np.abs(output))
        # Play the synthesized singing
        sd.play(output, sample_rate / 1.75)
        sd.wait()
        # Clean up temporary file
        os.remove('temp.mp3')

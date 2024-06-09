import sounddevice as sd
import numpy as np

class AudioHandler:
    def __init__(self, mic_name):
        self.mic_name = mic_name
        self.device_id = self.get_microphone_device_id(mic_name)
        if self.device_id is None:
            raise ValueError(f"Microphone '{mic_name}' not found.")

    @staticmethod
    def list_microphones():
        devices = sd.query_devices()
        mics = [device for device in devices if device['max_input_channels'] > 0]
        return mics

    def get_microphone_device_id(self, name):
        devices = sd.query_devices()
        for device in devices:
            if device['name'] == name and device['max_input_channels'] > 0:
                return device['index']
        return None

    def get_microphone_input(self, duration=1, fs=44100):
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64', device=self.device_id)
        sd.wait()  # Wait until recording is finished
        volume = np.linalg.norm(recording)
        return volume

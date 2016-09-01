from os.path import join
import pyaudio
import wave
import audioop
import matplotlib.pyplot as plt


class SpeechServices:
    # Configure Audio Interface
    SAMPLESIZE = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    SAMPLERATE = 44100
    THRESHOLD = 1200

    def __init__(self, directory):
        self.workingDirectory = directory
        self.audio = pyaudio.PyAudio()
        self.audioInStream = self.audio.open(format=SpeechServices.FORMAT, channels=SpeechServices.CHANNELS,
                                             rate=SpeechServices.SAMPLERATE, input=True,
                                             frames_per_buffer=SpeechServices.SAMPLESIZE)
        self.audioOutStream = self.audio.open(format=SpeechServices.FORMAT, channels=SpeechServices.CHANNELS,
                                              rate=SpeechServices.SAMPLERATE, output=True,
                                              frames_per_buffer=SpeechServices.SAMPLESIZE)

    def record_cmd(self, filename, duration):
        filedata = []
        activesecs = 0
        inactivesecs = 0
        self.audioInStream.start_stream()
        wf = wave.open(join(self.workingDirectory, filename), 'wb')
        wf.setnchannels(SpeechServices.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(SpeechServices.FORMAT))
        wf.setframerate(SpeechServices.SAMPLERATE)
        while activesecs < duration or inactivesecs < 1:
            rmsdata = []
            frames = []
            for i in range(0, int(SpeechServices.SAMPLERATE / SpeechServices.SAMPLESIZE)):
                sample = self.audioInStream.read(SpeechServices.SAMPLESIZE)
                frames.append(sample)
                filedata.append(sample)
                rmsdata.append(audioop.rms(sample, 2))
            if sum(i > SpeechServices.THRESHOLD for i in rmsdata) > 10:
                print
                "activity detected..."
                activesecs += 1
                inactivesecs = 0
            else:
                if inactivesecs > 1:
                    activesecs = 0
                    inactivesecs = 0
                    filedata = []
                inactivesecs += 1
        print
        "Writing audio data to file..."
        wf.writeframes(b''.join(filedata))
        wf.close()
        self.audioInStream.stop_stream()
        return filedata

    def play_response(self, filename):
        self.audioOutStream.start_stream()
        wf = wave.open(join(self.workingDirectory, filename), 'rb')
        data = wf.readframes(SpeechServices.SAMPLESIZE)
        while data != '':
            self.audioOutStream.write(data)
            data = wf.readframes(SpeechServices.SAMPLESIZE)
        wf.close()
        self.audioOutStream.stop_stream()
        self.audioOutStream.close()

    def plot_audio_graph(self, data):
        plt.plot(data)
        plt.ylabel('Amplitude')
        plt.show()

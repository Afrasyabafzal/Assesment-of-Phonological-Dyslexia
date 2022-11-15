from vosk import Model, KaldiRecognizer
import pyaudio
import time

from asyncio.windows_events import NULL


class TexttoSpeech :
    def __init__(self):
        self.output=NULL
        self.count = 0

    def convert(self):
        model= Model("D:\\fyp\\saif fyp\\vosk-model-small-en-us-0.15")
        recognizer = KaldiRecognizer(model,16000)
        mic =pyaudio.PyAudio()
        stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
        stream.start_stream()
        temp = []
        a = None
        i=0
        while i<20:
            data=stream.read(4096)
            # print(data)
            #if len(data)==0:
            # break
            i = i+1
            if recognizer.AcceptWaveform(data):
                a = recognizer.FinalResult()
                self.output=a
                print(a)
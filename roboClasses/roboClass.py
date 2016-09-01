from os.path import dirname
from roboClasses.watsonClass import *
from roboClasses.audioClass import *
from roboClasses.wolfClass import *
import threading


class Robosapien(WatsonServices, SpeechServices, WolfServices):

    NAMES = ["Rob", "Row", "rob", "row"]

    def __init__(self):
        WatsonServices.__init__(self, join(dirname(__file__), "roboConfig/"))
        SpeechServices.__init__(self, join(dirname(__file__), "roboConfig/"))
        WolfServices.__init__(self, join(dirname(__file__), "roboConfig/"))
        self.watson_event = threading.Event()
        self.cmd_event = threading.Event()
        self.response_event = threading.Event()
        self.cmd_thread = threading.Thread(name='cmdThread', target=self.get_voice_command, args=())
        self.watson_thread = threading.Thread(name='watsonThread', target=self.call_watson, args=())
        self.response_thread = threading.Thread(name='responseThread', target=self.say_response, args=())

    def get_voice_command(self):
        while True:
            SpeechServices.record_cmd(self, "command.wav", 3)
            self.cmd_event.set()
            self.response_event.wait()
            self.response_event.clear()

    def call_watson(self):
        while True:
            self.cmd_event.wait()
            self.cmd_event.clear()
            cmd = WatsonServices.stt_call(self, "command.wav")
            print cmd
            if any(substring in cmd for substring in Robosapien.NAMES):
                response = WatsonServices.conversation(self, cmd)
                if response == "I don't understand":
                    response = WolfServices.wolf_query(self, cmd)
                print response
                WatsonServices.tts_call(self, response, "response.wav")
                self.watson_event.set()
            else:
                self.response_event.set()

    def say_response(self):
        while True:
            self.watson_event.wait()
            SpeechServices.play_response(self, "response.wav")
            self.watson_event.clear()
            self.response_event.set()

from os.path import join
import json
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import DialogV1


class WatsonServices:

    def __init__(self, directory):
        # Open STT Service
        with open(join(directory, "sttConfig.json")) as confile:
            stt_config = json.load(confile)['credentials']
        self.speechToText = SpeechToTextV1(username=stt_config['username'], password=stt_config['password'])

        # Open TTS Service
        with open(join(directory, "ttsConfig.json")) as confile:
            tts_config = json.load(confile)['credentials']
        self.textToSpeech = TextToSpeechV1(username=tts_config['username'], password=tts_config['password'])

        # Open the Dialog Service
        with open(join(directory, "dialogConfig.json")) as confile:
            dialog_config = json.load(confile)['credentials']
        self.dialogID = dialog_config['id']
        self.dialog = DialogV1(username=dialog_config['username'], password=dialog_config['password'])
        self.response = self.dialog.conversation(self.dialogID)
        self.workingDirectory = directory

    def tts_call(self, text, file_name):
        with open(join(self.workingDirectory, file_name), 'wb') as audio_file:
            audio_file.write(self.textToSpeech.synthesize(text, accept='audio/wav', voice="en-US_MichaelVoice"))

    def stt_call(self, file_name):
        with open(join(self.workingDirectory, file_name), 'rb') as audio_file:
            service_response = json.loads((json.dumps(self.speechToText.recognize(audio_file,
                                                      content_type='audio/wav', timestamps=False),
                                                      indent=2)))
        try:
            text = (service_response.get("results")[0].get("alternatives")[0].get("transcript"))
        except:
            text = ""
        print text
        return text

    def conversation(self, prompt):
        # Send the text to the dialog service and get the response
        self.response = self.dialog.conversation(dialog_id=self.dialogID, dialog_input=prompt,
                                                 conversation_id=self.response['conversation_id'],
                                                 client_id=self.response['client_id'])
        reply = self.response['response']
        reply = reply[0]
        return reply

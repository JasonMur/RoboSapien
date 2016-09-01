import wolframalpha
from os.path import join
import json


class WolfServices:
    def __init__(self, directory):
        with open(join(directory, "wolfConfig.json")) as confile:
            wolf_config = json.load(confile)['credentials']
        self.app_id = wolf_config['id']
        self.client = wolframalpha.Client(self.app_id)

    def wolf_query(self, question):
        result = self.client.query(question)
        if len(result.pods) > 0:
            pod = result.pods[1]
            if pod.text:
                answer = pod.text
                answer = answer.encode('ascii', 'ignore')
            else:
                answer = "I have no answer for that."
        else:
            answer = "Sorry, I am not sure."
        return answer

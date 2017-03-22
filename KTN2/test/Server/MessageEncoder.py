import json
import time

class MessageEncoder():

    def encode_error(self, error):
        return json.dumps({'timestamp':time.time(), 'sender':"", 'response':'error', 'content':error})

    def encode_info(self, info):
        return json.dumps({'timestamp':time.time(), 'sender':"", 'response':'info', 'content':info})

    def encode_message(self, sender, message):
        return json.dumps({'timestamp':time.time(), 'sender':sender, 'response':'message', 'content':message})

    def encode_history(self, history):
        return json.dumps({'timestamp':time.time(), 'sender':"", 'response':'history', 'content':history})

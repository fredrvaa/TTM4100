import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return None

    def parse_error(self, payload):
        return {'timestamp': payload['timestamp'], 'error': payload['content']}
    
    def parse_info(self, payload):
        return {'timestamp': payload['timestamp'], 'info': payload['content']}

    def parse_message(self, payload):
        return {'timestamp': payload['timestamp'], 'message': payload['content'], 'sender': payload['sender']}

    def parse_history(self, payload):
        history = []
        for json_message in payload['content']:
            history.append(self.parse(json_message))
        return {'timestamp': payload['timestamp'], "history": history}

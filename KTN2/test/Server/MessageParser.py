import json

class MessageParser():

    def __init__(self):

        self.possible_responses = {
            'login': self.parse_login,
            'logout': self.parse_logout,
            'msg': self.parse_message,
            'names': self.parse_names,
            'help': self.parse_help
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['request'] in self.possible_responses:
            return self.possible_responses[payload['request']](payload)
        else:
            return None

    def parse_login(self, payload):
        return {'login': payload['content']}                

    def parse_logout(self, payload):
        return {'logout': None}

    def parse_message(self, payload):
        return {'message': payload['content']}

    def parse_names(self, payload):
        return {'names': None}

    def parse_help(self,string):
        return {'help': None}

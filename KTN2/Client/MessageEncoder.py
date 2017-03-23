import json

class MessageEncoder():

    def encode_login(self, username):
        return json.dumps({'request':'login', 'content':username})

    def encode_logout(self):
        return json.dumps({'request':'logout', 'content':None})

    def encode_sendMessage(self, message):
        return json.dumps({'request':'msg', 'content':message})

    def encode_requestNames(self):
        return json.dumps({'request':'names', 'content':None})

    def encode_requestHelp(self):
        return json.dumps({'request':'help', 'content':None})

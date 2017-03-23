# -*- coding: utf-8 -*-
import socket
import time
import sys
from enum import Enum
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
from MessageEncoder import MessageEncoder



class State(Enum):
    LOGIN = 1
    CHATROOM = 2

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Init
        self.host = host
        self.server_port = server_port
        self.state = State.LOGIN;

        self.messageEncoder = MessageEncoder()
        self.messageParser = MessageParser()

        self.username = ""

        # Run client
        self.run()

    def run(self):
        try:
            # Initiate the connection to the server
            self.connection.connect((self.host, self.server_port))
            messageReceiver = MessageReceiver(self, self.connection)
            messageReceiver.start()
        except socket.error as e:
            sys.exit("Connection to server refused.")

        while (not self.connection._closed):
            if self.state == State.LOGIN:
                print("Username:")
                self.username = input()
                self.send_payload(self.messageEncoder.encode_login(self.username))
            elif self.state == State.CHATROOM:
                message = input()
                if message == 'logout':
                    self.send_payload(self.messageEncoder.encode_logout())
                elif message == 'names':
                    self.send_payload(self.messageEncoder.encode_requestNames())
                elif message == 'help':
                    self.send_payload(self.messageEncoder.encode_requestHelp())
                else:
                    self.send_payload(self.messageEncoder.encode_sendMessage(message))

            time.sleep(0.1)

        print("Disconnected from server")



    def disconnect(self):
        self.connection.close()

    def receive_payload(self, payload):
        message = self.messageParser.parse(payload)
        if 'error' in message.keys():
            print("Error:", message['error'])
            self.state = State.LOGIN
        elif 'info' in message.keys():
            print("Info:", message['info'])
        elif 'message' in message.keys():
            if self.state == State.CHATROOM:
            	if message['sender'] != self.username:
                	print(message['sender']+":", message['message'])
        elif 'history' in message.keys():
            print("")
            print("Welcome", self.username, "to CHATROOM!")
            for msg in message['history']:
            	if msg['sender'] == self.username:
            		print(msg['message'])
            	else:
                	print(msg['sender']+":", msg['message'])
            self.state = State.CHATROOM

    def send_payload(self, payload):
    	if not self.connection._closed:
        	self.connection.send(payload.encode())


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('127.0.0.1', 9998)

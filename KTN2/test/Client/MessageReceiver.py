# -*- coding: utf-8 -*-
from threading import Thread
import socket

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        super(MessageReceiver, self).__init__()
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True

        self.client = client
        self.connection = connection

    def run(self):
        while True:
            msg = self.connection.recv(4096).decode()
            if msg == "":
                self.client.disconnect()
                return
            else:
                self.client.receive_payload(msg)
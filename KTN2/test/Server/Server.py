# -*- coding: utf-8 -*-
import socketserver
import MessageParser
import re
from MessageParser import MessageParser
from MessageEncoder import MessageEncoder

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_clients = {}
history = []

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Init
        self.messageEncoder = MessageEncoder()
        self.messageParser = MessageParser()

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).decode()

            if received_string == "":
                self.connection.close()
                del connected_clients[self.connection]
                break
            else:
                payload = self.messageParser.parse(received_string)
                if 'login' in payload.keys():
                    if re.match("^[A-Za-z0-9_-]*$", payload['login']):
                        self.connection.send(self.messageEncoder.encode_history(history).encode())
                        connected_clients[self.connection] = payload['login']
                    else:
                        self.connection.send(self.messageEncoder.encode_error("Invalid username").encode())
                elif 'logout' in payload.keys():
                    self.connection.close()
                    del connected_clients[self.connection]
                    return
                elif 'message' in payload.keys():
                    message = self.messageEncoder.encode_message(connected_clients[self.connection], payload['message'])
                    history.append(message)
                    for conn in connected_clients.keys():
                        conn.send(message.encode())
                elif 'names' in payload.keys():
                    self.connection.send(self.messageEncoder.encode_info(', '.join(connected_clients.values())).encode())
                elif 'help' in payload.keys():
                    self.connection.send(self.messageEncoder.encode_info("This is the help").encode())
                
            
    


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()

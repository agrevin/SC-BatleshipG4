import socket

class BatleshipServer:
    """Class for a Batleship server"""

    def __init__(self, host: str = 'localhost', port: int = 12345):
        """Constructor"""
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self):
        """Connect to the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.connected = True

    def disconnect(self):
        """Disconnect from the server"""
        self.socket.close()
        self.connected = False

    def receive(self):
        """Receive a message from the client"""
        return self.socket.recv(1024).decode()

if __name__ == '__main__':
    server = BatleshipServer()
    server.connect()
    while True:
        print(server.receive())
    server.disconnect()

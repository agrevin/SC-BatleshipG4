import random
import subprocess
import json
import sys
import socket

class Field:
    """Class for a Batleship field"""

    def __init__(self, ships: list, hash0: int, proof0: int, nonce0):
        """Constructor"""
        self.ships = ships
        self.nonces = nonce0
        self.hashes = hash0
        self.proofs = proof0

class BatleshipClient:
    """Class for a Batleship client"""

    def __init__(self, host: str = 'localhost', port: int = 12345):
        """Constructor"""
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.boats = {'Carrier': 5,
                      'Battleship': 4,
                      'Destroyer': 3,
                      'Cruiser1': 2,
                      'Cruiser2': 2,
                      'Submarine1': 1,
                      'Submarine2': 1}
        self.field: Field = None

    def connect(self):
        """Connect to the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.host, self.port))
        self.connected = True

    def disconnect(self):
        """Disconnect from the server"""
        self.socket.close()
        self.connected = False

    def send(self, message: str):
        """Send a message to the server"""
        self.socket.send(message.encode())
    
    def place_boats(self):
        """Ask the user to place their boats and generate a proof and a hash of the field configuration"""
        _field = []
        for boat in self.boats:
            print(f'Place your {boat} ({self.boats[boat]} spaces)')
            [x, y, direction] = input('Enter the x(0-9), y(0-9), and direction (0-UP, 1-RIGHT, 2-DOWN, 3-LEFT): ').split()
            _field.append([x, y, direction])
        #generate random nonce from 0 to 2^16-1
        self.field_nonce = random.randint(0, 2**16 - 1)
        data = {'nonce': self.field_nonce, 'ships': _field}
        #generate proof from zokrates file
        flat_list = [item for sublist in _field for item in sublist]
        print(flat_list)    
        compute_witness_command = f'zokrates compute-witness -a {self.field_nonce} {" ".join(map(str, flat_list))}'
        generate_proof_command = f'zokrates generate-proof'

        print(f"Executing command: {compute_witness_command}")
        # Execute the commands using subprocess
        try:
            # Execute the compute-witness command
            subprocess.run(compute_witness_command, shell=True, check=True)

            # Execute the generate-proof command
            subprocess.run(generate_proof_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")  

        


if __name__ == '__main__':
    client = BatleshipClient()
    client.connect()
    data = client.place_boats()
    client.send(json.dumps(data))
    client.disconnect()

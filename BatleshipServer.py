import socket
import os
import subprocess
from BatleshipServerClasses import BatleshipGames





class BatleshipServer:
    """Class for a Batleship server"""

    def __init__(self, host: str = 'localhost', port: int = 12345):
        """Constructor"""

        #Http stuff
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

        #Game stuff
        self.battleship_games = BatleshipGames()

        #dispatcher stuff
        self.note_types: dict = {
            "create": self.note_type_create,
            "join": self.note_type_join,
            "fire": self.note_type_fire,
            "report": self.note_type_report,
            "wave": self.note_type_wave,
            "claim": self.note_type_claim,
            "requestPlayer": self.note_type_requestPlayer,
            "requestTurn": self.note_type_requestTurn,
            "requestGamesNames": self.note_type_requestGamesNames
        }

        #Directory stuff
        self.temp_dir: str = f"{os.getcwd()}/temp"
        self.proof_dir: str = f"{os.getcwd()}/ServerVerifiers"
        self.field_proof_dir = f"{self.proof_dir}/field"
        self.alive_proof_dir = f"{self.proof_dir}/alive"
        self.shot_proof_dir = f"{self.proof_dir}/shot"
        os.makedirs(self.proof_dir, exist_ok=True)
        os.makedirs(self.field_proof_dir, exist_ok=True)
        os.makedirs(self.alive_proof_dir, exist_ok=True)
        os.makedirs(self.shot_proof_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)


    def connect(self):
        """Connect to the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.connected = True

    def disconnect(self):
        """Disconnect from the server"""
        self.socket.close()
        self.connected = False

    # Receive message from client
    def receive(self):
        """Receive a message from the client"""
        return self.socket.recv(10240).decode()

    def alive_verifier(self):
        verify_command = f'zokrates verify -j {self.temp_dir}/proof.json -v {self.alive_proof_dir}/verification.key'

        print(f"Executing command: {verify_command}")

        try:
            # Execute the compute-witness command
            verify_process = subprocess.run(verify_command, shell=True, check=True, capture_output=True)
            print(f"Output: {verify_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            
    def shot_verifier(self):
        verify_command = f'zokrates verify -j {self.temp_dir}/proof.json -v {self.shot_proof_dir}/verification.key'

        print(f"Executing command: {verify_command}")

        try:
            # Execute the compute-witness command
            verify_process = subprocess.run(verify_command, shell=True, check=True, capture_output=True)
            print(f"Output: {verify_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
    
    def battle_ground_verifier(self):
        verify_command = f'zokrates verify -j {self.temp_dir}/proof.json -v {self.field_proof_dir}/verification.key'

        print(f"Executing command: {verify_command}")

        try:
            # Execute the compute-witness command
            verify_process = subprocess.run(verify_command, shell=True, check=True, capture_output=True)
            print(f"Output: {verify_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")



    # Create type note
    def note_type_create(self, args: list):
        note_data = {
            "sender_id": args[0],
            "game_id": args[1],
            "fleet_position": args[2]
        }

        

        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_position"])
        
        self.battle_ground_verifier()

        os.remove(f'{self.temp_dir}/proof.json')

        print(self.battleship_games.createGame(note_data["game_id"],note_data["sender_id"]))

    # Join type note
    def note_type_join(self, args: list):
        note_data = {
                "sender_id": args[0],
                "game_id": args[1],
                "fleet_proof": args[2]
            }
        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_proof"])

        self.battle_ground_verifier()

        os.remove(f'self.temp_dir}/proof.json')

        
    # Fire type note
    def note_type_fire(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "target_player_id": args[2],
                "shot_coordinates": (int(args[3]), int(args[4])),
                "fleet_intact": args[5]
            }
        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_position"])
        
        self.alive_verifier()

        os.remove(f'{self.temp_dir}/proof.json')
        
        print(self.battleship_games.fireShot(note_data["game_id"],note_data["sender_id"],note_data["target_player_id"],note_data["shot_coordinates"]))

    # Report type note
    def note_type_report(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "shooter_id": args[2],
                "shot_coordinates": (int(args[3]), int(args[4])),
                "shot_result": args[5],
                "response_correct": args[6]
            }

        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_position"])
        
        self.shot_verifier()

        os.remove(f'{self.temp_dir}/proof.json')
        print(self.battleship_games.reportShot(note_data["game_id"],note_data["sender_id"],note_data["shooter_id"],note_data["shot_coordinates"],note_data["shot_result"]))

    # Wave type note
    def note_type_wave(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.waveTurn(note_data["game_id"],note_data["sender_id"]))

    # Claim type note
    def note_type_claim(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "fleet_intact": args[2]
            }

        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_position"])
        
        self.alive_verifier()

        os.remove(f'{self.temp_dir}/proof.json')
        
        print(self.battleship_games.claimVictory(note_data["game_id"],note_data["sender_id"]))
        # Perform actions for Claim Victory note

    # Request Player type note
    def note_type_requestPlayer(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.requestPlayer(note_data["game_id"]))

    # Request Turn type note
    def note_type_requestTurn(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.requestTurn(note_data["game_id"]))

    # Request Games Names type note
    def note_type_requestGamesNames(self, args: list):
        print(self.battleship_games.games.keys())

    # Note factory
    def handle_note(self, note):
        """Handle different types of notes"""
        note_type, *args = note.split('$')
        note_type.lower()
        note_type_handler = self.note_types.get(note_type)

        if note_type_handler is not None:
            note_type_handler(args)
        else:
          print("Unknown note type:", note_type)  

   

if __name__ == '__main__':
    server = BatleshipServer()
    server.connect()
    while True:
        server.handle_note(server.receive())
    server.disconnect()

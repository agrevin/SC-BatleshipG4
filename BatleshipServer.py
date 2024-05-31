import socket
import os
import json
import subprocess
import shutil
import time
from BatleshipServerClasses import BatleshipGames
from ProofingSetupConfigFile import LaunchProofSetup





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
            "requestGamesNames": self.note_type_requestGamesNames,
            "proveAlive": self.note_type_proveAlive,
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

        self.move_Keys()


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

        #print(f"Executing command: {verify_command}")

        try:
            # Execute the compute-witness command
            verify_process = subprocess.run(verify_command, shell=True, check=True, capture_output=True)
            output_lines = verify_process.stdout.decode().splitlines()
            
            if "PASSED" in output_lines[-1]:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return False
            

    def shot_verifier(self):
        verify_command = f'zokrates verify -j {self.temp_dir}/proof.json -v {self.shot_proof_dir}/verification.key'

        #print(f"Executing command: {verify_command}")

        try:
            # Execute the compute-witness command
            verify_process = subprocess.run(verify_command, shell=True, check=True, capture_output=True)
            output_lines = verify_process.stdout.decode().splitlines()
            print(f"Output: {verify_process.stdout.decode()}")
            if "PASSED" in output_lines[-1]:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
    

    def battle_ground_verifier(self):
        verify_command = f'zokrates verify -j {self.temp_dir}/proof.json -v {self.field_proof_dir}/verification.key'

        #print(f"Executing command: {verify_command}")

        try:
            # Execute the compute-witness command
            verify_process = subprocess.run(verify_command, shell=True, check=True, capture_output=True)
            #print(f"Output: {verify_process.stdout.decode()}")
            output_lines = verify_process.stdout.decode().splitlines()
            if "PASSED" in output_lines[-1]:
                return True
            else:
                return False
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
            
        
        if self.battle_ground_verifier():
            
            with open(f'{self.temp_dir}/proof.json') as f:
                proof = json.load(f)

            proofHash = proof['inputs']

            print(self.battleship_games.createGame(note_data["game_id"],note_data["sender_id"],proofHash))
            print("\n")

        os.remove(f'{self.temp_dir}/proof.json')

        
    # Join type note
    def note_type_join(self, args: list):
        note_data = {
                "sender_id": args[0],
                "game_id": args[1],
                "fleet_proof": args[2]
            }
        
        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_proof"])
            

        if self.battle_ground_verifier():
            
            with open(f'{self.temp_dir}/proof.json') as f:
                proof = json.load(f)

            proofHash = proof['inputs']

            print(self.battleship_games.joinGame(note_data["game_id"],note_data["sender_id"],proofHash))
            print("\n")

        os.remove(f'{self.temp_dir}/proof.json')

        
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
            f.write(note_data["fleet_intact"])
        
        if self.alive_verifier():
            print(self.battleship_games.fireShot(note_data["game_id"],note_data["sender_id"],note_data["target_player_id"],note_data["shot_coordinates"]))
            print("\n")
        
        os.remove(f'{self.temp_dir}/proof.json')
            


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
            f.write(note_data["response_correct"])
        
        if self.shot_verifier():
            print(self.battleship_games.reportShot(note_data["game_id"],note_data["sender_id"],note_data["shooter_id"],note_data["shot_coordinates"],note_data["shot_result"]))
            print("\n")

        os.remove(f'{self.temp_dir}/proof.json')
        

    # Wave type note
    def note_type_wave(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.waveTurn(note_data["game_id"],note_data["sender_id"]))
        print("\n")

    # Claim type note
    def note_type_claim(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "fleet_intact": args[2]
            }

        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_intact"])
        
        if self.alive_verifier():
            print(self.battleship_games.claimVictory(note_data["game_id"],note_data["sender_id"]))
            print("\n")

        os.remove(f'{self.temp_dir}/proof.json')
        

    # Request Player type note
    def note_type_requestPlayer(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.requestPlayer(note_data["game_id"]))
        print("\n")

    # Request Turn type note
    def note_type_requestTurn(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.requestTurn(note_data["game_id"]))
        print("\n")

    def note_type_proveAlive(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "fleet_intact": args[2]
            }

        with open(f'{self.temp_dir}/proof.json','w') as f:
            f.write(note_data["fleet_intact"])
        
        if self.alive_verifier():
            print(self.battleship_games.proofAlive(note_data["game_id"],note_data["sender_id"]))
            print("\n")

        os.remove(f'{self.temp_dir}/proof.json')

    # Request Games Names type note
    def note_type_requestGamesNames(self, args: list):
        games_list = list(self.battleship_games.games.keys())
        if games_list:
            print("Available Battleship Games:")
            for i, game_name in enumerate(games_list, 1):
                print(f"{i}. {game_name}")
        else:
            print("No available games.")

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

   
    def move_Keys(self):

        current_dir = os.getcwd()
        BattleGroundProofDirect = f'{current_dir}/BattleGround_proof_v2/verification.key'
        AliveProofDirect = f'{current_dir}/AliveProof/verification.key'
        ShotProofDirect = f'{current_dir}/Shot_proof/verification.key'

        # Target paths
        field_proof_target = f'{self.field_proof_dir}/verification.key'
        alive_proof_target = f'{self.alive_proof_dir}/verification.key'
        shot_proof_target = f'{self.shot_proof_dir}/verification.key'

        # Move files if they do not already exist in the target locations
        if not os.path.exists(field_proof_target):
            shutil.move(BattleGroundProofDirect, field_proof_target)
            print(f"Moved {BattleGroundProofDirect} to {field_proof_target}")
        else:
            print(f"File already exists at {field_proof_target}")

        if not os.path.exists(alive_proof_target):
            shutil.move(AliveProofDirect, alive_proof_target)
            print(f"Moved {AliveProofDirect} to {alive_proof_target}")
        else:
            print(f"File already exists at {alive_proof_target}")

        if not os.path.exists(shot_proof_target):
            shutil.move(ShotProofDirect, shot_proof_target)
            print(f"Moved {ShotProofDirect} to {shot_proof_target}")
        else:
            print(f"File already exists at {shot_proof_target}")

        time.sleep(2)
        os.system('clear')






if __name__ == '__main__':
    original_direct = os.getcwd()
    print("Do you want to compile and setup")
    answer = input("1. Yes\n2. No\n")
    if answer == "1":
        startSetup = LaunchProofSetup()
    os.chdir(original_direct)
    server = BatleshipServer()
    server.connect()
    while True:
        server.handle_note(server.receive())
    server.disconnect()

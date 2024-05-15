import random
import os
import subprocess
import json
import sys
import socket
import time 


class BatleshipClient:
    """Class for a Batleship client"""

    def __init__(self, host: str = 'localhost', port: int = 12345, game_id: str = '',player_id: int = 0):
        """Constructor"""

        #Http stuff
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

        #Game stuff
        self.boats = {'Carrier': 5,
                      'Battleship': 4,
                      'Destroyer': 3,
                      'Cruiser1': 2,
                      'Cruiser2': 2,
                      'Submarine1': 1,
                      'Submarine2': 1}
        self.field: list = [] # can be changed to class
        self.game_id: str = game_id
        self.player_id =  player_id
        self.players_in_game = {}
        self.hash = []

        if self.game_id != -1:
            self.create_direct()
        self.connect()

    def create_direct(self):

        self.proof_dir: str = f"{os.getcwd()}/{self.game_id}{random.randint(0, 2**16 - 1)}"
        self.field_proof_dir = f"{self.proof_dir}/field"
        self.alive_proof_dir = f"{self.proof_dir}/alive"
        self.shot_proof_dir = f"{self.proof_dir}/shot"
        os.makedirs(self.proof_dir, exist_ok=True)
        os.makedirs(self.field_proof_dir, exist_ok=True)
        os.makedirs(self.alive_proof_dir, exist_ok=True)
        os.makedirs(self.shot_proof_dir, exist_ok=True)
    

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
        self.field = _field
        
    def battleGoundProof(self):
        #generate random nonce from 0 to 2^16-1
        self.field_nonce = random.randint(0, 2**16 - 1)

        #generate proof from zokrates file
        flat_list = [item for sublist in self.field for item in sublist]
        zokdir = f'{os.getcwd()}/BattleGround_proof'
        compute_witness_command = f'zokrates compute-witness -s {zokdir}/abi.json -i {zokdir}/out -o {self.field_proof_dir}/witness -a {self.field_nonce} {" ".join(map(str, flat_list))}'
        generate_proof_command = f'zokrates generate-proof -i {zokdir}/out -j {self.field_proof_dir}/proof.json -p {zokdir}/proving.key -w {self.field_proof_dir}/witness'

        print(f"Executing command: {compute_witness_command}")
        # Execute the commands using subprocess

        try:
            # Execute the compute-witness command
            compute_witness_process = subprocess.run(compute_witness_command, shell=True, check=True, capture_output=True)
            #print(f"Output: {compute_witness_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")  
    
        print(f"Executing command: {generate_proof_command}")
        # Execute the commands using subprocess
        try:
            
            #This cannot be like this, we need to check the output of the stdout to check if there was any problem

            witness_file_path = f"{self.field_proof_dir}/witness"

            while not os.path.exists(witness_file_path):
                time.sleep(1)

            generate_proof_process = subprocess.run(generate_proof_command, shell=True, check=True, capture_output=True)
            #print(f"Output: {generate_proof_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")          
        

        with open(f'{self.field_proof_dir}/proof.json') as f:
            proof = json.load(f)

        
        proofHash = proof['inputs']

        self.hash = proofHash[:]
        








    def join_game(self, label: str ,game_id: str):
        """Join a game"""

        self.game_id = game_id
        self.place_boats()
        self.battleGoundProof()
        with open(f'{self.field_proof_dir}/proof.json') as f:
            proof = json.load(f)
        print(proof)
        self.send(f'{label}${self.player_id}${game_id}${proof}')



    def wave_turn(self):
        """Wave the turn"""
        self.send(f'wave${self.game_id}${self.player_id}')

    def fire_shot(self):
        """Fire a shot"""
        print("Do you wish to see game's players?")
        see_players = input("1. Yes\n2. No\n")
        if see_players == '1':
            self.send(f'requestPlayer${self.game_id}${self.player_id}')
        
        target = input('Enter the target player id: ')
        x, y = input('Enter the x(0-9), y(0-9): ').split()
        self.send(f'fire${self.game_id}${self.player_id}${target}${x}${y}$FaltaAProof')

    def report_shot(self):
        """Report a shot"""
        print("Do you wish to see game's players?")
        see_players = input("1. Yes\n2. No\n")
        if see_players == '1':
            self.send(f'requestPlayer${self.game_id}${self.player_id}')
        
        target = input('Enter the attacker player id: ')
        x, y = input('Enter the x(0-9), y(0-9): ').split()
        result = input('Enter the result (HIT, MISS, SUNK): ')
        self.send(f'report${self.game_id}${self.player_id}${target}${x}${y}${result}$FaltaAProof')

    def claim_victory(self):
        """Claim victory"""
        self.send(f'claim${self.game_id}${self.player_id}$FaltaAProof')

    def see_Players(self):
        self.send(f'requestPlayer${self.game_id}${self.player_id}')
        print("Do you wish to add the info of a new player?")
        add_info = input("1. Yes\n2. No\n")
        if add_info == '1':
            print("Input the Players id")
            players_id = input()
            self.players_in_game[players_id] = 0

    def see_Turn(self):
        self.send(f'requestTurn${self.game_id}${self.player_id}')
    
    def increase_shot_counter(self):
        print("To what player do you wish to increase the shot counter")
        player_to_increase = input()
        if player_to_increase not in self.players_in_game:
            print("That player isnt currently in your game")
        
        self.players_in_game[player_to_increase] = self.players_in_game[player_to_increase] + 1
    
    def add_players_info(self):
        print("What players info do you wish to add")
        player_new_info = input()
        self.players_in_game[player_new_info] = 0

    def see_my_game_players_info(self):
        print("Your game player info is:\n")
        for key, value in self.players_in_game.items():
            print(f"Player '{key}' as received '{value}' shots.")
    def clean_dir(self):
        """Remove the proof directory"""
        os.system(f'rm -rf {self.proof_dir}')

    def start_game(self):
        """Start the game"""

        action_dispatcher = {
            "1": self.wave_turn,
            "2": self.fire_shot,
            "3": self.report_shot,
            "4": self.claim_victory,
            "5": self.see_Players,
            "6": self.see_Turn,
            "7": self.increase_shot_counter,
            "8": self.add_players_info,
            "9": self.see_my_game_players_info,
            "10": lambda: (self.disconnect(), self.clean_dir(), exit())
        }

        while(True):
            print("Decide action:")
            action = input("1. Wave turn\n2. Fire shot\n3. Report shot\n4. Claim victory\n5. See Players in your game\n6. See whose turn is it\n7. Increase shot counter\n8. Add a player info\n9. See your game players status\n10. Exit\n")

            result = action_dispatcher.get(action)
            if result is not None:
                result()
            else:
                print("Invalid action selected")
                continue


if __name__ == '__main__':
    print("Choose a game mode:")
    game_mode = input("1. Create a game\n2. Join a game\n")
    if game_mode == '1':
        print("Choose a game id:")
        game_id = input()
        print("Choose your id:")
        player_id = input()
        client = BatleshipClient(game_id=game_id, player_id=player_id)
        client.join_game("create",game_id)
        client.start_game()

    elif game_mode == '2':
        print("Choose your id:")
        player_id = input()
        client = BatleshipClient(game_id=-1, player_id=player_id)
        print("Do you wish to see the games in progress?")
        see_games = input("1. Yes\n2. No\n")
        if see_games == '1':
            client.send(f'requestGamesNames')
        print("Choose a game id:")
        game_id = input()
        client.game_id  = game_id
        client.join_game("join",game_id)
        #To Do: interrupt if error in joining.
        client.create_direct()
        client.start_game()
    else:
        print("Invalid game mode selected")

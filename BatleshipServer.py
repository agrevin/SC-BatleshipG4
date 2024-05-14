import socket
import os
import json
import re
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
            "claim": self.note_type_claim
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

    def receive(self):
        """Receive a message from the client"""
        return self.socket.recv(1024).decode()
    

    def note_type_create(self, args: list):
        note_data = {
            "sender_id": args[0],
            "game_id": args[1],
            "fleet_position": args[2]
        }


        #if Correct
        self.battleship_games.createGame(note_data["game_id"],note_data["sender_id"])

    def note_type_join(self, args: list):
        note_data = {
                "sender_id": args[0],
                "game_id": args[1],
                "fleet_proof": args[2]
            }

        self.battleship_games.joinGame(note_data["game_id"],note_data["sender_id"])

    def note_type_fire(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "target_player_id": args[2],
                "shot_coordinates": (int(args[3]), int(args[4])),
                "fleet_intact": args[5]
            }
            
        print(self.battleship_games.fireShot(note_data["game_id"],note_data["sender_id"],note_data["target_player_id"],note_data["shot_coordinates"]))

    def note_type_report(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "shooter_id": args[2],
                "shot_coordinates": (int(args[3]), int(args[4])),
                "shot_result": args[5],
                "response_correct": args[6]
            }
            
        print(self.battleship_games.reportShot(note_data["game_id"],note_data["sender_id"],note_data["shooter_id"],note_data["shot_coordinates"],note_data["shot_result"]))

    def note_type_wave(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1]
            }
            
        print(self.battleship_games.waveTurn(note_data["game_id"],note_data["sender_id"]))

    def note_type_claim(self, args: list):
        note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "fleet_intact": args[2]
            }
            
        print(self.battleship_games.claimVictory(note_data["game_id"],note_data["sender_id"]))
        # Perform actions for Claim Victory note


    

    def handle_note(self, note):
        """Handle different types of notes"""
        note_type, *args = note.split('$')
        for arg in args:
            print(arg)
        note_type.lower()
        note_type_handler = self.note_types.get(note_type)

        if note_type_handler is not None:
            note_type_handler(args)
        else:
          print("Unknown note type:", note_type)  


        #if note_type == "create":
        #    
        #    note_data = {
        #        "sender_id": args[0],
        #        "game_id": args[1],
        #        "fleet_position": args[2]
        #    }
        #    #verify battleground proof
        #    
        #    #if correct 
        #    self.battleship_games.createGame(note_data["game_id"],note_data["sender_id"])
            
        #elif note_type == "join":
        #    
        #    note_data = {
        #        "sender_id": args[0],
        #        "game_id": args[1],
        #        "fleet_proof": args[2]
        #    }
        #    self.battleship_games.joinGame(note_data["game_id"],note_data["sender_id"])

        #elif note_type == "fire":
        #    
        #    note_data = {
        #        "game_id": args[0],
        #        "sender_id": args[1],
        #        "target_player_id": args[2],
        #        "shot_coordinates": (int(args[3]), int(args[4])),
        #        "fleet_intact": args[5]
        #    }
        #    
        #    print(self.battleship_games.fireShot(note_data["game_id"],note_data["sender_id"],note_data["target_player_id"],note_data["shot_coordinates"]))

        #elif note_type == "report":
        #    
        #    note_data = {
        #        "game_id": args[0],
        #        "sender_id": args[1],
        #        "shooter_id": args[2],
        #        "shot_coordinates": (int(args[3]), int(args[4])),
        #        "shot_result": args[5],
        #        "response_correct": args[6]
        #    }
        #    
        #    print(self.battleship_games.reportShot(note_data["game_id"],note_data["sender_id"],note_data["shooter_id"],note_data["shot_coordinates"],note_data["shot_result"]))
            

        #elif note_type == "wave":
        #    
        #    note_data = {
        #        "game_id": args[0],
        #        "sender_id": args[1]
        #    }
        #    
        #    print(self.battleship_games.waveTurn(note_data["game_id"],note_data["sender_id"]))
            
        #elif note_type == "claim":
        #    # Handle Claim Victory note
        #    note_data = {
        #        "game_id": args[0],
        #        "sender_id": args[1],
        #        "fleet_intact": args[2]
        #    }
        #    
        #    print(self.battleship_games.claimVictory(note_data["game_id"],note_data["sender_id"]))
        #    # Perform actions for Claim Victory note

        #else:
        #    print("Unknown note type:", note_type)

if __name__ == '__main__':
    server = BatleshipServer()
    server.connect()
    while True:
        server.handle_note(server.receive())
    server.disconnect()

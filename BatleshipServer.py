import socket
from BatleshipServerClasses import BatleshipGames
class BatleshipServer:
    """Class for a Batleship server"""

    def __init__(self, host: str = 'localhost', port: int = 12345):
        """Constructor"""
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.battleship_games = BatleshipGames()

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
    

    def handle_note(self, note):
        """Handle different types of notes"""
        note_type, *args = note.split(',')
        note_type.lower()
        if note_type == "create":
            
            note_data = {
                "sender_id": args[0],
                "game_id": args[1],
                "fleet_position": args[2:]
            }
            print("Received Create Game note:", note_data)
            
            #verify battleground proof

            
            #if correct 

            self.battleship_games.createGame(game_id)
            
        elif note_type == "join":

            note_data = {
                "sender_id": args[0],
                "game_id": args[1],
                "fleet_position": args[2:]
            }
            print("Received Join Game note:", note_data)

        elif note_type == "fire":
            
            note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "target_player_id": args[2],
                "shot_coordinates": (int(args[3]), int(args[4])),
                "fleet_intact": args[5]
            }
            print("Received Fire one shot note:", note_data)
            

        elif note_type == "report":
            
            note_data = {
                "game_id": args[0],
                "sender_id": args[1],
                "shooter_id": args[2],
                "shot_coordinates": (int(args[3]), int(args[4])),
                "shot_result": args[5],
                "response_correct": args[6]
            }
            print("Received Report on Shot note:", note_data)
            

        elif note_type == "wave":
            
            note_data = {
                "type": note_type,
                "game_id": args[0],
                "sender_id": args[1]
            }
            print("Received Wave Turn note:", note_data)
            
        elif note_type == "claim":
            # Handle Claim Victory note
            note_data = {
                "type": note_type,
                "game_id": args[0],
                "sender_id": args[1],
                "fleet_intact": args[2]
            }
            print("Received Claim Victory note:", note_data)
            # Perform actions for Claim Victory note

        else:
            print("Unknown note type:", note_type)
if __name__ == '__main__':
    server = BatleshipServer()
    server.connect()
    while True:
        print(server.receive())
    server.disconnect()

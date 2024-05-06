class Player:
    """Class for a Player"""  
    def __init__(self, name: str):
        """Constructor"""
        self.name = name
        self.fieldHash = -1
        self.id = -1




class Game:
    """Class for a Batleship Game"""
    def __init__(self, number: int):
        """Constructor"""
        self.number = number
        self.players = []   
        self.turn = []
    
    def addPlayer(self, player: str):
        """Add a player to the game"""
        newPlayer = Player(player) 
        self.players.append(newPlayer)




class BatleshipGames:
    """Class for a Batleship Games"""

    def __init__(self):
        """Constructor"""
        self.games = {}
        


    def createGame(self, gametitle: str):
        """Create a new game""" 
        self.games[gametitle] = Game(gametitle)




    def joinGame(self, gametitle: str, player: str):
        """Join a game""" 
        self.games[gametitle].addPlayer(player)


    def receive(self):
        """Receive a message from the client"""
        return self.socket.recv(1024).decode()
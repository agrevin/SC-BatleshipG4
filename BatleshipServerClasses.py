class Player:
    """Class for a Player"""  
    def __init__(self, name: int):
        """Constructor"""
        self.name = name
        self.fieldHash = -1




class Game:
    """Class for a Batleship Game"""
    def __init__(self, number: int, firstPlayerId: int):
        """Constructor"""
        self.number = number
        self.players = []
        addPlayers(firstPlayerId)   
        self.turn = []
        self.turn.append(firstPlayerId)
    
    def addPlayer(self, player: int):
        """Add a player to the game"""
        newPlayer = Player(player) 
        self.players.append(newPlayer.name)

    
    def fireShotInGame(self, gametitle: int, shootingPlayer :  int, targettingPlayer: int, shotCoords [2]: int) -> str:
        
        if shootingPlayer not in self.players or targettingPlayer not in self.players:
            return f"In game {self.number}: Shooting Player {shootingPlayer} or Targetting Player {targettingPlayer} does not exist in the game"

        if shootingPlayer = self.turn[0]:
           self.turn.append(self.turn[0])
           self.turn.pop(0)
           self.turn.insert(0,targettingPlayer)
           #Print whose turn is next
           return f" In game {self.number}: Shooting Player: {shootingPlayer} shot Targetting Player: {targettingPlayer} at x: {shotCoords[0]} and y: {shotCoords[1]}"

        return f"In game {self.number}: It is not SShooting Player: {shootingPlayer} turn "


class BatleshipGames:
    """Class for a Batleship Games"""

    def __init__(self):
        """Constructor"""
        self.games = {}
        


    def createGame(self, gametitle: int) -> str:
        """Create a new game""" 
        # nao esquecer sender id
        self.games[gametitle] = Game(gametitle)




    def joinGame(self, gametitle: int, player: int) -> str:
        """Join a game""" 
        if gametitle in self.games:
            return self.games[gametitle].addPlayer(player)


    def fireShot(self, gametitle: int, shootingPlayer :  int, targettingPlayer: int, shotCoords [2]: int)-> str :
        """Fire a shot"""
        
        if gamtitle in self.games.keys:
            return self.games[gametitle].fireShotInGame()

        
    def reportShot(self, gametitle: int, shootingPlayer: int, targettingPlayer: int, shotCoords [2]: int, result: str)-> str :
    
    self.reportShot() 
        
        
        















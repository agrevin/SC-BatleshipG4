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
        newPlayer = Player(firstPlayerId) 
        self.players.append(newPlayer.name)
        self.turn = []
        self.turn.append(firstPlayerId)
        self.waveturn = {} 
        self.waveturn[firstPlayerId] = False     

  
    def addPlayer(self, player: int):
        """Add a player to the game"""
        newPlayer = Player(player) 
        self.players.append(newPlayer.name)
        self.waveturn[player] = False
        print(self.players)

    
    def fireShotInGame(self, shootingPlayer :  int, targettingPlayer: int, shotCoords: list) -> str:
        
        """Verify is players actually exist"""
        if shootingPlayer not in self.players or targettingPlayer not in self.players:
            return f"In game {self.number}: Shooting Player {shootingPlayer} or Targetting Player {targettingPlayer} does not exist in the game"
        
        """Verify if it is players turn"""
        if shootingPlayer != self.turn[0]:
            return f"In game {self.number}: It is not Shooting Player: {shootingPlayer} turn "

        self.turn.append(self.turn[0])
        self.turn.pop(0)
        self.turn.insert(0,targettingPlayer)
       #Print whose turn is next
        return f"In game {self.number}: Shooting Player: {shootingPlayer} shot Targetting Player: {targettingPlayer} at x: {shotCoords[0]} and y: {shotCoords[1]}"

        

    def reportShotInGame(self, reportingPlayer: int, shootingPlayer: int, shotCoords: list, result: str)-> str :
       if reportingPlayer not in self.players or shootingPlayer not in self.players:
            return f"In game {self.number}: Reporting Player {reportingPlayer} or Shooting Player {shootingPlayer} does not exist in the game"
        
       if reportingPlayer != self.turn[0]:
            return f"In game {self.number}: It is not Reporting Player: {shootingPlayer} turn " 

       return f"In game {self.number}: Reporting Player: {shootingPlayer} is reporting a {result} at x: {shotCoords[0]} and y: {shotCoords[1]} from shot from Shooting Player: {shootingPlayer}"

    
    def waveTurnInGame(self, waveTurnPlayer: int)-> str:
       if waveTurnPlayer not in self.players:
            return f"In game {self.number}: Player who wants to wave turn: {waveTurnPlayer} does not exist."

       if waveTurnPlayer != self.turn[0]:
            return f"In game {self.number}: Player: {waveTurnPlayer} cannot wave its turn because it is not their turn."
       self.turn.append(self.turn[0])
       self.turn.pop(0)
       self.waveturn[waveTurnPlayer] = True
       return f"In game {self.number}: It is Player : {self.turn[0]} turn."

    def checkVcitoryClaim(self, claimVictoryPlayer:int )-> str:
        if False in self.waveturn.values():
            return f"In game {self.number}: The Player : {claimVictoryPlayer} Won."
        
        

class BatleshipGames:
    """Class for a Batleship Games"""

    def __init__(self):
        """Constructor"""
        self.games = {}
        


    def createGame(self, gametitle: int, player : int ) -> str:
        """Create a new game""" 
        # nao esquecer sender id
        self.games[gametitle] = Game(gametitle,player)
        
        return 




    def joinGame(self, gametitle: int, player: int) -> str:
        """Join a game""" 
        if gametitle in self.games:
            return self.games[gametitle].addPlayer(player)


    def fireShot(self, gametitle: int, shootingPlayer :  int, targettingPlayer: int, shotCoords: list)-> str :
        """Fire a shot"""
        
        if gametitle in self.games:
            return self.games[gametitle].fireShotInGame(shootingPlayer,targettingPlayer, shotCoords)

        
    def reportShot(self, gametitle: int, reportingPlayer: int, shootingPlayer: int, shootCoords: list, result: str)-> str :
        
        """Report shot"""

        if gametitle in self.games:
            return self.games[gametitle].reportShotInGame(reportingPlayer,shootingPlayer,shootCoords, result)
        
     
    def waveTurn(self, gametitle: int, waveTurnPlayer: int)-> str:
        if gametitle in self.games:
           return self.games[gametitle].waveTurnInGame(waveTurnPlayer)

        
    def claimVictory(self, gametitle: int, claimVictoryPlayer: int)-> str:
        if gametitle in self.games:
           return self.games[gametitle].checkVcitoryClaim(claimVictoryPlayer)
        
        















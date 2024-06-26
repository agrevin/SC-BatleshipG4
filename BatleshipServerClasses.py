import time

time_to_proof_alive = 30


class Player:
    """Class for a Player"""  
    def __init__(self, name: int,hashes: list):
        """Constructor"""
        self.name = name
        self.fieldHash = hashes




class Game:
    """Class for a Batleship Game"""
    def __init__(self, title: str, firstPlayerId: int , hashes: list):
        """Constructor"""
        self.title = title
        self.players = []
        newPlayer = Player(firstPlayerId,hashes) 
        self.fullPlayers = {}
        self.fullPlayers[newPlayer.name] = newPlayer

        self.players.append(newPlayer.name)
        self.turn = []
        self.turn.append(firstPlayerId)
        self.hasReported = {}
        self.hasReported[firstPlayerId] = True
        self.playerClaimedVictory = None
        self.victoryClock = None
        self.gameHasEnded = False

  
    def addPlayer(self, player: int,hashes: list)->str:
        if not self.gameHasEnded and (self.victoryClock == None or time.time() - self.victoryClock < time_to_proof_alive):
            
            if self.playerClaimedVictory != None:
                self.playerClaimedVictory = None
                self.victoryClock = None

            """Add a player to the game"""
            if player in self.players:
                return f"In the game '{self.title}': Player: '{player}' is already in the game."
            
            newPlayer = Player(player,hashes) 
            self.fullPlayers.append(newPlayer)

            self.players.append(newPlayer.name)
            self.turn.append(player)
            self.hasReported[player] = True
            return f"In the game '{self.title}': the Player: '{newPlayer.name}' has joined."
        else:
            self.gameHasEnded = True
            return f"In the game '{self.title}': Game has ended. Player: '{player}' cannot join."


    def fireShotInGame(self, shootingPlayer :  int, targettingPlayer: int, shotCoords: list) -> str:
        
        if not self.gameHasEnded and (self.victoryClock == None or time.time() - self.victoryClock < time_to_proof_alive):

            if self.playerClaimedVictory != None:
                self.playerClaimedVictory = None
                self.victoryClock = None


            """Verify is players actually exist"""
            if shootingPlayer not in self.players or targettingPlayer not in self.players:
                return f"In the game {self.title}: Shooting Player {shootingPlayer} or Targetting Player {targettingPlayer} does not exist in the game"
            
            """Verify if it is players turn"""
            if shootingPlayer != self.turn[0]:
                return f"In the game {self.title}: It is not Shooting Player: {shootingPlayer} turn "

            """Verify if shooting player is not shooting itself"""
            if shootingPlayer == targettingPlayer:
                return f"In the game {self.title}: Shooting Player: {shootingPlayer} cannot shoot itself"
            
            """Verify if shooting player has reported the last shot"""
            if self.hasReported[shootingPlayer] == False:
                return f"In the game {self.title}: Shooting Player: {shootingPlayer} has not reported the last shot"
            
            self.hasReported[shootingPlayer] = True
            self.hasReported[targettingPlayer] = False


            self.turn.append(self.turn[0])
            self.turn.pop(0)
            self.turn.remove(targettingPlayer)
            self.turn.insert(0,targettingPlayer)
            #Print whose turn is next
            return f"In the game {self.title}: Shooting Player: {shootingPlayer} shot Targetting Player: {targettingPlayer} at x: {shotCoords[0]} and y: {shotCoords[1]}"
        else:
            self.gameHasEnded = True
            return f"In the game {self.title}: Game has ended."

        
    def reportShotInGame(self, reportingPlayer: int, shootingPlayer: int, shotCoords: list, result: str,hashes : list)-> str :
        if not self.gameHasEnded and (self.victoryClock == None or time.time() - self.victoryClock < time_to_proof_alive):

            if self.playerClaimedVictory != None:
                self.playerClaimedVictory = None
                self.victoryClock = None
            
            if reportingPlayer not in self.players or shootingPlayer not in self.players:
                return f"In the game {self.title}: Reporting Player {reportingPlayer} or Shooting Player {shootingPlayer} does not exist in the game"
            
            if reportingPlayer != self.turn[0]:
                return f"In game {self.title}: It is not Reporting Player: {reportingPlayer} turn " 

            if self.hasReported[reportingPlayer] == True:   
                return f"In the game {self.title}: Reporting Player: {reportingPlayer} has already reported the last shot"

            self.hasReported[reportingPlayer] = True
            return f"In the game {self.title}: Reporting Player: {reportingPlayer} is reporting a {result} at x: {shotCoords[0]} and y: {shotCoords[1]} from shot from Shooting Player: {shootingPlayer}"
        else:
            self.gameHasEnded = True
            return f"In the game {self.title}: Game has ended."

    
    def waveTurnInGame(self, waveTurnPlayer: int)-> str:
        if not self.gameHasEnded:
            if waveTurnPlayer not in self.players:
                    return f"In the game {self.title}: Player who wants to wave turn: {waveTurnPlayer} does not exist."

            if waveTurnPlayer != self.turn[0]:
                    return f"In the game {self.title}: Player: {waveTurnPlayer} cannot wave its turn because it is not their turn."
                
            if self.hasReported[waveTurnPlayer] == False:   
                return f"In the game {self.title}: WaveTurning Player: {waveTurnPlayer} cannot wave its turn until it has reported the shot"

            print(f"Player: '{waveTurnPlayer}' has decided to wave its turn")
            self.turn.append(self.turn[0])
            self.turn.pop(0)
            return f"In the game {self.title}: It is Player : {self.turn[0]} turn."
        else:
            return f"In the game {self.title}: Game has ended."


    def checkVcitoryClaim(self, claimVictoryPlayer:int )-> str:
            if not self.gameHasEnded and (self.victoryClock == None or time.time() - self.victoryClock < time_to_proof_alive):
                self.playerClaimedVictory = claimVictoryPlayer
                self.victoryClock = time.time() 
                return f"In the game {self.title}: The Player : {claimVictoryPlayer} has claimed victory\n Players have 15s to proof they are alive."
            else:
                self.gameHasEnded = True
                return f"In the game {self.title}: Game has ended."
        

    def proof_alivness(self, player:int)-> str:
        if not self.gameHasEnded:
            if self.playerClaimedVictory == None:
                return f"In the game {self.title}: No player has claimed victory yet."

            if self.playerClaimedVictory == player:
                return f"In the game {self.title}: Player : {player} has claimed victory, so they cannot proof they are alive."

            if time.time() - self.victoryClock < 15:
                self.victoryClock = None
                self.playerClaimedVictory = None
                return f"In the game {self.title}: Player : {player} has proved they are alive.\n Game will continue."   
            
            self.gameHasEnded = True
            return f"In the game {self.title}: Player : {self.playerClaimedVictory} has won the game.\n Game has ended."
        else:
            return f"In the game {self.title}: Game has ended."

class BatleshipGames:
    """Class for a Batleship Games"""

    def __init__(self):
        """Constructor"""
        self.games = {}
        


    def createGame(self, gametitle: str, player : int ,hashes: list) -> str:
        """Create a new game""" 
        # nao esquecer sender id
        self.games[gametitle] = Game(gametitle,player,hashes)
        
        return f"A new game called '{gametitle}' was created."


    def joinGame(self, gametitle: str, player: int,hashes : list) -> str:
        """Join a game""" 
        if gametitle in self.games:
            return self.games[gametitle].addPlayer(player,hashes)

        return f"Game '{gametitle}' does not exist."


    def fireShot(self, gametitle: str, shootingPlayer :  int, targettingPlayer: int, shotCoords: list)-> str :
        """Fire a shot"""
        
        if gametitle in self.games:
            return self.games[gametitle].fireShotInGame(shootingPlayer,targettingPlayer, shotCoords)

        
    def reportShot(self, gametitle: str, reportingPlayer: int, shootingPlayer: int, shootCoords: list, result: str,hashes : list)-> str :
        
        """Report shot"""

        if gametitle in self.games:
            return self.games[gametitle].reportShotInGame(reportingPlayer,shootingPlayer,shootCoords, result,hashes)
        
     
    def waveTurn(self, gametitle: str, waveTurnPlayer: int)-> str:
        """Wave turn"""
        if gametitle in self.games:
           return self.games[gametitle].waveTurnInGame(waveTurnPlayer)

        
    def claimVictory(self, gametitle: str, claimVictoryPlayer: int)-> str:
        """Claim victory"""
        if gametitle in self.games:
           return self.games[gametitle].checkVcitoryClaim(claimVictoryPlayer)


    def requestPlayer(self, gametitle: str)-> str:
        """Request player"""
        return f"The players in the game {gametitle} are : {self.games[gametitle].players}"


    def requestTurn(self, gametitle: str)-> str:
        """Request player"""
        return f"In the game {gametitle}: it is Player : {self.games[gametitle].turn[0]} turn."
    

    def proofAlive(self, gametitle: str, player: int)-> str:
        """Proof Alive"""
        if gametitle in self.games:
            msg_to_return = self.games[gametitle].proof_alivness(player)
            if self.games[gametitle].gameHasEnded:
                del self.games[gametitle]
            return msg_to_return















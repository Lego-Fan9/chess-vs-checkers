from logger import logger

logger_base = 'blackboard.py:'
logger.trace(f'{logger_base} loaded')

class blackboard:
    def __init__(self, sqlManager, boardManager):
        self.sqlManager = sqlManager
        self.boardManager = boardManager
        self.gameBlackboardInternal = {
            "who_starts": self.boardManager.global_data["who_starts"],
            "is_standard": self.boardManager.global_data["is_standard"],
            "start_side_0": self.boardManager.global_data["alive_side_0"],
            "start_side_1": self.boardManager.global_data["alive_side_1"],
            "moves": []
        }
        self.gameContinue = True
    
    def addMove(self, moveData):
        self.gameBlackboardInternal["moves"].append(moveData)
    
    def gameEnded(self):
        self.gameContinue = False
        self.sqlManager.postGameData(self.gameBlackboardInternal)
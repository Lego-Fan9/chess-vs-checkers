from logger import logger

# Make logger message
logger_base = '/dataBuilder/boardMaker.py:'
logger.trace(f'{logger_base} loaded')

class boardManager:
    def __init__(self, data):
        if data["is_standard_board"] == True:
            self.global_data = {
                "sides": [data["side_numeric_0"], data["side_numeric_1"]],
                "alive_side_0": [],
                "alive_side_1": [],
                "is_standard": True,
                "gameEnd": False
            }
            if data["who_starts"] == False:
                import random
                self.global_data["who_starts"] = random.randint(0, 1)
            else: 
                self.global_data["who_starts"] = data["who_starts"]
            self.board = [[False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False],
                          [False, False, False, False, False, False, False, False]]
            for x in data['data']:
                new_data = {
                    "pieceName": x["pieceName"],
                    "unique_id": x["unique_id"],
                    "side_numeric": x["side_numeric"],
                    "pieceMoveIndex": x["pieceMoveIndex"],
                    "is_king": x["is_king"],
                    "can_become_other_on_opponent_side": x["can_become_other_on_opponent_side"],
                    "can_kill_chain": x["can_kill_chain"],
                    "startMoveSpecial": x["startMoveSpecial"],
                    "can_jump": x["can_jump"]
                }
                if x["pieceKillIndex"] == []:
                    new_data["pieceKillIndex"] = x["pieceMoveIndex"]
                else:
                    new_data["pieceKillIndex"] = x["pieceKillIndex"]
                self.board[x["pieceStartY"]][x["pieceStartX"]] = new_data
                alive_side = 'alive_side_' + str(new_data["side_numeric"])
                self.global_data[alive_side].append(new_data["unique_id"])
                logger.info(f'{logger_base} created a "{new_data["pieceName"]}" at "{x["pieceStartX"]}, {"pieceStartY"}" with unique_id "{new_data["unique_id"]}"')
                new_data = {}
            # Next line displays board, but was too spammy
            # logger.trace(f'{logger_base} created board: {self.board}')
            logger.info(f'{logger_base} created new board')
        else:
            raise AttributeError(f"{logger_base}boardManager.__init__(): Invalid board configuation")
    
    def register_blackboard(self, blackboard):
        self.blackboard = blackboard

    def displayBoard(self):
        if self.global_data["is_standard"] == True:
            for row in self.board:
                print(' '.join([str(piece["unique_id"]) if piece else '.' for piece in row]))
        else:
            raise AttributeError(f"'{logger_base}boardManager.displayBoard(): Invalid board, cannot display")
        
    def movePiece(self, pieceId, newSpot, oldSpot):
        pieceName = False
        if self.board[oldSpot[0]][oldSpot[1]]["unique_id"] == pieceId:
            pieceName = self.board[oldSpot[0]][oldSpot[1]]["pieceName"]
        else:
            raise AttributeError(f'{logger_base} Couldn\'t find {pieceId} in the board')
        if pieceName == False:
            raise AttributeError(f'{logger_base} Couldn\'t find {pieceId} in the board')
        else: 
            logger.debug(f'{logger_base} found {pieceName} in the board')
        if self.board[newSpot[0]][newSpot[1]] != False:
            raise AttributeError(f'{logger_base} invalid move to {newSpot} it is populated')
        if self.board[newSpot[0]][newSpot[1]] != False:
            raise AttributeError(f'{logger_base} invalid move to {newSpot} internal error with "unique_id"')
        logger.debug(f'{logger_base} all pre-move checks complete and good')
        self.board[newSpot[0]][newSpot[1]] = self.board[oldSpot[0]][oldSpot[1]]
        self.board[oldSpot[0]][oldSpot[1]] = False
        logger.info(f'{logger_base} moved {pieceName} from {oldSpot} to {newSpot}')
        move_data = {
            "pieceName": pieceId, 
            "newSpot": newSpot, 
            "oldSpot": oldSpot,
            "kill": False,
            "currentBoard": self.board,
            "skipTurn": False}
        self.blackboard.addMove(move_data)
        logger.debug(f'{logger_base} added piece to moves list')

    def killPiece(self, pieceId, newSpot, oldSpot):
        pieceName = False
        if self.board[oldSpot[0]][oldSpot[1]]["unique_id"] == pieceId:
            pieceName = self.board[oldSpot[0]][oldSpot[1]]["pieceName"]
        else:
            raise AttributeError(f'{logger_base} Couldn\'t find {pieceId} in the board')
        if pieceName == False:
            raise AttributeError(f'{logger_base} Couldn\'t find {pieceId} in the board')
        else: 
            logger.debug(f'{logger_base} found {pieceName} in the board')
        if self.board[newSpot[0]][newSpot[1]] == False:
            raise AttributeError(f'{logger_base} invalid kill to {newSpot} it is not populated')
        if self.board[newSpot[0]][newSpot[1]]["unique_id"] == pieceId:
            raise AttributeError(f'{logger_base} invalid kill to {newSpot} internal error with "unique_id"')
        logger.trace(f'{logger_base} all pre-move checks complete and good')
        oldPiece = self.board[newSpot[0]][newSpot[1]]
        self.board[newSpot[0]][newSpot[1]] = self.board[oldSpot[0]][oldSpot[1]]
        self.board[oldSpot[0]][oldSpot[1]] = False
        logger.info(f'{logger_base}{oldPiece["unique_id"]} killed by {pieceName} who moved from {oldSpot} to {newSpot}')
        move_data = {
            "pieceName": pieceId, 
            "newSpot": newSpot, 
            "oldSpot": oldSpot,
            "kill": True,
            "currentBoard": self.board,
            "skipTurn": False}
        self.blackboard.addMove(move_data)
        logger.debug(f'{logger_base} added piece to moves list')
        side = oldPiece["side_numeric"]
        if side == 0:
            self.global_data["alive_side_0"].remove(oldPiece["unique_id"])
        elif side == 1:
            self.global_data["alive_side_1"].remove(oldPiece["unique_id"])
        else:
            raise AttributeError(f'{logger_base} error getting {pieceId} side')
        logger.trace(f'{logger_base} removed {oldPiece["unique_id"]} from alive list') 
        if oldPiece["is_king"] == True:
            self.global_data["gameEnd"] = True
            self.blackboard.gameEnded()
            logger.info(f'{logger_base} game is ending')
        if len(self.global_data["alive_side_0"]) <= 0:
            self.global_data["gameEnd"] = True
            self.blackboard.gameEnded()
            logger.info(f'{logger_base} game is ending')
        elif len(self.global_data["alive_side_1"]) <= 0:
            self.global_data["gameEnd"] = True
            self.blackboard.gameEnded()
            logger.info(f'{logger_base} game is ending')

    def skipTurn(self):
        move_data = {
            "pieceName": None, 
            "newSpot": None, 
            "oldSpot": None,
            "kill": None,
            "currentBoard": self.board,
            "skipTurn": True}
        self.blackboard.addMove(move_data)
        logger.debug(f'{logger_base} skipped turn')
from logger import logger
import blackboard
import boardMaker
import moveCheck
import sqlhelper
import json
import random
import time

logger_base = 'main.py:'
logger.trace(f'{logger_base} all modules loaded')

setup_file_path = r'D:\python codes\chessVcheckers\test_3_27_25\chess-vs-checkers\dataBuilder\setup.json'
with open(setup_file_path, 'r') as file:
    setup_data = json.load(file)

boardManager = boardMaker.boardManager(setup_data)
sqlManager = sqlhelper.sqlManager()
blackboard = blackboard.blackboard(sqlManager, boardManager)
boardManager.register_blackboard(blackboard)

logger.trace(f'{logger_base} setup all objects')

def findPiece(piece):
    y_count = 0
    for y in boardManager.board:
        x_count = 0
        for x in boardManager.board[y_count]:
            if boardManager.board[y_count][x_count] == False:
                pass
            elif boardManager.board[y_count][x_count]["unique_id"] == piece:
                return [y_count, x_count]
            x_count += 1
        y_count += 1
    raise KeyError(f'{logger_base} couldn\'t find piece: {piece} in the board')

def get_suggested_moves(side):
    returndata = []
    for piece in boardManager.global_data[side]:
        piecedata = {"piece": piece, "move": False, "type": "none", "special": False}
        returnListAdd = False
        pieceCord = findPiece(piece)
        piecedata["old"] = pieceCord
        boolList, moves, kills, specials = moveCheck.moveCheck(boardManager.board, pieceCord)
        if boolList[1]:
            piecedata["move"] = random.choice(kills)
            piecedata["type"] = "kill"
            returnListAdd = True
        elif boolList[0]:
            piecedata["move"] = random.choice(moves)
            piecedata["type"] = "move"
            returnListAdd = True
        if boolList[2] == True:
            piecedata["special"] = True
        if returnListAdd:
            returndata.append(piecedata)
    return returndata

def get_move(side):
    data = get_suggested_moves(side)
    if data == []:
        return {"type": "none"}
    else:
        return random.choice(data)

def make_move(movedata):
    if movedata["type"] == "kill":
        boardManager.killPiece(movedata["piece"], movedata["move"], movedata["old"])
    elif movedata["type"] == "move":
        boardManager.movePiece(movedata["piece"], movedata["move"], movedata["old"])
    else:
        boardManager.skipTurn()

turnCount = 1
while blackboard.gameContinue:
    make_move(get_move("alive_side_0"))
    print(turnCount)
    turnCount += 1
    make_move(get_move("alive_side_1"))
    print(turnCount)
    turnCount += 1
print('DONE')
print(boardManager.displayBoard())
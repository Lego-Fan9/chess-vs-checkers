from logger import logger
import blackboard
import boardMaker
import moveCheck
import sqlhelper
import json

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
            if boardManager.board[y_count][x_count]["unique_id"] == piece:
                return [y_count, x_count]
            x_count += 1
        y_count += 1
    raise KeyError(f'{logger_base} couldn\'t find piece: {piece} in the board')

def get_all_moves(side):
    returndata = []
    for piece in boardManager.global_data[side]:
        piecedata = {"piece": piece, "moves": [], "kills": [], "specialRemove": False}
        returnListAdd = False
        pieceCord = findPiece(piece)
        boolList, moves, kills, specials = moveCheck.moveCheck(boardManager.board, pieceCord)
        if boolList[0]:
            returnListAdd = True
            piecedata["moves"].append(moves)
        if boolList[1]:
            returnListAdd = True
            piecedata["moves"].append(kills)
            piecedata["kills"].append(kills)
        if boolList[2]:
            piecedata["specialRemove"] = True
        if returnListAdd:
            returndata.append(piecedata)
    return returndata

print(get_all_moves("alive_side_0"))
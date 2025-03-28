from logger import logger

logger_base = "moveCheck.py:"
logger.trace(f'{logger_base} loaded')

def moveCheck(board, pieceCord):
    returnMove = []
    returnKill = []
    returnSpecial = []
    returnBool = [False, False, False]
    piece = board[pieceCord[0]][pieceCord[1]]

    for x in piece["pieceMoveIndex"]:
        try:
            if board[pieceCord + x[0]][pieceCord + x[1]] == False:
                returnMove.append([[pieceCord + x[0]], [pieceCord + x[1]]])
                returnBool[0] = True
        except KeyError as ke:
             logger.trace(f'{logger_base} KeyError {ke} this is probably ok')

    for x in piece["pieceKillIndex"]:
        try:
            if board[pieceCord + x[0]][pieceCord + x[1]] != False:
                if board[pieceCord + x[0]][pieceCord + x[1]]["side_numeric"] == piece["side_numeric"]:
                    pass # Piece is ally
                else:
                    returnKill.append([board[x[pieceCord + 0]], [pieceCord + x[1]]])
                    returnBool[1] = True
        except KeyError as ke:
             logger.trace(f'{logger_base} KeyError {ke} this is probably ok')

    if piece["startMoveSpecial"] != []:
        for x in piece["pieceMoveIndex"]:
            try:
                if board[pieceCord + (x[0] + piece["startMoveSpecial"][0])][pieceCord + (x[1] + ["startMoveSpecial"][1])] == False:
                    returnMove.append([pieceCord + (x[0] + piece["startMoveSpecial"][0])], [pieceCord + (x[1] + ["startMoveSpecial"][1])])
                    returnBool[0] = True
                    returnBool[2] = True
                    returnSpecial.append([pieceCord + (x[0] + piece["startMoveSpecial"][0])], [pieceCord + (x[1] + ["startMoveSpecial"][1])])
            except KeyError as ke:
                logger.trace(f'{logger_base} KeyError {ke} this is probably ok')
    
    return returnBool, returnMove, returnKill, returnSpecial
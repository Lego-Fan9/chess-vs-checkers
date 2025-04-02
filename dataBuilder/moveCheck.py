from logger import logger

logger_base = "moveCheck.py:"
logger.trace(f'{logger_base} loaded')

def moveCheck(board, pieceCord):
    """
    Checks all possible moves, kills, and special moves for a given piece.

    Args:
        board (list): The current state of the board.
        pieceCord (list): The coordinates [y, x] of the piece to check.

    Returns:
        tuple: A tuple containing:
            - boolList (list): [canMove, canKill, hasSpecial].
            - moves (list): List of valid move coordinates.
            - kills (list): List of valid kill coordinates.
            - specials (list): List of special moves (if any).
    """
    y, x = pieceCord
    piece = board[y][x]

    if not piece:
        raise ValueError(f"{logger_base} No piece found at {pieceCord}")

    moves = []
    kills = []
    specials = []
    canMove = False
    canKill = False
    hasSpecial = False

    # Check for special moves
    # Adds the special move to the pieceMoveIndex
    # This pieceMoveIndex is a local clone so it is temporary
    if piece["startMoveSpecial"]:
        specials.append(piece["startMoveSpecial"])
        hasSpecial = True
        piece["pieceMoveIndex"].append(piece["startMoveSpecial"])

    # Check possible moves
    for move in piece["pieceMoveIndex"]:
        newY, newX = y + move[1], x + move[0]
        if 0 <= newY < len(board) and 0 <= newX < len(board[0]):
            if not is_path_blocked(board, pieceCord, [newY, newX]):
                if not board[newY][newX]:  # Empty spot
                    moves.append([newY, newX])
                    canMove = True
            elif piece["can_jump"] == True:
                if not board[newY][newX]:  # Empty spot
                    moves.append([newY, newX])
                    canMove = True

    # Check possible kills
    for kill in piece["pieceKillIndex"]:
        newY, newX = y + kill[1], x + kill[0]
        if 0 <= newY < len(board) and 0 <= newX < len(board[0]):
            if not is_path_blocked(board, pieceCord, [newY, newX]):
                target = board[newY][newX]
                if target and target["side_numeric"] != piece["side_numeric"]:  # Opponent piece
                    kills.append([newY, newX])
                    canKill = True
            elif piece["can_jump"] == True:
                target = board[newY][newX]
                if target and target["side_numeric"] != piece["side_numeric"]:  # Opponent piece
                    kills.append([newY, newX])
                    canKill = True

    boolList = [canMove, canKill, hasSpecial]
    return boolList, moves, kills, specials

def is_path_blocked(board, start, end):
    """
    Checks if the path between two points is blocked for sliding pieces (e.g., queen, rook, bishop).

    Args:
        board (list): The game board.
        start (list): Starting coordinates [y, x].
        end (list): Ending coordinates [y, x].

    Returns:
        bool: True if the path is blocked, False otherwise.
    """
    startY, startX = start
    endY, endX = end

    # If start and end are the same, no need to check
    if start == end:
        return False

    deltaY = endY - startY
    deltaX = endX - startX

    stepY = (deltaY // abs(deltaY)) if deltaY != 0 else 0
    stepX = (deltaX // abs(deltaX)) if deltaX != 0 else 0

    currentY, currentX = startY + stepY, startX + stepX

    # Ensure that the loop will terminate at the end
    while (currentY, currentX) != (endY, endX):
        try:
            if board[currentY][currentX]:  # Path is blocked
                return True
        except IndexError:
            # If out of bounds, treat this as a blocked path
            return True

        currentY += stepY
        currentX += stepX

        # Prevent the loop from getting stuck if somehow the increments
        # are not bringing us closer to the end coordinates
        if (currentY, currentX) == (startY, startX):
            return False

    return False

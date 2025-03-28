from boardMaker import boardManager
import json

filepath = ''
with open(filepath, 'r') as file:
    file = json.load(file)

boardManager = boardManager(file)
boardManager.displayBoard()
from boardMaker import boardManager
import sqlhelper
import json

def makeBoard(filepath):
    with open(filepath, 'r') as file:
        file = json.load(file)
    boardManager = boardManager(file)
    boardManager.displayBoard()

def sqlTestConn():
    sqlManager = sqlhelper.sqlManager()
    sqlManager._get_sql()
    print('done getting sql conn')
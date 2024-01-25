import json

commands = []

def loadConfig():
    global commands
    with open("app/settings/commands.txt", "r") as file:
        commands = json.load(file) # Reading the file
        file.close()

def saveComamnds():
    with open("app/settings/commands.txt", "w") as file:
        strCommands = json.dumps(commands)
        print(strCommands)
        file.write(strCommands)
        file.close()
    
def addCommand(command):
    commands.append(command)
    saveComamnds()
    
def removeCommand(command):
    commands.remove(command)
    saveComamnds()
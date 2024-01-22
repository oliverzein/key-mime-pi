import json

commands = []

def loadConfig():
    with open("app/settings/commands.txt", "r") as file:
        commands = json.load(file) # Reading the file
        file.close()
        return commands
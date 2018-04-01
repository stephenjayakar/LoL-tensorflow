N = 140

import json

FILE = open("static_data/champions.json")
championJSON = json.load(FILE)
FILE.close()
championJSON = championJSON["data"]
championTable = {}

FILE = open("static_data/championFeatures.json", "r")
championFeatures = json.load(FILE)
FILE.close()


for name in championJSON.keys():
    key = int(championJSON[name]['id'])
    championTable[key] = name

def id_to_name(x: int) -> str:
    return championTable[x]

# coverts champion name to 8 bit representation
def name_to_index(name: str) -> list:
    return championFeatures[name]

# this is pretty inefficient, but whatever
def index_to_name(x: int) -> str:
    for name in championFeatures.keys():
        if x == championFeatures[name]:
            return name

# given a list of names, and converts to features
def team_to_features(team: list) -> list:
    returnTeam = [0] * N
    for name in team:
        index = name_to_index(name)
        returnTeam[index] = 1
    return returnTeam
    # binaries = []
    # for name in team:
    #     binaries.append(championFeatures[name])
    # binaries.sort(key=lambda x: x[0])
    # binaries = list(map(lambda x: x[1:], binaries))
    # for i in range(4):
    #     binaries[0].extend(binaries[i])
    # return binaries[0]
    

# code to create initial conversion    
if __name__ == "__main__":
    print("not running main because commented")
    # dictionary = {}
    # counter = 0
    # names = championJSON.keys()
    # names = list(names)
    # names.sort()
    # for name in names:
    #     dictionary[name] = counter
    #     counter += 1
    # FILE = open("static_data/championFeatures.json", 'w')
    # FILE.write(json.dumps(dictionary))
    # FILE.close()
                              

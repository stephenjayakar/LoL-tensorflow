import champions
import json

""" where the magic happens
we convert the 10 champions in the match
to 2 40 bit values, where each value 
is made up of 8 bit values indicating the champion a 
player is playing.  The 8 bit values within a team are 
sorted with lower ID first.
The last value determines which team won: 0 is red, 1 is blue
"""
def match_to_features(match: dict):
    champsTeamRed = []
    champsTeamBlue = []
    for p in match["participants"]:
        name = champions.id_to_name(int(p['championId']))
        if p['teamId'] == 100:
            champsTeamRed.append(name)
        else:
            champsTeamBlue.append(name)
    features = champions.team_to_features(champsTeamRed) + champions.team_to_features(champsTeamBlue)
    win = match['teams'][0]['win'] == 'Win'
    win = int(win)
    win = [win, 1 - win]
    features += win
    return features
        
        
class Data:
    index = 0
    tx = None
    ty = None

    px = None
    py = None
    
    def __init__(self):
        self.tx = []
        self.ty = []
        for i in range(1, 200):
            data = open("big_data/matches{}.json".format(i), 'r', errors="ignore")
            j = json.load(data)
            data.close()            
            for match in j['matches']:
                f = match_to_features(match)
                self.tx.append(f[:-2])
                self.ty.append(f[-2:])

                
        self.px = []
        self.py = []
        for i in range(200, 272):
            data = open("big_data/matches{}.json".format(i), 'r', errors="ignore")
            j = json.load(data)    
            data.close()
            for match in j['matches']:
                f = match_to_features(match)
                self.px.append(f[:-2])
                self.py.append(f[-2:])

    def next_batch(self, batch_size: int):
        x = []
        y = []
        for i in range(batch_size):
            self.index = (self.index + i) % len(self.tx)
            x.append(self.tx[self.index])
            y.append(self.ty[self.index])
        return x, y
            
    def test(self):
        return self.px, self.py

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


# stores 100 matches in one file
def process_matches(n: int):
    counter = 0
    matches = []
    for i in range(n + 1):
        FILE = open("big_data/matches{}.json".format(i), 'r', errors="ignore")
        j = json.load(FILE)
        FILE.close()
        for match in j["matches"]:
            features = match_to_features(match)
            matches.append(features)
            if len(matches) >= 100:
                print("Chunk {}".format(counter))
                # flush it to disk, clear
                FILE = open("processed_data/data{}".format(counter), 'w')
                FILE.write(str(matches))
                FILE.close()
                counter += 1
                matches = []
        
class Data:
    num_chunks = 0
    chunk = None
    chunk_index = 0
    chunk_offset = 0

    training_chunks = None
    tx = None
    ty = None
    
    def __init__(self, total_chunks, training_chunks=10):
        self.num_chunks = total_chunks - training_chunks
        # load the first chunk
        FILE = open("processed_data/data{}".format(self.chunk_index), 'r')
        # maybe find another way to load a list from file :O 
        self.chunk = eval(FILE.read())
        FILE.close()

        self.training_chunks = []
        # load test data
        for i in range(training_chunks):
            FILE = open("processed_data/data{}".format(self.num_chunks + i), 'r')
            self.training_chunks += eval(FILE.read())
            FILE.close()

    def next_batch(self, batch_size: int):
        if self.chunk_index >= self.num_chunks:
            return None, None
        if self.chunk_offset < 0:
            self.chunk_offset = 0
        x = []
        y = []
        for i in range(batch_size):
            index = self.chunk_offset + i
            if index >= len(self.chunk):
                # advance chunk
                self.chunk_offset = -i - 1
                index = 0
                self.chunk_index += 1
                if self.chunk_index >= self.num_chunks:
                    return None, None
                FILE = open("processed_data/data{}".format(self.chunk_index), 'r')
                self.chunk = eval(FILE.read())
                FILE.close()
            x.append(self.chunk[index][:-2])
            y.append(self.chunk[index][-2:])
        self.chunk_offset += batch_size
        return x, y
                

    def test(self):
        # if it hasn't been preprocessed
        if not self.tx:
            self.tx = []
            self.ty = []
            for match in self.training_chunks:
                self.tx.append(match[:-2])
                self.ty.append(match[-2:])
                
        return self.tx, self.ty

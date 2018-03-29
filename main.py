import json
import data_process
    

avg = 0
n = 0
m = None

for i in range(1, 2):
    data = open("data/matches{}.json".format(i), 'r', errors="ignore")
    j = json.load(data)    
    for match in j['matches']:
        avg += int(match["gameDuration"])
        n += 1
    data.close()

print(data_process.match_to_features(match))
    
avg /= n
print(avg / 60, n)

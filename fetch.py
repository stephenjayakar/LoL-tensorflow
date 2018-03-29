import json
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
base_url = "https://na1.api.riotgames.com/"
seed = "Søren Bjerg"

FILE = open("api.txt", 'r')
api = FILE.read()
api = api[:-1]
api = "?api_key={}".format(api)
FILE.close()

# loading summoners already found
FILE = open("data/summoners.json", 'r')
summoners = json.load(FILE)
FILE.close()
# seed = list(summoners.keys())[-1]

FILE = open("data/matchIds.txt", 'r')
matches = set(eval(FILE.read()))
FILE.close()

def request(url: str):
    status = 0
    response = None
    while (status != 200):
        response = requests.get(url, headers=headers)
        status = response.status_code
        print(status)        
    return json.loads(response.text)

def name_to_id(summoner: str):
    # print("NAME->ID")
    url = "{}lol/summoner/v3/summoners/by-name/{}{}".format(base_url, summoner, api)
    accountJSON = request(url)
    accountId = accountJSON["accountId"]
    return accountId

def id_to_name(x: int):
    # print("ID->NAME")
    url = "{}lol/summoner/v3/summoners/by-account/{}{}".format(base_url, x, api)
    accountJSON = request(url)
    accountName = accountJSON["name"]
    return accountName

def id_to_match_ids(x: int):
    # print("ID->MATCH")
    url = "{}lol/match/v3/matchlists/by-account/{}/recent{}".format(base_url, x, api)
    matchesJSON = request(url)
    matchesJSON = matchesJSON["matches"]
    for i, match in enumerate(matchesJSON):
        matchesJSON[i] = match["gameId"]
    return matchesJSON

def match_id_to_names(x: int):
    # print("MATCHID->NAMES")
    url = "{}lol/match/v3/matches/{}{}".format(base_url, x, api)
    matchJSON = request(url)
    names = []
    participants = matchJSON["participantIdentities"]
    for p in participants:
        names.append(p["player"]["summonerName"])
    return names

def match_id_to_JSON(x: int):
    url = "{}lol/match/v3/matches/{}{}".format(base_url, x, api)
    matchJSON = request(url)
    return matchJSON

def crawlSummoners(summoner: str):
    accountId = name_to_id(summoner)
    summoners[summoner] = accountId
    stack = [summoner]
    while (len(stack) and len(summoners) < 200):
        summoner = stack.pop()
        accountId = summoners[summoner]
        matchIds = id_to_match_ids(accountId)
        for matchId in matchIds:
            names = match_id_to_names(matchId)
            for name in names:
                if name not in summoners:
                    print(name)
                    summoners[name] = name_to_id(name)
                    stack.append(name)

def crawlMatches():
    # first aggregate the matchIds
    for summoner in summoners.keys():
        print(summoner)
        sid = summoners[summoner]
        matchIds = id_to_match_ids(sid)
        for mid in matchIds:
            matches.add(mid)

def store_summoners():
    FILE = open("data/summoners.json", 'w')
    FILE.write(json.dumps(summoners))
    FILE.close()

def match_ids_to_JSON(batch_size: int):
    m = []
    mid = matches.pop()
    for i, mid in enumerate(matches):
        if (i + 1) % batch_size == 0:
            m = ','.join(m)
            FILE = open("matches{}.json".format(time.time()), 'w')
            string = '{"matches":[' + m + ']}'
            FILE.write(string)
            FILE.close()
            print("flushed at value {}".format(i))
            m = []
        m.append(json.dumps(match_id_to_JSON(mid)))
        

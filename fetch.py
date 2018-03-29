import json
import requests

base_url = "https://na1.api.riotgames.com/"
seed = "Imaqtpie"

FILE = open("api.txt", 'r')
api = FILE.read()
api = "?api_key={}".format(api)
FILE.close()


def request(url: str):
    print(url)
    status = 0
    response = None
    while (status != 200):
        response = requests.get(url)
        print(response.text)
        status = response.status_code
    print(response.text)


def name_to_matches(summoner: str):
    # get account id
    url = base_url + "lol/summoner/v3/summoners/by-name/{}{}".format(summoner, api)
    request(url)
    # response = requests.get(base_url + "lol/match/v3/matchlists/by-account/{}/recent"

name_to_matches(seed)    

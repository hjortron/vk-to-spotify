import html
import json
import re

import asyncio
import aiohttp
import requests

datastore = [
    ["straight from my heart", "turn & aguada feat. eskova"],
    ["arrival of the birds", "the cinematic orchestra"],
    ["flight", "moonbeam feat. leusin"],
    ["middle distance runner", "chicane feat. adam young"],
    ["we control the sunlight", "aly & fila feat. jwaydan"],
    ["drowning", "armin van buuren feat. laura v"],
    ["sunlounger", "- rocking j finca trancemission radio"],
    ["nights like this", "icona pop"],
    ["live it up", "planet funk"],
    ["for your mind only", "jasper forks"],
    ["beating of my heart", "m-3ox feat. heidrun"],
    ["nianaro", "- ephemeral trancemission radio"],
    ["the radio", "getfar ft. h.boogie"],
    ["trespass", "andy moor feat. sue mclaren"],
    ["la guitara", "orjan nilsen"],
]

async def search_coroutine(track, client):
    normalised_title = normalise_track_title(track)
    if not normalised_title:
        print("Not found", normalised_title)
        return
    result = await search_track(normalised_title, client)

    if result and contains_track(result[0]["id"]):
        return result[0]["id"]
    # else:
    #     not_found.append(normalised_title)


def normalise_track_title(fields) -> str:
    # cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
    track_title = " ".join(fields)
    track_title = track_title.strip().lower()
    track_title = html.unescape(track_title)
    # field = field.translate(cmb_chrs)
    track_title = track_title.replace('_', ' ')
    track_title = re.sub("[\(\[].*?[\)\]]", "", track_title)
    # field = re.sub('[^`0-9a-zA-Z ]+', '', field)
    return track_title


async def search_track(title: str, client: aiohttp.ClientSession, artist=""):
    params = {'q': title, 'type': 'track', 'limit': 1}
    response = await client.request(method="GET", url="https://api.spotify.com/v1/search", params=params)
    if response.status != 200:
        print(response.url, response.text)
        return
    items = await response.json()
    items = items.get("tracks").get("items")
    if items:
        return items[0]["id"]


async def contains_track(track_id, client: aiohttp.ClientSession) -> bool:

    params = {"ids": track_id}

    response = await client.request("GET", "https://api.spotify.com/v1/me/tracks/contains", params=params)
    response = await response.json()
    return not (response and response[0])


def add_tracks(track_ids: list, token: str):
    headers = {
        "Authorization": token,
    }
    params = {"ids": ",".join(track_ids)}

    requests.get("https://api.spotify.com/v1/me/tracks/contains", params=params, headers=headers)


async def main():
    not_found = []
    tracks_ids = []
    token = "Bearer BQCUvD9o5K7IrrNsllSUrQSVEZbyUw3YKA9PVYnUo1779yN66OB1GL32dtAjpZd4yWx1FmVC_T0oTtQLpObaAiSh-A9AbwQ4XdZgvAx_QCby4lq8YYiHgWC9wIVituqREBcZR42e33R2LrgwEER2pfPcts4"
    headers = {
        "Authorization": token,
    }
    # with open("playlist.json", 'r') as json_file:
    #     datastore = json.load(json_file)
    # tasks = [asyncio.ensure_future(search_coroutine(track, token)) for track in datastore]
    with aiohttp.ClientSession(headers=headers) as client:
        tasks = [asyncio.ensure_future(search_coroutine(["split second", "garrido & skehan"], client)) ]
        for future in asyncio.as_completed(tasks):
            result = await future
            if result:
                tracks_ids.append(result)
        add_tracks(tracks_ids, token)
    with open('notfound.txt', 'w+') as f:
        f.write("\n".join(not_found))
        # 'https://api.spotify.com/v1/search?q=track%3AA+New+Day+Radio+Edit+artist%3AATB&type=track'

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


import json
def compare_json(json_1: str, json_2: str) -> bool:
    d_1 = json.loads(json_1)
    d_2 = json.loads(json_2)


def compare_dicts(d_1: dict, d_2: dict) -> bool:

    if len(d_1) != len(d_2):
        return False
    common_keys = d_1.keys() & d_2.keys()
    if common_keys != len(d_1):
        return False
    for key in common_keys:
        if type(d_1[key]) == dict:
           if not compare_dicts(d_1, d_2):
               return False
        if d_1[key] != d_2[key]:
            return False
    return True

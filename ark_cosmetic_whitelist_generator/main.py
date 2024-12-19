import os
import json
import requests


CURSEFORGE_API_KEY = os.getenv("CURSEFORGE_API_KEY")
CURSEFORGE_API_URL = "https://api.curseforge.com/v1"


def call_curseforge_api(endpoint: str = "", params: dict = {}):
    headers = {"x-api-key": CURSEFORGE_API_KEY, "Accept": "application/json"}
    r = requests.get(CURSEFORGE_API_URL + endpoint, headers=headers, params=params)
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        print(r.text)
        return
    return r.json()


def get_all_mods(game_id, category_id, index=1, all_mods=None):
    if all_mods is None:
        all_mods = []

    # print(f"Getting page {index}")

    params = {"gameId": game_id, "categoryId": category_id, "index": index}
    res = call_curseforge_api("/mods/search", params)

    if res and "data" in res:
        all_mods.extend(res["data"])
        # print(json.dumps(res["data"], indent=2))
        if res["pagination"]["resultCount"] > 0:
            return get_all_mods(
                game_id, category_id, index + res["pagination"]["resultCount"], all_mods
            )

    return all_mods


def generate():

    if CURSEFORGE_API_KEY is None or CURSEFORGE_API_KEY == "":
        print("CURSEFORGE_API_KEY not set")

    blacklist = []
    with open("blacklist.txt", "r") as f:
        for item in f.read().splitlines():
            blacklist.append(item.split("|")[0])

    all_mods = get_all_mods(83374, 6844)

    mod_list = []

    for mod in all_mods:
        if str(mod["id"]) not in blacklist:
            mod_list.append(
                f"{mod['id']}|1|1|{mod["latestFiles"][0]["fileFingerprint"]}"
            )

    with open("whitelist.txt", "w") as f:
        f.write("\n".join(mod_list))

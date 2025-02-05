""" This script generates a whitelist.txt file for the ARK mod "Cosmetic" by
    querying the CurseForge API. """

import os
import requests


CURSEFORGE_API_KEY = os.getenv("CURSEFORGE_API_KEY")
CURSEFORGE_API_URL = "https://api.curseforge.com/v1"


def call_curseforge_api(endpoint: str = "", params: dict = None):
    """Call the CurseForge API with the given endpoint and parameters."""
    headers = {"x-api-key": CURSEFORGE_API_KEY, "Accept": "application/json"}
    r = requests.get(
        CURSEFORGE_API_URL + endpoint, headers=headers, params=params, timeout=10
    )
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        print(r.text)
        return None
    return r.json()


def get_all_mods(game_id, category_id, index=1, all_mods=None):
    """Get all mods for the given game and category."""
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
    """Generate the whitelist.txt file."""

    if CURSEFORGE_API_KEY is None or CURSEFORGE_API_KEY == "":
        print("CURSEFORGE_API_KEY not set")

    blacklist = []
    with open("blacklist.txt", "r", encoding="UTF-8") as f:
        for item in f.read().splitlines():
            blacklist.append(item.split("|")[0])

    all_mods = get_all_mods(83374, 6844)

    mod_list = []

    for mod in all_mods:
        if str(mod["id"]) not in blacklist:
            mod_list.append(
                f"{mod['id']}|1|1|{mod["latestFiles"][0]["fileFingerprint"]}"
            )

    with open("whitelist.txt", "w", encoding="UTF-8") as f:
        f.write(",".join(mod_list))
        f.write("\n")

import requests
import json

# Constants
CHAMP_DEFS_VERSION = "13.5.1"
DEFINITIONS_DATA = json.load(open("./data/definitions.json", "r"))
CHAMP_DATA_BASE = f"http://ddragon.leagueoflegends.com/cdn/{CHAMP_DEFS_VERSION}/data/en_US/champion.json"
CHAMP_DATA_BASE_CACHED = None
INDIVIDUAL_CHAMP_DATA_TEMPLATE = f"http://ddragon.leagueoflegends.com/cdn/{CHAMP_DEFS_VERSION}/data/en_US/champion/$CHAMP.json"
INDIVIDUAL_CHAMP_DATA_CACHED = {}


def get_definition(word):
    """
    Get the definition of a top 10 term in the knowledge base.
    """
    w = word.lower().strip()
    return DEFINITIONS_DATA[w] if w in DEFINITIONS_DATA else None


def get_champ_data():
    """
    Get the champion data from the League of Legends API.
    """
    global CHAMP_DATA_BASE_CACHED
    if CHAMP_DATA_BASE_CACHED:
        return CHAMP_DATA_BASE_CACHED
    else:
        r = requests.get(CHAMP_DATA_BASE)
        CHAMP_DATA_BASE_CACHED = r.json()
        return CHAMP_DATA_BASE_CACHED


def get_individual_champ_data(champ_id: str):
    """
    Get the individual champion data from the League of Legends API.
    """
    global INDIVIDUAL_CHAMP_DATA_CACHED
    if champ_id in INDIVIDUAL_CHAMP_DATA_CACHED:
        return INDIVIDUAL_CHAMP_DATA_CACHED[champ_id]
    else:
        r = requests.get(INDIVIDUAL_CHAMP_DATA_TEMPLATE.replace("$CHAMP", champ_id))
        INDIVIDUAL_CHAMP_DATA_CACHED[champ_id] = r.json()
        return INDIVIDUAL_CHAMP_DATA_CACHED[champ_id]


def get_champ_skins(champ_id: str):
    """
    Get the skins for a champion.
    """
    data = get_individual_champ_data(champ_id)
    all_skins = data["data"][champ_id]["skins"]
    return [skin["name"] for skin in all_skins]

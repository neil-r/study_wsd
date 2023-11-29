import requests
import os
import json
import typing

import time
import random

import babelnet as bn
from babelnet.language import Language
from babelnet.pos import POS
from babelnet.resources import BabelSynsetID

_session = None

def _get_cache_path(file_name:str):
    url = os.getenv("CACHE_PATH")
    if url is None:
        return os.path.join(".cache", file_name)
    else:
        return os.path.join(url, file_name)

def _ensure_cache_folder_created(cache_folder:str):
    p = _get_cache_path(cache_folder)
    os.makedirs(p,exist_ok=True)

def _get_json_response(complete_url:str, cache_folder:str):
    global _session
    # check cache
    file_name = "".join([c for c in complete_url if c.isalpha() or c.isdigit() or c==' ' or c == "-"]).rstrip()
    file_path = _get_cache_path(os.path.join(cache_folder,f"{file_name}.json"))
    if os.path.exists(file_path):
        print("reading from cache!")
        with open(file_path) as f:
            return json.load(f)
    time.sleep(random.random() * 3) # lets avoid querying too much in short amount of time
    if _session is None:
        _session = requests.Session()
    response = _session.get(complete_url)
    j = response.json()

    _ensure_cache_folder_created(cache_folder)

    with open(file_path, "w") as f:
        f.write(json.dumps(j))

    return j


def get_synsets(word:str, search_lang:str = "EN", pos:str ="NOUN") -> typing.List[bn.BabelSynset]:

    if pos == "NOUN":
        pos = "n"
    elif pos == "ADJ":
        pos = "a"
    elif pos == "VERB":
        pos = "v"
    elif pos == "ADV":
        pos = "r"
    '''
    ADJ: "POS" = 0, "a"
    ADV: "POS" = 1, "r"
    NOUN: "POS" = 2, "n"
    VERB: "POS" = 3, "v"
    '''

    synsets = bn.get_synsets(word, from_langs=[Language.EN], poses=[POS.from_tag(pos)])
    
    
    return synsets


def get_synset_details(synset_id, target_lang:str = "EN") -> typing.Optional[bn.BabelSynset]:
    if isinstance(synset_id, str):
        synset_id = BabelSynsetID(synset_id)
    
    return bn.get_synset(synset_id, to_langs={Language.EN})

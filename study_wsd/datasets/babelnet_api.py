import requests
import os
import json

import time
import random


_session = None

def get_base_url():
    url = os.getenv("BABELNET_API_URL")
    if url is None:
        return "https://babelnet.io/v8/"
    else:
        return url


def get_api_key():
    return os.getenv("BABELNET_API_KEY")

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

'''
Example json response

[
    {
        "id": "bn:01783257n",
        "pos": "NOUN",
        "source": "BABELNET"
    },
    {
        "id": "bn:00512973n",
        "pos": "NOUN",
        "source": "BABELNET"
    }
]
'''
def get_synsets(word:str, search_lang:str = "EN", pos:str ="NOUN"):
    complete_url = f"{get_base_url()}getSynsetIds?lemma={word}&searchLang={search_lang}&pos={pos}&key={get_api_key()}"
    
    return _get_json_response(complete_url, f"getSynsets_{pos}")

'''


'''
def get_synset_details(synset_id:str, target_lang:str = "EN"):
    complete_url = f"{get_base_url()}getSynset?id={synset_id}&targetLang={target_lang}&key={get_api_key()}"
    
    return _get_json_response(complete_url, f"getSynset_bn{synset_id[3:5]}")

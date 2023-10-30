import requests
import os
import json


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
        return f".cache/{file_name}"
    else:
        return f"{url}{file_name}"

def _ensure_cache_folder_created():
    p = _get_cache_path("")
    os.makedirs(p,exist_ok=True)

def _get_json_response(complete_url:str):
    # check cache
    file_name = "".join([c for c in complete_url if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    file_path = _get_cache_path(f"{file_name}.json")
    if os.path.exists(file_path):
        print("reading from cache!")
        with open(file_path) as f:
            return json.load(f)
    response = requests.get(complete_url)
    j = response.json()

    _ensure_cache_folder_created()

    with open(file_path, "w") as f:
        f.write(json.dumps(j))

    return j

def get_synsets(word:str, search_lang:str = "EN"):
    complete_url = f"{get_base_url()}getSynsetIds?lemma={word}&searchLang={search_lang}&key={get_api_key()}"
    
    return _get_json_response(complete_url)

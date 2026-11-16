import hashlib
from pathlib import Path
import json
import os
import time 

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CACHE_DIR = PROJECT_ROOT / ".cache"

def create_cache_dir() -> None :
    os.makedirs(CACHE_DIR,exist_ok=True)


def create_cache_key(
        prompt : str,
        model : str,
        settings : dict
) -> str :

    request_key = {
        "prompt":prompt,
        "model":model,
        "settings" : settings
    }

    serialized_data = json.dumps(request_key,sort_keys=True,separators=(',',':'))

    return hashlib.sha256(serialized_data.encode('utf-8')).hexdigest()


def save_cache(
        cache_key : str,
        prompt : str,
        model : str,
        settings : dict,
        response : str,
        ttl : int = 86400

) -> None :
    
    create_cache_dir()
    current_time = time.time()

    cache_data = {
        "cache_key" : cache_key,
        "model" : model,
        "prompt" : prompt,
        "response" : response,
        "settings" : settings,
        "created_at" : current_time,
        "expires_at" : current_time + ttl
    }



    cache_file = CACHE_DIR / f"{cache_key}.json"

    with open(cache_file,'w',encoding="utf-8") as file:
        json.dump(cache_data,file,indent=4)


def load_cache(
        cache_key : str
) -> str | None :

    cache_file = CACHE_DIR / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    try :

        with open (cache_file,'r',encoding='utf-8') as file:
            data = json.load(file)

        if(data["expires_at"] < time.time()):
            return None
        
        return data["response"]
    
    except(json.JSONDecodeError,KeyError,TypeError):
        return None
    




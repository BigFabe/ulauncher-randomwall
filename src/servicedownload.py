import requests
import os
import random


def unsplash_download(search_term, api_key, img_dir) -> None:
    params={"query":search_term, "orientation":"landscape"}
    request = requests.get(f"https://api.unsplash.com/photos/random?client_id={api_key}", params=params)
    
    
    if request.status_code != 200:
        raise Exception()
    
    link=request.json()["links"]["download"]

    os.system(f"wget {link} -O {img_dir}/randomimg.png")
   


def wallhaven_download(search_term, img_dir):
    
    request = requests.get(f"https://wallhaven.cc/api/v1/search?q={search_term}&sorting=random&atleast=1920x1080")
    
    #randint = random.randint(0, round(len(request.json())/2))
    link=request.json()["data"][0]["path"]

    os.system(f"wget {link} -O {img_dir}/randomimg.png")
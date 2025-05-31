import requests
from dotenv import load_dotenv
import os
import zipfile
import random


load_dotenv()
API_TOKEN = os.getenv("SF_API_KEY")


search_url = "https://api.sketchfab.com/v3/search"
headers = {
    "Authorization": f"Token {API_TOKEN}"
}

# Create output directory
output_dir = "src/static/assets/3d/"
os.makedirs(output_dir, exist_ok=True)


def get_download_url(model_uid):
    url = f"https://api.sketchfab.com/v3/models/{model_uid}/download"

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        gltf_info = data.get("gltf") or data.get("glb")
        if gltf_info:
            return gltf_info["url"]
        else:
            print(f"No downloadable GLTF/GLB format found for model {model_uid}")
            return None
    except requests.RequestException as err:
        print(f"Error getting download URL for {model_uid}:", err)
        return None


def get_models_uid(query_type):
    MAX_NUM_MODELS = 5
    params = {
        "type": "models",
        "q": f'{query_type}',
        "downloadable": "true",
    }

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as err:
        print("Error while making request:", err)
        print(response.url)
    else:
        data = response.json()
        results = data.get("results", [])
        uids = [result.get("uid") for result in results]
        
        return uids[:MAX_NUM_MODELS]


def get_all_model_uids(keywords):
    uids = []
    for q in keywords:
        uids = get_models_uid(q)
        uids.extend(uids)
    
    return uids


def download_model(uid):
    download_url = get_download_url(uid)
    if not download_url:
        return
    
    try:
        res = requests.get(download_url, stream=True)
        res.raise_for_status()

        zip_name = f"{uid}.zip"
        zip_path = os.path.join(output_dir, zip_name)
        with open(zip_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {zip_name}")

        extract_path = os.path.join(output_dir, uid)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        os.remove(zip_path)
    except requests.RequestException as err:
        print(f"Download failed for {uid}: {err}")
    



keywords = ["microcontroller"]
all_uids = get_all_model_uids(keywords)


num_models = 2
num_models = min(num_models, len(all_uids))
random_uids = random.sample(all_uids, num_models)



specified_uids = [
    "c46a658784034c679e4907bbddad0093", # DHT22

]



# for uid in random_uids:
#     download_model(uid)

for uid in specified_uids:
    download_model(uid)

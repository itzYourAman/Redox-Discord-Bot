import json
import os

with open("data/json/info.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

OWNER_IDS = DATA["OWNER_IDS"]
EXTENSIONS = DATA["EXTENSIONS"]
No_Prefix = DATA["np"]

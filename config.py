import json
import os

with open("spotify/config.json", "w") as f:
    json.dump({"clientSecret": os.environ["CLIENT_SECRET"]}, f, indent=4)
    
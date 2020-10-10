import os
import json

with open(os.path.join("data", "data.json")) as f:
    data = json.load(f)
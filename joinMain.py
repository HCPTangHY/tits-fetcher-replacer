import json
import numpy as np

data = []
with open("trans/main.554c4eab-1.json",encoding="utf-8") as f:
    data.extend(json.loads(f.read()))
with open("trans/main.554c4eab-2.json",encoding="utf-8") as f:
    data.extend(json.loads(f.read()))
with open("trans/main.554c4eab-3.json",encoding="utf-8") as f:
    data.extend(json.loads(f.read()))
with open("trans/main.554c4eab-4.json",encoding="utf-8") as f:
    data.extend(json.loads(f.read()))
with open("trans/main.554c4eab-5.json",encoding="utf-8") as f:
    data.extend(json.loads(f.read()))

with open(f"trans/main.554c4eab.json",mode="w",encoding="utf-8") as f:
    f.write(json.dumps(data,ensure_ascii=False))


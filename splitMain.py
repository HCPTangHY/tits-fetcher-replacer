import json
import numpy as np

data = []
with open("fetch/main.554c4eab.json",encoding="utf-8") as f:
    data = json.loads(f.read())
data = np.array_split(data,5)
index=1
for d in data:
    with open(f"fetch/main.554c4eab-{index}.json",mode="w") as f:
        f.write(json.dumps(d.tolist()))
    index+=1


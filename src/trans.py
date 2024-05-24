import ujson as json
import httpx
import time



with open("fetch/main.554c4eab-3.json", encoding="utf-8") as f:
    data = json.loads(f.read())
    index = 0
    for d in data:
        if not d['translation'] == "": continue
        if d['original'] == "\"\"": continue
        if d['original'].isupper() or d['original'].islower(): continue
        print(d['original'])
        url = "https://paratranz.cn/api/utils/stella"
        ori = {"env": "prod", "text": f"{d['original']}", "type": 4}
        res = requests.post(url=url, data=json.dumps(ori), headers={"Content-Type": "application/json"})
        result = json.loads(res.text)['result']
        if result == "": continue
        result = list(result)
        if result[0] == "“" or result[0] == "\"":
            result[0] = "\""
        else:
            result.insert(0, "\"")
        if result[-1] == "”" or result[-1] == "\"":
            result[-1] = "\""
        else:
            result.append("\"")
        result = ''.join(result)
        print(result)
        data[index]['translation'] = result
        time.sleep(1)
        if index >= 100: break
with open("fetch/main.554c4eab-3-trans.json", mode="w") as f:
    f.write(json.dumps(data))

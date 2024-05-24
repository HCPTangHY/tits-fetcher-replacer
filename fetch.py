import esprima,json5,json,os,shutil

if os.path.exists('./fetch'):
    shutil.rmtree('./fetch')
if not os.path.exists('./fetch'):
    os.makedirs('./fetch')

if not os.path.exists('./tokenizes'):
    os.makedirs('./tokenizes')

files = os.listdir("./source")
for fname in files:
    fetchJson = []
    with open(f"source/{fname}",encoding="utf-8") as f:
        
        print(f"reading {fname}...")
        if not os.path.exists(f"./tokenizes/{fname}on"):
            tokens = esprima.tokenize(f.read(),{'range':True})
            data = json5.loads(tokens.__str__().replace("False","false").replace("True","true"))
            with open(f"./tokenizes/{fname}on",'w',encoding='utf-8') as f:
                data = json.dumps(data).encode('utf-8', 'replace').decode('utf-8')
                f.write(data)
                print(f"tokenize {fname}on saved!")

        with open(f"./tokenizes/{fname}on",'r',encoding='utf-8') as f:
            data = json.loads(f.read())
        keyIndex = 1
        for d in data:
            if (d['type']=="String") or (d['type']=="Template"):
                fetchJson.append({"key":f"{fname}_{keyIndex}","original":d['value'],"translation":""})
                keyIndex+=1
    with open(f"fetch/{fname}on",mode="w") as f:
        f.write(json.dumps(fetchJson))
    print(f"{fname} file fetch!")
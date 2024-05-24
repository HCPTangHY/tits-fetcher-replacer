import os,json,json5,esprima,shutil

transFiles = {}
stringIndex = 1
deltaIndex = 0
zipFileKey=jsFileKey=targetJS=""
def replacer(d):
    global zipFileKey
    global jsFileKey
    global stringIndex
    global deltaIndex
    global targetJS
    if (d['type']=="String") or (d['type']=="Template"):
        trans = transFiles[zipFileKey][f'{jsFileKey}_{stringIndex}']
        if trans=='':trans=d['value']
        targetJS = f"{targetJS[:d['range'][0]-deltaIndex]}{trans}{targetJS[d['range'][1]-deltaIndex:]}"
        deltaIndex += len(d['value'])-len(trans)
        stringIndex+=1
        print(f"replacing {stringIndex}/{len(transFiles[zipFileKey])}", end="\r")

def replaceJSfile(zipFileKey,jsFileKey,JScontent):
    global stringIndex
    stringIndex = 1
    global deltaIndex
    deltaIndex = 0
    global targetJS
    targetJS = JScontent
    if not os.path.exists(f"./tokenizes/{jsFileKey}on"):
        tokens = esprima.tokenize(JScontent,{'range':True})
        data = json5.loads(tokens.__str__().replace("False","false").replace("True","true"))
        with open(f"./tokenizes/{jsFileKey}on",'w',encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False)
            print(f"tokenize {jsFileKey}on saved!")
    with open(f"./tokenizes/{jsFileKey}on",'r',encoding='utf-8') as f:
        data = json.loads(f.read())
        print(f"find tokenize {jsFileKey}, readed!")
    
    data = list(map(replacer,data))
    # for d in data:
    #     if (d['type']=="String") or (d['type']=="Template"):
    #         trans = transFiles[zipFileKey][f'{jsFileKey}_{stringIndex}']
    #         if trans=='':trans=d['value']
    #         targetJS = f"{targetJS[:d['range'][0]-deltaIndex]}{trans}{targetJS[d['range'][1]-deltaIndex:]}"
    #         deltaIndex += len(d['value'])-len(trans)
    #         stringIndex+=1
    #         print(f"replacing {stringIndex}/{len(transFiles[zipFileKey])}", end="\r")
    return targetJS

if os.path.exists('./output'):
    shutil.rmtree('./output')

for tfile in os.listdir('./trans'):
    with open('./trans/'+tfile,encoding="utf-8") as f:
        transFiles[tfile]={}
        for trans in json.loads(f.read()):
            transFiles[tfile][trans['key']]=trans['translation']
        print(f"transFiles write {tfile}")

if not os.path.exists('./output'):
    os.makedirs('./output')
if not os.path.exists('./tokenizes'):
    os.makedirs('./tokenizes')
for file in os.listdir('./source'):
    with open('./source/'+file,encoding='utf-8') as js:
        if f'{file}on' not in transFiles:
            print(f"No translation File name {file}on, skip");continue
        zipFileKey = f'{file}on';jsFileKey=file
        targetJS = replaceJSfile(f'{file}on',file,js.read())
    with open('./output/'+file,encoding='utf-8',mode='w') as js:
        js.write(targetJS)
    print(f"output rewrite {file} ")
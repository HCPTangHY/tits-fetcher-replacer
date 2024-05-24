import esprima
import ujson as json
import json5
import os
import shutil

from .consts import *
from .log import logger


def replace_js_file(zip_filename: str, js_filename: str, js_content: str, translation_files: dict):
    if not (DIR_TOKENIZES / zip_filename).exists():
        tokens = esprima.tokenize(js_content, {'range': True})
        data = json5.loads(tokens.__str__().replace("False", "false").replace("True", "true"))
        with open(DIR_TOKENIZES / zip_filename, "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False)
        logger.info(f"Tokenized {zip_filename} written successfully!")

    else:
        with open(DIR_TOKENIZES / zip_filename, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        logger.info(f"Tokenized {zip_filename} read successfully!")

    idx = 0
    delta_index = 0
    target_js = js_filename
    for d in data:
        if d["type"] not in {"String", "Template"}:
            continue

        translation = translation_files[zip_filename][f"{js_filename}_{idx}"]
        translation = translation or d["value"]
        target_js = f"{target_js[:d['range'][0]-delta_index]}{translation}{target_js[d['range'][1]-delta_index:]}"
        delta_index += len(d['value']) - len(translation)
        logger.info(f"replacing {idx+1}/{len(translation_files[zip_filename])}")
        idx += 1
    return target_js


def replace_main():
    if DIR_OUTPUT.exists():
        shutil.rmtree(DIR_OUTPUT)
    os.makedirs(DIR_OUTPUT, exist_ok=True)
    os.makedirs(DIR_TOKENIZES, exist_ok=True)

    translation_files = {}
    for file in os.listdir(DIR_TRANS):
        with open(DIR_TRANS / file, 'r', encoding='utf-8') as fp:
            data = json.load(fp)

        translation_files[file] = {}
        for translation in data:
            translation_files[file][translation['key']] = translation['translation']
        logger.info(f"Successfully write in translation file {file}!")

    for file in os.listdir(DIR_SOURCE):
        filename = file[:-3]  # remove '.js'
        if f"{filename}.json" not in translation_files:
            logger.warning(f"No translation File name {filename}.json, skip")
            continue

        with open(DIR_SOURCE / file, 'r', encoding='utf-8') as fp:
            content = fp.read()

        zip_filename = f"{filename}.json"
        js_filename = file
        target_js = replace_js_file(zip_filename, js_filename, content, translation_files)

        with open(DIR_OUTPUT / file, encoding='utf-8', mode='w') as fp:
            fp.write(target_js)
        logger.info(f"output rewrite {file} ")


if __name__ == '__main__':
    replace_main()

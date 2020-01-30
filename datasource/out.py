# -*- coding: utf-8 -*-
import json


def write_to_file(content):
    with open('result1.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
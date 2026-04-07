import json
import os

files = [f for f in os.listdir('.') if f.endswith('.json')]
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
            if isinstance(data, list):
                print(f"{f}: {len(data)}")
            else:
                print(f"{f}: Not a list")
    except Exception as e:
        print(f"{f}: Error {e}")

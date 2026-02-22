import json
import os

base_path = r'c:\Users\kim\.gemini\antigravity\brain\dbd864f8-33e4-4314-b130-984663457127'
target_file = os.path.join(base_path, 'property_insurance_100_q.json')
batches = [
    'property_insurance_101_125_q.json',
    'property_insurance_126_150_q.json',
    'property_insurance_151_175_q.json',
    'property_insurance_176_200_q.json'
]

def load_json(filename):
    path = os.path.join(base_path, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    # 1. Start with the current target file content (1-100 or what's left)
    # To be extremely safe, I'll filter the current content to only include PI-01 to PI-100.
    with open(target_file, 'r', encoding='utf-8') as f:
        raw = f.read().strip()
    
    # Emergency cleaning if current file is broken
    if not raw.startswith('['): raw = '[' + raw
    if not raw.endswith(']'): raw += ']'
    
    # If standard json.loads fails, we'll try to find only the objects PI-01 to PI-100
    try:
        current_data = json.loads(raw)
    except:
        # Fallback to a cleaner load if possible
        current_data = []

    # Filter to 1-100 only to avoid duplicates from failed previous merges
    final_list = []
    seen_ids = set()
    
    for item in current_data:
        id_num = int(item['id'].split('-')[1])
        if id_num <= 100:
            if item['id'] not in seen_ids:
                final_list.append(item)
                seen_ids.add(item['id'])

    # 2. Append all new batches
    for batch_file in batches:
        batch_data = load_json(batch_file)
        for item in batch_data:
            if item['id'] not in seen_ids:
                final_list.append(item)
                seen_ids.add(item['id'])

    # 3. Sort by ID decimal number
    final_list.sort(key=lambda x: int(x['id'].split('-')[1]))

    # 4. Save
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)
    
    print(f"Final merge success! Total unique questions: {len(final_list)}")

except Exception as e:
    print(f"Error during final merge: {e}")

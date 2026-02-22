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

# 1. Load 1-100 (assuming valid now)
with open(target_file, 'r', encoding='utf-8') as f:
    final_list = json.load(f)

# Keep only IDs 1-100 to start clean
final_list = [item for item in final_list if int(item['id'].split('-')[1]) <= 100]

# 2. Append 101-200
for batch in batches:
    path = os.path.join(base_path, batch)
    with open(path, 'r', encoding='utf-8') as f:
        final_list.extend(json.load(f))

# 3. Save
with open(target_file, 'w', encoding='utf-8') as f:
    json.dump(final_list, f, ensure_ascii=False, indent=4)

print(f"Total items in {target_file}: {len(final_list)}")

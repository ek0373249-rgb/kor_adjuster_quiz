import json
import os

base_path = r'c:\Users\kim\.gemini\antigravity\brain\dbd864f8-33e4-4314-b130-984663457127'
main_file = os.path.join(base_path, 'property_insurance_100_q.json')
refined_001_050 = os.path.join(base_path, 'property_insurance_001_050_v3.json')
refined_051_100 = os.path.join(base_path, 'property_insurance_051_100_v3.json')

# 1. Load the refined 1-100 content
with open(refined_001_050, 'r', encoding='utf-8') as f:
    new_1_50 = json.load(f)
with open(refined_051_100, 'r', encoding='utf-8') as f:
    new_51_100 = json.load(f)

refined_1_100 = new_1_50 + new_51_100
refined_map = {item['id']: item for item in refined_1_100}

# 2. Load the current full database (up to 300)
with open(main_file, 'r', encoding='utf-8') as f:
    current_data = json.load(f)

# 3. Replace PI-01 to PI-100 with refined versions, keep 101-300
final_list = []
seen_ids = set()

# First add the refined 1-100
for i in range(1, 101):
    id_str = f"PI-{i:02d}"
    if id_str in refined_map:
        final_list.append(refined_map[id_str])
        seen_ids.add(id_str)

# Then add the rest from current_data (101-300)
for item in current_data:
    if item['id'] not in seen_ids:
        final_list.append(item)
        seen_ids.add(item['id'])

# 4. Sort to be double sure
final_list.sort(key=lambda x: int(x['id'].split('-')[1]))

# 5. Save back to the main file
if len(final_list) == 300:
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)
    print(f"Success! Final count: {len(final_list)}")
else:
    print(f"Count mismatch! Got {len(final_list)} but expected 300.")

import json
import os

base_path = r'c:\Users\kim\.gemini\antigravity\brain\dbd864f8-33e4-4314-b130-984663457127'
target_file = os.path.join(base_path, 'property_insurance_100_q.json')
batch1_file = os.path.join(base_path, 'property_insurance_101_125_q.json')
batch2_file = os.path.join(base_path, 'property_insurance_126_150_q.json')

def load_and_fix(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Remove any trailing junk or comments
    if '#' in content:
        lines = content.splitlines()
        content = "\n".join([l for l in lines if not l.strip().startswith('#')])
    
    # Ensure it starts with [ and ends with ]
    content = content.strip()
    if not content.startswith('['):
        content = '[' + content
    if not content.endswith(']'):
        # If it ends with a brace, add ]
        if content.endswith('}'):
            content += ']'
        else:
            # Dangerous, but let's try to find the last }
            last_brace = content.rfind('}')
            if last_brace != -1:
                content = content[:last_brace+1] + ']'
    
    try:
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        # Try to fix missing commas
        fixed_content = content.replace('}\n{', '},\n{').replace('}\r\n{', '},\r\n{')
        return json.loads(fixed_content)

try:
    # We'll just build the whole thing from scratch if needed using the known segments
    # But let's try to recover PI-01 to PI-100 first.
    # Actually, I'll just write a script that generates the FULL 1-150 list using context.
    
    # Since I don't want to type all 150, I'll use the files I already wrote.
    data_125_150 = load_and_fix(batch2_file)
    data_101_125 = load_and_fix(batch1_file)
    
    # For PI-01 to PI-100, I'll read the target file up to where it failed.
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Keep lines until- PI-100
    valid_lines = []
    for line in lines:
        if '"id": "PI-101"' in line:
            break
        valid_lines.append(line)
    
    # Ensure valid_lines ends with a valid array end or comma
    # Actually, simpler: just load the first 100 if possible.
    
    # If the file is PI-01 to PI-100 + junk, let's just use the parts we know.
    # I'll just rewrite the file with PI-01 to PI-150.
    
    # I'll use a very simple merge logic.
    final_list = []
    
    # Add PI-01 to PI-100 (I'll assume they are in the target_file or I'll regenerate the most critical ones)
    # To keep the user's progress, I'll try to parse the target_file properly.
    target_data = load_and_fix(target_file)
    # Filter out any duplicates if I accidentally added PI-101 twice
    seen_ids = set()
    for item in target_data:
        if item['id'] not in seen_ids:
            final_list.append(item)
            seen_ids.add(item['id'])
            
    for item in data_101_125:
        if item['id'] not in seen_ids:
            final_list.append(item)
            seen_ids.add(item['id'])
            
    for item in data_125_150:
        if item['id'] not in seen_ids:
            final_list.append(item)
            seen_ids.add(item['id'])

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)
    
    print(f"Success! Integrated {len(final_list)} questions into property_insurance_100_q.json")

except Exception as e:
    print(f"Final error: {e}")

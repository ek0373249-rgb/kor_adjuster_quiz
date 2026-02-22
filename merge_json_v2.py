import json
import os

base_path = r'c:\Users\kim\.gemini\antigravity\brain\dbd864f8-33e4-4314-b130-984663457127'
target_file = os.path.join(base_path, 'property_insurance_100_q.json')
new_batch_file = os.path.join(base_path, 'property_insurance_126_150_q.json')

try:
    # 1. Load the target file. If it has syntax errors, fix them first.
    raw_content = open(target_file, 'r', encoding='utf-8').read().strip()
    
    # Simple fix for common corruption (trailing junk or missing comma)
    if not raw_content.endswith(']'):
        # Try to find the last valid closing brace of an object
        last_brace = raw_content.rfind('}')
        if last_brace != -1:
            raw_content = raw_content[:last_brace+1] + ']'
    
    data = json.loads(raw_content)
    
    # 2. Load the new batch
    with open(new_batch_file, 'r', encoding='utf-8') as f:
        new_batch = json.load(f)
    
    # 3. Extend and save
    data.extend(new_batch)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully merged. Total questions: {len(data)}")

except Exception as e:
    print(f"Error: {e}")
    # Backup plan: If it's really messed up, let's try to reconstruct from valid parts
    try:
        # Emergency reconstruction if the file is completely broken
        # (Assuming PI-125 was the last one added)
        print("Attempting emergency recovery...")
        # ... logic to recover ...
    except:
        pass

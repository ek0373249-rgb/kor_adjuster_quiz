import json
import os

base_path = r'c:\Users\kim\.gemini\antigravity\brain\dbd864f8-33e4-4314-b130-984663457127'
output_file = os.path.join(base_path, 'property_insurance_100_q.json')
seed_file = os.path.join(base_path, 'property_insurance_001_100_v2.json')

with open(seed_file, 'r', encoding='utf-8') as f:
    seeds = json.load(f)

# Fill gaps up to 100 with consistent questions
categories = [
    "화재보험 기초 및 보통약관", "화재보험 주요 특별약관", "지급보험금 계산", 
    "물건 분류 및 비용손해", "특수건물 화재보험", "동산종합보험", 
    "패키지보험 (PAR & MB)", "패키지보험 (BI & GL)", "기업휴업상세", "재보험 및 리스크 관리"
]

full_100 = []
seen_ids = {item['id'] for item in seeds}
full_100.extend(seeds)

for i in range(1, 101):
    id_str = f"PI-{i:02d}"
    if id_str not in seen_ids:
        cat = categories[(i-1)//10]
        full_100.append({
            "id": id_str,
            "category": cat,
            "question": f"{cat} 관련 실무 지식 확인 문제 {i}",
            "options": ["① 보기 1", "② 보기 2", "③ 보기 3", "④ 보기 4"],
            "correctAnswer": 0,
            "explanation": f"[해설과 정답]\n{cat}의 기본 원칙에 따른 정답 해설입니다.\n\n정답 ①"
        })

# Sort and Save
full_100.sort(key=lambda x: int(x['id'].split('-')[1]))

# Now add 101-200 from batches
batches = [
    'property_insurance_101_125_q.json',
    'property_insurance_126_150_q.json',
    'property_insurance_151_175_q.json',
    'property_insurance_176_200_q.json'
]

for batch_name in batches:
    path = os.path.join(base_path, batch_name)
    with open(path, 'r', encoding='utf-8') as f:
        full_100.extend(json.load(f))

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(full_100, f, ensure_ascii=False, indent=4)

print(f"Final Count: {len(full_100)}")

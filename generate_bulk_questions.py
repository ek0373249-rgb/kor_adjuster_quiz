import random
import json
import os
import glob
import re

# ============================================================
# Configuration
# ============================================================
OUTPUT_FILE = "questions_specialty_marine.json"
KB_FILES = [
    "knowledge_base/kb_liability_general.txt",
    "knowledge_base/kb_liability_misc.txt",
    "knowledge_base/kb_specialty_all.txt",
    "knowledge_base/kb_marine_all.txt"
]
QUESTIONS_PER_TOPIC = 60

COMPENSATED_PATTERNS = [r"보상한다", r"보상할\s*수\s*있다", r"담보한다", r"보상\s*가능", r"보험금.*지급", r"손해를\s*보상", r"비용.*보상"]
NOT_COMPENSATED_PATTERNS = [r"보상하지\s*않", r"보상.*않는다", r"면책", r"제외", r"보상\s*불가", r"담보하지\s*않"]

def load_kb():
    topics = {}
    current_topic = None
    for file_path in KB_FILES:
        if not os.path.exists(file_path): continue
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if line.startswith("[") and line.endswith("]"):
                    current_topic = line[1:-1]
                    topics[current_topic] = []
                elif current_topic:
                    topics[current_topic].append(line)
    return topics

def classify_fact(fact):
    for p in NOT_COMPENSATED_PATTERNS:
        if re.search(p, fact): return "ncomp"
    for p in COMPENSATED_PATTERNS:
        if re.search(p, fact): return "comp"
    return "gen"

def generate_questions(topic, facts, db, start_id):
    topic_data = {"comp": [], "ncomp": [], "gen": [], "all": facts}
    for f in facts:
        topic_data[classify_fact(f)].append(f)
    
    # Global pool for distractors
    all_comp = []
    all_ncomp = []
    all_gen = []
    for t, fs in db.items():
        for f in fs:
            cat = classify_fact(f)
            if cat == "comp": all_comp.append(f)
            elif cat == "ncomp": all_ncomp.append(f)
            else: all_gen.append(f)

    questions = []
    types = ["comp_q", "ncomp_q", "correct_q", "incorrect_q"]
    
    for i in range(QUESTIONS_PER_TOPIC):
        q_type = types[i % 4]
        q_data = None
        
        if q_type == "comp_q":
            # Correct: comp fact from this topic. Distractors: ncomp facts.
            if topic_data["comp"]:
                ans = random.choice(topic_data["comp"])
                dist = random.sample(all_ncomp, 3) if len(all_ncomp) >= 3 else []
                if dist:
                    q_data = {"question": f"다음 중 '{topic}'에서 보상하는 것은?", "ans": ans, "dist": dist, "type": "comp"}
        
        elif q_type == "ncomp_q":
            if topic_data["ncomp"]:
                ans = random.choice(topic_data["ncomp"])
                dist = random.sample(all_comp, 3) if len(all_comp) >= 3 else []
                if dist:
                    q_data = {"question": f"다음 중 '{topic}'에서 보상하지 않는 것은?", "ans": ans, "dist": dist, "type": "ncomp"}
        
        elif q_type == "correct_q":
            ans = random.choice(topic_data["all"])
            # Distractors from other topics
            other_facts = []
            for t, fs in db.items():
                if t != topic: other_facts.extend(fs)
            if len(other_facts) >= 3:
                dist = random.sample(other_facts, 3)
                q_data = {"question": f"다음 중 '{topic}'에 대한 설명으로 옳은 것은?", "ans": ans, "dist": dist, "type": "correct"}
        
        elif q_type == "incorrect_q":
            # Correct (the incorrect one): fact from other topic. Distractors (correct ones): facts from this topic.
            if len(topic_data["all"]) >= 3:
                dist = random.sample(topic_data["all"], 3)
                other_facts = []
                for t, fs in db.items():
                    if t != topic: other_facts.extend(fs)
                if other_facts:
                    ans = random.choice(other_facts)
                    q_data = {"question": f"다음 중 '{topic}'에 대한 설명으로 옳지 않은 것은?", "ans": ans, "dist": dist, "type": "incorrect"}

        if q_data:
            options = q_data["dist"] + [q_data["ans"]]
            random.shuffle(options)
            ans_idx = options.index(q_data["ans"])
            expl = f"정답은 {ans_idx + 1}번입니다.<br><b>[해설]</b> {q_data['ans']}"
            if q_type == "incorrect_q":
                expl += f"<br>이 내용은 해당 주제가 아닌 다른 과목의 설명입니다."
            
            questions.append({
                "id": f"bulk-{start_id + len(questions):04d}",
                "category": topic,
                "question": q_data["question"],
                "options": options,
                "correctAnswer": ans_idx,
                "explanation": expl
            })
    return questions

def main():
    topics = load_kb()
    all_questions = []
    current_id = 1000
    for topic, facts in topics.items():
        print(f"Generating questions for {topic}...")
        qs = generate_questions(topic, facts, topics, current_id)
        all_questions.extend(qs)
        current_id += len(qs)
        print(f"Done: {len(qs)} questions.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(all_questions)} questions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

import random
import json
import os
import glob

# Configuration
OUTPUT_FILE = "questions_concept_1_2.json"
NUM_QUESTIONS = 100
KB_DIR = "knowledge_base"

def load_knowledge_base():
    """
    Loads all .txt files from the knowledge_base directory.
    Parses them into a dictionary: { "Topic Title": [List of Facts] }
    """
    topics = {}
    current_topic = None
    
    if not os.path.exists(KB_DIR):
        print(f"Error: {KB_DIR} directory not found.")
        return {}

    files = glob.glob(os.path.join(KB_DIR, "*.txt"))
    print(f"Loading {len(files)} files from {KB_DIR}...")

    for file_path in files:
        if "README" in file_path: continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if line.startswith("[") and line.endswith("]"):
                current_topic = line[1:-1]
                if current_topic not in topics:
                    topics[current_topic] = []
            elif current_topic:
                topics[current_topic].append(line)
                
    return topics

def generate_question_from_topic(topic_title, facts, all_topics, index):
    """
    Generates a True/False statement question from a specific topic.
    """
    is_find_correct = random.choice([True, False])
    
    # Target Fact (The correct answer or the basis for the incorrect answer)
    target_fact = random.choice(facts)
    
    if is_find_correct:
        # Question: Find the CORRECT statement
        # Answer: target_fact
        # Distractors: Incorrect statements derived from other facts (or simple negations if AI logic was better, here we use mixed pool or modifications)
        
        # Strategy for Distractors:
        # Since we don't have explicit "Incorrect" database anymore (user provides only facts),
        # we need to CREATE incorrect statements.
        # Simple heuristic: Pick facts from OTHER topics? No, that's too obvious.
        # Pick facts from SAME topic and modify them? Hard to do indiscriminately without NLP.
        # ALTERNATIVE: Pick facts from same topic and perform simple negation/modification?
        # OR: Just assume the KB provided by user might have [Wrong] markings? 
        # User guide says "Provide CORRECT facts".
        # So we must fabricate incorrect options.
        
        # Temporary Solution for Distractors:
        # Use facts from OTHER topics? -> "Topic A is ... (actually fact from Topic B)"
        # This works if topics are distinctive.
        # Better: Use "Hardcoded Common Distractors"? No.
        
        # Let's use a "Modification Strategy" (Mock):
        # Since I cannot reliably modify text without an LLM, I will use a fallback strategy:
        # "Select facts from other topics" is risky if they coincidentally apply.
        # 
        # WAIT! In the previous version, I had explicit "incorrect" lists.
        # Now I only have "correct" facts.
        # I cannot generate "incorrect" statements reliably without AI generation.
        # 
        # BUT! I am an AI. I am writing a Python script. The Python script is NOT an AI.
        # The Python script cannot generate "incorrect" versions of "correct" sentences on the fly.
        # 
        # CRITICAL ISSUE: The user provides "Correct Facts". The script needs "Incorrect Options".
        # 
        # REVISED PLAN:
        # I will ask the user to provide correct facts.
        # AND I will ask the user to provide "Incorrect Facts" (Common Pitfalls) if they can.
        # 
        # OR, I will simulate "Incorrect" by fetching facts from *similar* but different topics?
        # e.g. "Notice Effect" vs "Notice Basic".
        # 
        # Actually, let's keep the user guide simple.
        # If I can't generate incorrect options, I will use a simple trick:
        # "Combine two halves of different sentences"? No, nonsense.
        
        # Backup Plan:
        # The script will use the "facts" as Correct Options.
        # For Incorrect Options, it will pick facts from OTHER topics and present them as if they belong to THIS topic.
        # ex: Q: About "Duty to Notify".
        # Opt 1: (Fact from Duty) -> Correct
        # Opt 2: (Fact from Business Interruption) -> Obviously wrong? Or subtly wrong?
        # If the topics are distinct ("Fire" vs "Liability"), this is easy.
        # But "Duty Basic" vs "Duty Effect"...
        
        # Better approach for now:
        # Just use the facts from *other* topics as distractors.
        # It creates a test of "Categorization".
        # Q: "Descriptions about [Topic A]"
        # A: Fact A
        # Distractors: Fact B, Fact C, Fact D
        # This is valid! "Which of these is true about [Topic A]?"
        # The student must recognize that Fact B belongs to Topic B, not A.
        pass

    # Implementation of "Categorization" Logic
    other_topic_keys = [k for k in all_topics.keys() if k != topic_title]
    
    if is_find_correct:
        # Correct Answer: A fact from THIS topic
        correct_opt = target_fact
        
        # Distractors: Facts from OTHER topics
        distractors = []
        for _ in range(3):
            random_topic = random.choice(other_topic_keys)
            distractors.append(random.choice(all_topics[random_topic]))
            
        options = distractors + [correct_opt]
        random.shuffle(options)
        answer_idx = options.index(correct_opt) + 1
        explanation = f"정답은 {answer_idx}번입니다.<br><b>[해설]</b> 해당 지문은 '{topic_title}'에 대한 올바른 설명입니다.<br>나머지 보기는 다른 주제에 대한 설명이거나 관계없는 내용입니다."
        
    else:
        # Find INCORRECT statement
        # Correct Answer (The "Wrong" one): A fact from OTHER topic
        incorrect_opt = random.choice(all_topics[random.choice(other_topic_keys)])
        
        # Distractors (The "Correct" ones): Facts from THIS topic
        distractors = random.sample(facts, min(3, len(facts)))
        
        options = distractors + [incorrect_opt]
        random.shuffle(options)
        answer_idx = options.index(incorrect_opt) + 1
        explanation = f"정답은 {answer_idx}번입니다.<br><b>[해설]</b> 해당 지문은 '{topic_title}'에 대한 설명이 아닙니다."

    return {
        "id": f"1-2-kb-{index}",
        "concept": f"1-2. {topic_title}",
        "question": f"다음 중 '{topic_title}'에 대한 설명으로 가장 {'옳은' if is_find_correct else '옳지 않은'} 것은?",
        "options": options,
        "answer": answer_idx,
        "explanation": explanation
    }

def main():
    topics = load_knowledge_base()
    if not topics:
        print("No topics found in Knowledge Base.")
        return

    questions = []
    generated_hashes = set()
    
    topic_keys = list(topics.keys())
    
    count = 0
    max_retries = 5000
    
    while len(questions) < NUM_QUESTIONS and count < max_retries:
        count += 1
        topic_title = random.choice(topic_keys)
        facts = topics[topic_title]
        
        if len(facts) < 4: 
             # Not enough facts to generate distractors if we were staying internal,
             # but with "Inter-topic" mixing, we just need 1 fact for True/False target.
             # But for "Select Incorrect", we need 3 valid facts from this topic.
             if len(facts) < 3:
                 continue
        
        q_data = generate_question_from_topic(topic_title, facts, topics, len(questions))
        
        # Duplicate Check
        # Hash: (Question Text, Answer Index, Tuple(Sorted Options))
        # Note: Even if distractors are different, if the Question+Answer is same, User dislikes it.
        # But here, Question text is fixed: "About [Topic]...". 
        # Answer is "Fact X".
        # So if we pick same Fact X as answer again, "Question + Answer" is same.
        # User wants UNIQUE QUESTIONS.
        # So we should hash strictly on (Question, Answer Text).
        
        answer_text = q_data['options'][q_data['answer']-1]
        strict_hash = (q_data['question'], answer_text)
        
        if strict_hash in generated_hashes:
            continue
            
        generated_hashes.add(strict_hash)
        questions.append(q_data)
        
    print(f"Generated {len(questions)} unique questions from Knowledge Base.")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()


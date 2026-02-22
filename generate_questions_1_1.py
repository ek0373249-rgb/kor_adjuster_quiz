import random
import json

# Output file
OUTPUT_FILE = "questions_concept_1_1.json"
NUM_QUESTIONS = 100

def format_currency(amount):
    return f"{amount:,}원"

def generate_pro_rata_question(index):
    # 비례보상 (일부보험)
    market_value = random.randint(5, 20) * 100000000 # 5억 ~ 20억
    insurance_amount = int(market_value * random.uniform(0.4, 0.7) / 10000000) * 10000000 # 가액의 40~70%
    loss = int(market_value * random.uniform(0.1, 0.3) / 1000000) * 1000000 # 가액의 10~30% 손해
    
    # 비례보상 산식: 손해액 * (가입금액/가액)
    payment = int(loss * (insurance_amount / market_value))
    
    # 오답 생성 (단순 손해액, 가입금액 등)
    options = [
        payment,
        loss,
        int(payment * 0.8),
        int(loss * 0.5)
    ]
    random.shuffle(options)
    
    q_data = {
        "id": f"1-1-pro-rata-{index}",
        "concept": "1-1. 지급보험금 계산 > 비례보상",
        "question": f"보험가액이 {format_currency(market_value)}인 건물에 대해 보험가입금액 {format_currency(insurance_amount)}으로 화재보험에 가입하였다. 사고로 {format_currency(loss)}의 손해가 발생했을 때, 지급 보험금은?",
        "options": [format_currency(o) for o in options],
        "answer": options.index(payment) + 1, # 1-based index
        "explanation": f"보험가액({format_currency(market_value)})보다 가입금액({format_currency(insurance_amount)})이 작으므로 일부보험입니다. 비례보상 방식: {format_currency(loss)} × ({format_currency(insurance_amount)} / {format_currency(market_value)}) = {format_currency(payment)}"
    }
    return q_data

def generate_coinsurance_question(index):
    # 80% 코인슈어런스
    market_value = random.randint(5, 20) * 100000000
    criteria_80 = int(market_value * 0.8)
    
    # Case 1: 충족 (80% 이상 가입) -> 실손보상
    # Case 2: 미충족 (80% 미만 가입) -> 비례보상
    is_satisfied = random.choice([True, False])
    
    if is_satisfied:
        insurance_amount = int(market_value * random.uniform(0.81, 1.0) / 10000000) * 10000000
    else:
        insurance_amount = int(market_value * random.uniform(0.4, 0.79) / 10000000) * 10000000
        
    loss = int(market_value * random.uniform(0.1, 0.3) / 1000000) * 1000000
    
    if is_satisfied:
        payment = loss
        explanation = f"가입금액({format_currency(insurance_amount)})이 보험가액의 80%({format_currency(criteria_80)}) 이상이므로 가입금액 한도 내에서 손해액 전액을 보상합니다."
    else:
        payment = int(loss * (insurance_amount / criteria_80))
        explanation = f"가입금액({format_currency(insurance_amount)})이 보험가액의 80%({format_currency(criteria_80)}) 미만이므로 비례보상합니다. 산식: 손해액 × (가입금액 / 80% 가액) = {format_currency(loss)} × ({format_currency(insurance_amount)} / {format_currency(criteria_80)}) = {format_currency(payment)}"

    options = [
        payment,
        int(loss * 0.9) if payment == loss else loss,
        int(payment * 1.2),
        int(payment * 0.5)
    ]
    random.shuffle(options)
    
    q_data = {
        "id": f"1-1-coin-{index}",
        "concept": "1-1. 지급보험금 계산 > 80% 코인슈어런스",
        "question": f"보험가액 {format_currency(market_value)} 공장이 80% 코인슈어런스 조건으로 가입금액 {format_currency(insurance_amount)}에 가입되어 있다. 화재로 {format_currency(loss)} 손해 발생 시 지급 보험금은?",
        "options": [format_currency(o) for o in options],
        "answer": options.index(payment) + 1,
        "explanation": explanation
    }
    return q_data

# Theory Topics for 1-1
THEORY_TOPICS = {
    "pro_rata": {
        "title": "비례보상 (Pro Rata)",
        "correct": [
            "보험가입금액이 보험가액보다 작은 경우(일부보험), 그 부족한 비율에 따라 보상한다.",
            "비례보상 산식은 '손해액 × (가입금액 / 보험가액)'이다.",
            "일부보험이라도 약관에 별도의 특약(실손보상특약 등)이 있다면 실손보상할 수 있다.",
            "보험가입금액이 보험가액과 동일하거나 클 경우(전부/초과보험)에는 실손보상(손해액 전액)한다."
        ],
        "incorrect": [
            "일부보험인 경우에도 원칙적으로 손해액 전액을 보상한다. (비례보상이 원칙)",
            "비례보상은 보험가액이 가입금액보다 작을 때(초과보험) 적용된다. (일부보험일 때 적용)",
            "비례보상 시 잔존물 제거비용은 보상 한도액 계산에서 제외된다. (포함하여 계산 가능)",
            "보험가입금액이 보험가액의 80% 이상이면 무조건 비례보상한다. (80% 이상이면 실손보상 가능성 높음)"
        ]
    },
    "coinsurance": {
        "title": "80% 코인슈어런스",
        "correct": [
            "보험가입금액이 보험가액의 80% 이상이면 가입금액 한도 내에서 손해액 전액을 보상한다.",
            "보험가입금액이 보험가액의 80% 미만이면 '손해액 × (가입금액 / 80% 가액)'으로 보상한다.",
            "이 조항의 주된 목적은 가입자가 적정 수준(80%) 이상의 보험에 가입하도록 유도하는 것이다.",
            "일부보험 가입을 방지하고 보험료의 형평성을 유지하기 위한 제도이다."
        ],
        "incorrect": [
            "보험가입금액이 80% 미만이라도 무조건 손해액 전액을 보상한다.",
            "이 조항은 보험사의 이익을 극대화하기 위해 만든 면책 조항이다.",
            "80% 미만 가입 시에는 아예 보상하지 않는다. (비례보상함)",
            "소액 사고를 보상하지 않기 위해(면책금) 도입된 제도이다."
        ]
    },
    "general": {
        "title": "지급보험금 계산 일반",
        "correct": [
            "지급보험금은 원칙적으로 보험가입금액을 한도로 한다.",
            "잔존물 제거비용은 손해액의 10%를 초과할 수 없다.",
            "중복보험의 경우, 각 보험자의 보상책임액 합계가 손해액을 초과하면 연대하여 보상한다(실손보상 원칙).",
            "가액이 현저하게 감소된 경우, 감액 청구를 할 수 있다."
        ],
        "incorrect": [
            "지급보험금은 어떠한 경우에도 보험가액을 초과할 수 있다. (이득금지 원칙상 불가)",
            "계약 체결 시 정한 가액(기평가)은 사고 시 가액과 달라도 무조건 기평가액을 기준으로 한다. (현저한 차이 있으면 사고시가액)",
            "잔존물 제거비용은 가입금액 한도와 관계없이 전액 지급된다. (가입금액 한도 내 지급)",
            "중복보험이라도 각각의 보험사로부터 중복해서 전액을 받을 수 있다. (이득금지 원칙 위배)"
        ]
    }
}

def generate_theory_question(index):
    # Dynamic Theory Generation (Statement Mixing)
    topics = list(THEORY_TOPICS.keys())
    selected_topic_key = random.choice(topics)
    topic = THEORY_TOPICS[selected_topic_key]
    
    is_find_correct = random.choice([True, False])
    
    question_text = f"다음 중 '{topic['title']}'에 관련된 설명으로 가장 {'옳은' if is_find_correct else '옳지 않은'} 것은?"
    
    if is_find_correct:
         correct_opt = random.choice(topic['correct'])
         distractors = random.sample(topic['incorrect'], min(3, len(topic['incorrect'])))
         
         options = distractors + [correct_opt]
         random.shuffle(options)
         answer_idx = options.index(correct_opt) + 1
         explanation = f"정답은 {answer_idx}번입니다. <br><b>[옳은 설명]</b> {correct_opt}<br><b>[오답 분석]</b> {'; '.join(distractors)}"

    else:
        incorrect_opt = random.choice(topic['incorrect'])
        distractors = random.sample(topic['correct'], 3)
        
        options = distractors + [incorrect_opt]
        random.shuffle(options)
        answer_idx = options.index(incorrect_opt) + 1
        explanation = f"정답은 {answer_idx}번입니다. <br><b>[옳지 않은 설명]</b> {incorrect_opt}<br><b>[나머지 보기]</b> 모두 올바른 설명입니다."

    return {
        "id": f"1-1-theory-{index}",
        "concept": f"1-1. 지급보험금 계산 > {topic['title']}",
        "question": question_text,
        "options": options,
        "answer": answer_idx,
        "explanation": explanation
    }

def generate_double_insurance_question(index):
    # 중복보험 (독립책임액 비례분담)
    market_value = random.randint(5, 10) * 100000000 # 5억~10억
    loss = int(market_value * random.uniform(0.1, 0.5) / 1000000) * 1000000
    
    # A사, B사 가입 (합계가 가액 초과)
    ia_a = int(market_value * random.uniform(0.6, 0.9) / 10000000) * 10000000
    ia_b = int(market_value * random.uniform(0.6, 0.9) / 10000000) * 10000000
    
    # 독립책임액 계산 (각각 별도로 계산했을 때 지급할 금액)
    indep_a = min(loss, ia_a) # 실손보상 가정 (간단화)
    indep_b = min(loss, ia_b)
    sum_indep = indep_a + indep_b
    
    # A사 분담액 = 손해액 * (A독립 / (A독립 + B독립))
    payment_a = int(loss * (indep_a / sum_indep))
    
    options = [
        payment_a,
        int(loss / 2),
        ia_a,
        int(loss * (ia_a / (ia_a + ia_b))) # 가입금액 비례 (오답)
    ]
    random.shuffle(options)
    
    q_data = {
        "id": f"1-1-double-{index}",
        "concept": "1-1. 지급보험금 계산 > 중복보험",
        "question": f"보험가액 {format_currency(market_value)} 건물에 A화재 {format_currency(ia_a)}, B화재 {format_currency(ia_b)}을 각각 가입하였다. {format_currency(loss)} 손해 발생 시 A화재의 분담액은? (단, 독립책임액 비례분담 방식 적용)",
        "options": [format_currency(o) for o in options],
        "answer": options.index(payment_a) + 1,
        "explanation": f"중복보험 분담 산식(독립책임액 비례): 손해액 × (자사 독립책임액 / 독립책임액 합계). \n1. A사 독립책임액: {format_currency(indep_a)} (손해액 한도)\n2. B사 독립책임액: {format_currency(indep_b)}\n3. A사 분담액: {format_currency(loss)} × ({format_currency(indep_a)} / {format_currency(sum_indep)}) = {format_currency(payment_a)}"
    }
    return q_data

def generate_debris_removal_question(index):
    # 잔존물 제거비용 (손해액의 10% 한도)
    loss = random.randint(1, 5) * 10000000 # 1천~5천
    debris_cost_real = int(loss * random.uniform(0.05, 0.2)) # 실제 발생비용 (5~20%)
    
    limit_10 = int(loss * 0.1) # 한도: 손해액의 10%
    payable_debris = min(debris_cost_real, limit_10)
    
    total_payment = loss + payable_debris
    
    options = [
        total_payment,
        loss + debris_cost_real, # 한도 무시 (오답)
        loss,
        loss + int(debris_cost_real * 0.8)
    ]
    random.shuffle(options)
    
    q_data = {
        "id": f"1-1-debris-{index}",
        "concept": "1-1. 지급보험금 계산 > 잔존물제거비용",
        "question": f"화재로 인한 직접 손해액이 {format_currency(loss)}이고, 잔존물 제거비용이 {format_currency(debris_cost_real)} 발생하였다. 지급받을 총 보험금은? (단, 전부보험이며 가입금액 한도 내라고 가정)",
        "options": [format_currency(o) for o in options],
        "answer": options.index(total_payment) + 1,
        "explanation": f"잔존물 제거비용은 '손해액의 10%'를 한도로 보상합니다. \n1. 한도액: {format_currency(loss)} × 10% = {format_currency(limit_10)}\n2. 인정액: Min({format_currency(debris_cost_real)}, {format_currency(limit_10)}) = {format_currency(payable_debris)}\n3. 총 지급액: {format_currency(loss)} + {format_currency(payable_debris)} = {format_currency(total_payment)}"
    }
    return q_data

def main():
    questions = []
    generated_hashes = set()
    
    max_retries = 2000
    count = 0
    
    while len(questions) < NUM_QUESTIONS and count < max_retries:
        count += 1
        r = random.random()
        
        # Generator dispatch
        if r < 0.3:
            q_func = generate_pro_rata_question
        elif r < 0.5:
            q_func = generate_coinsurance_question
        elif r < 0.7:
            q_func = generate_double_insurance_question
        elif r < 0.85:
            q_func = generate_debris_removal_question
        else:
            q_func = generate_theory_question
            
        q_data = q_func(len(questions))
        
        # Uniqueness Check
        # For calculation problems, checks 'question' text (which contains numbers) + options + answer
        # For theory problems, checks 'question' text + sorted options + answer
        q_hash = (q_data['question'], q_data['answer'], tuple(sorted(q_data['options'])))
        
        if q_hash in generated_hashes:
            continue
            
        generated_hashes.add(q_hash)
        questions.append(q_data)
            
    if len(questions) < NUM_QUESTIONS:
        print(f"Warning: Only generated {len(questions)} unique questions out of {NUM_QUESTIONS}")
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(questions)} unique questions in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

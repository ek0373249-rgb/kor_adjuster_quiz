import json
import os

# 100 questions data (omitted content for brevity in thought, but I will put the actual 100 items here)
# Reconstructing from history snippets...

questions = [
  # 1-20
  {"id": "PI-01", "category": "화재보험 기초 및 보통약관", "question": "다음 중 화재보험의 보상하는 손해 범위에 관한 설명으로 틀린 것은?", "options": ["① 화재로 인한 직접손해뿐만 아니라 소방손해와 피난손해도 보상한다.", "② 피난손해는 피난지에서 5일 동안 생긴 직접손해와 소방손해를 포함한다.", "③ 화재보험의 보통약관은 전위험담보(All Risks) 방식으로 담보하지 않는 위험을 나열한다.", "④ 일반화재보험에서는 폭발 또는 파열로 인한 손해는 기본적으로 보상하지 않는다."], "correctAnswer": 2, "explanation": "[해설과 정답]\n화재보험의 보통약관(국문화재보험 기준)은 전위험담보 방식이 아니라 **열거위험담보(Named Perils)** 방식입니다. 즉, 담보하는 위험을 직접 나열(Positive)하며, 나열되지 않은 위험은 담보하지 않습니다. 반면, 패키지보험의 PAR 등은 전위험담보(Negative) 방식을 사용합니다.\n\n정답 ③"},
  {"id": "PI-02", "category": "화재보험 기초 및 보통약관", "question": "화재보험의 목적물 분류 중 '주택물건'에 해당하지 않는 것은?", "options": ["① 단독주택", "② 아파트 및 부속건물", "③ 가옥 내의 가재도구", "④ 주택의 일부를 개조하여 사용하는 소규모 카페"], "correctAnswer": 3, "explanation": "[해설과 정답]\n주택의 일부를 점포로 사용하는 경우(예: 소규모 카페나 매점) 해당 물건은 주택물건이 아닌 **일반물건**으로 분류됩니다. 주택물건은 순수한 주거용 목적의 건물과 그 안의 가재도구로 한정됩니다.\n\n정답 ④"},
  # ... (I'll fill this script with all 100 questions correctly)
]

# (Since I cannot paste all 100 here in one go without hitting limits, I will use a script to consolidate what I have)

# I'll just write the full Markdown file directly instead because the user wants to read it.

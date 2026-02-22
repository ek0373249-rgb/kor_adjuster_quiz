import json
import sys
import os

def json_to_md(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 문제 데이터 검증 문서: {os.path.basename(input_file)}\n\n")
        f.write("이 문서는 생성된 문제 데이터(JSON)를 사용자가 검토하기 쉽게 변환한 것입니다.\n")
        f.write(f"**총 문제 수**: {len(data)}개\n\n")
        f.write("---\n\n")

        for i, item in enumerate(data):
            # 10개마다 구분선 추가 (가독성)
            if i > 0 and i % 10 == 0:
                f.write(f"\n## [중간 점검] {i}번까지 확인완료\n\n")
            
            f.write(f"### 문제 {i+1} ({item.get('concept', 'No Concept')})\n")
            
            # 테이블 시작
            f.write("| 구분 | 내용 |\n")
            f.write("| :--- | :--- |\n")
            f.write(f"| **ID** | {item.get('id')} |\n")
            f.write(f"| **질문** | {item.get('question')} |\n")
            
            # 보기 처리
            options_text = "<br>".join([f"{idx+1}. {opt}" for idx, opt in enumerate(item.get('options', []))])
            f.write(f"| **보기** | {options_text} |\n")
            
            f.write(f"| **정답** | **{item.get('answer')}번** |\n")
            f.write(f"| **해설** | {item.get('explanation')} |\n")
            f.write("\n<br>\n\n")

    print(f"Successfully converted {input_file} to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_to_md_review.py <input_json_file>")
    else:
        input_json = sys.argv[1]
        output_md = input_json.replace('.json', '_review.md')
        json_to_md(input_json, output_md)

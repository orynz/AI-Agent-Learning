"""
Hugging Face의 tokenizers 라이브러리를 사용해 
나만의 맞춤형 토크나이저(BPE 알고리즘 기반)를 직접 설계하고 
학습시키기 위한 실습 과정을 담고 있습니다.
"""

from tokenizers import (
    Tokenizer,  # 모델, 전처리기 등을 조립
    models,     #  토큰화 알고리즘
)
from tokenizers.pre_tokenizers import Whitespace # 문장을 단순히 공백(띄어쓰기) 기준으로 나눕
from tokenizers.trainers import BpeTrainer # BPE 알고리즘을 학습시킬 때 필요한 세부 설정(어휘 사전 크기, 최소 빈도수, 특수 토큰 등)을 담당

from pathlib import Path
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# 초기화
tokenizer = Tokenizer(model=models.BPE()) 
tokenizer.pre_tokenizer = Whitespace()

txt_path = data_dir / "sample.txt"
if not txt_path.exists():
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("오늘 비가와서 기분이 너무 별로입니다. 내일은 날씨가 좋기를 바랍니다.")
        
trainer = BpeTrainer(
    vocab_size=8000,          # 모델이 배울 전체 단어(토큰) 사전의 최대 크기 제한(실제 KoBERT는 약 8,000~10,000 사용)
    min_frequency=2,          # 최소 2번 이상 등장한 단어 조합만 사전에 등록하여 노이즈를 방지합니다.
    special_tokens=[          # 학습 시 특별한 의미를 부여할 5가지 특수 토큰을 정의합니다.
        "[PAD]",              # 1. 문장 길이를 맞추기 위한 빈칸 채우기용 토큰
        "[UNK]",              # 2. 사전에 없는 모르는 단어 처리용 토큰
        "[CLS]",              # 3. 문장 전체의 의미를 담는 시작 지점 토큰
        "[SEP]",              # 4. 문장과 문장을 구분하는 구분자 토큰
        "[MASK]"              # 5. 모델 학습을 위해 단어를 가리는 마스크 토큰
    ]
)

# 학습 실행
training_files = list(map(str, [txt_path]))
tokenizer.train(files=training_files, trainer=trainer)

# 결과 저장
training_path = data_dir / "bpe_tokenizer.json"
tokenizer.save(str(training_path))

# 로드 및 테스
new_tokenizer = Tokenizer.from_file(str(training_path))
output = new_tokenizer.encode("오늘 비가와서 기분이 너무 별로입니다.")
print(f"Tokens: {output.tokens}")
print(f"IDs: {output.ids}")
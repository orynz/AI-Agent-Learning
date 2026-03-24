from tokenizers import (
    Tokenizer, 
    models, 
)
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import WordPieceTrainer # BPE 대신 WordPieceTrainer 사용
from pathlib import Path

# 경로 설정
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# 초기화: WordPiece 모델 사용
# WordPiece는 초기화 시 unk_token을 정의해주는 것이 좋습니다.
tokenizer = Tokenizer(model=models.WordPiece(unk_token="[UNK]")) 
tokenizer.pre_tokenizer = Whitespace()

# 학습 파일 설정
txt_path = data_dir / "sample.txt"
if not txt_path.exists():
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("오늘 비가와서 기분이 너무 별로입니다. 내일은 날씨가 좋기를 바랍니다.")

# Trainer 설정: WordPieceTrainer 사용
trainer = WordPieceTrainer(
    vocab_size=8000, 
    min_frequency=2, 
    limit_alphabet=1000, # 한글 자모 기본 유니코드 범위 내에서 알파벳 제한 (한글 음절 조합 최적화)
    special_tokens=[
        "[PAD]", 
        "[UNK]", 
        "[CLS]", 
        "[SEP]", 
        "[MASK]"
    ],
    continuing_subword_prefix="##" # WordPiece의 핵심: 중간 토큰 식별자
)

# 학습 진행
training_files = [str(txt_path)]
tokenizer.train(files=training_files, trainer=trainer)

# 저장 및 로드
training_path = data_dir / "wordpiece_tokenizer.json"
tokenizer.save(str(training_path))
new_tokenizer = Tokenizer.from_file(str(training_path))

# 테스트 실행
test_sentence = "오늘 비가와서 기분이 너무 별로입니다."
output = new_tokenizer.encode(test_sentence)

print(f"입력 문장: {test_sentence}")
print(f"토큰화 결과: {output.tokens}")
print(f"ID 결과: {output.ids}")
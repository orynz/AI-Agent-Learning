""""
이 코드의 목적은 '사람의 언어'를 '컴퓨터의 숫자(벡터)'로 바꾸는 것
"""

from transformers import AutoTokenizer
from datasets import load_dataset
from pathlib import Path
    
CACHE_DIR = Path(__file__).parent / "data" / "hf_datasets"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 모델 호출: 'rotten_tomatoes'(영화 리뷰 감성 분석 데이터)
dataset = load_dataset(
    "rotten_tomatoes",
    cache_dir=str(CACHE_DIR),
    download_mode="reuse_dataset_if_exists",
)

# 다국어를 지원하는 BERT 모델의 토크나이저를 가져옵니다.
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# 기초 테스트: 문장을 숫자로 바꾸는 과정 확인
sentences = ["반갑습니다.", "허깅페이스 데이터셋 전처리를 배우는 중입니다."]
encoded = tokenizer(
    sentences, 
    padding="max_length",  # 길이를 맞추기 위해 부족한 부분은 채움
    max_length=10,         # 최대 길이를 10으로 설정
    truncation=True,       # 길면 자름
)

print("기초 테스트 인코딩 ID:", encoded["input_ids"])

# 데이터셋의 각 문장을 한꺼번에 토크나이징하는 함수를 정의합니다.
def tokenize_fn(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

# .map()을 사용하여 전체 데이터셋에 함수를 적용합니다. (batched=True로 속도 향상)
tokenized_dataset = dataset.map(tokenize_fn, batched=True)

print("추가된 컬럼:", tokenized_dataset["train"].column_names)

# 파이토치(PyTorch) 모델에 바로 넣을 수 있도록 텐서(Tensor) 형식으로 변환합니다.
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# 최종 확인
final_sample = tokenized_dataset["train"][0]
print("최종 데이터 타입 확인:", type(final_sample["input_ids"]))
print("첫 번째 샘플 텐서 크기:", final_sample["input_ids"].shape)

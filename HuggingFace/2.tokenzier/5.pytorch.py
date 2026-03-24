from transformers import AutoTokenizer
from datasets import load_dataset
from pathlib import Path
    
CACHE_DIR = Path(__file__).parent / "data" / "hf_datasets"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

dataset = load_dataset(
    "rotten_tomatoes",
    cache_dir=str(CACHE_DIR),
    download_mode="reuse_dataset_if_exists",
)


tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
sentences = ["반갑습니다.", "허깅페이스 데이터셋 전처리를 배우는 중입니다."]

encoded = tokenizer(
    sentences, 
    padding="max_length",  # 짧은 문장은 0(PAD)으로 채워 길이를 맞춤
    max_length=10, truncation=True, # max_length(10)보다 긴 문장은 자름
)

print("기초 테스트 인코딩 ID:", encoded["input_ids"])

# --- [2. 전체 데이터셋 일괄 전처리 함수] ---
# 데이터셋의 각 샘플(examples)을 받아서 토크나이징을 수행하는 함수를 정의합니다.
def tokenize_fn(examples):
    # 'text' 컬럼의 데이터를 가져와 128 길이에 맞춰 변환합니다.
    # return되는 값에는 input_ids, attention_mask 등이 포함됩니다.
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

# map 함수를 사용하여 전체 데이터셋에 tokenize_fn을 적용합니다.
# batched=True: 데이터를 하나씩 처리하지 않고 묶음으로 처리하여 속도를 대폭 향상시킵니다.
tokenized_dataset = dataset.map(tokenize_fn, batched=True)

# 전처리가 완료된 후 데이터셋에 어떤 컬럼들이 새로 생겼는지 확인합니다.
print("추가된 컬럼:", tokenized_dataset["train"].column_names)

# --- [3. 모델 학습을 위한 포맷 변환] ---
# 학습에 불필요한 원본 텍스트 등은 제외하고, 모델 입력에 필요한 컬럼만 추출하여 
# 파이토치(PyTorch) 텐서(Tensor) 형식으로 변환합니다.
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# 변환이 잘 되었는지 첫 번째 데이터를 꺼내 확인합니다.
final_sample = tokenized_dataset["train"][0]

# input_ids의 데이터 타입을 출력하여 'torch.Tensor'가 나오는지 확인합니다.
print("최종 데이터 타입 확인:", type(final_sample["input_ids"]))
# 실제 텐서 데이터의 형태(Shape)도 확인해봅니다. (길이가 128인지 확인)
print("첫 번째 샘플 텐서 크기:", final_sample["input_ids"].shape)


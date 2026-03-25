import torch
import re
import pandas as pd
from datasets import load_from_disk, Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification, 
    TrainingArguments, 
    Trainer,
    DataCollatorWithPadding
)
import torch.nn.functional as F                  # 확률 계산을 위한 소프트맥스 함수용 임포트

from utils import get_logger, timer, path_mgr
log = get_logger(name="spam_mail_pipeline.py", log_dir="./logs")

BASE_DIR = path_mgr.get_dir("data")
RESULTS_DIR = path_mgr.get_dir("data", "results")
DATASETS_DIR = path_mgr.get_dir("data", "custom_datasets")
CHECKPOINT_DIR = path_mgr.get_dir("data", "checkpoints")

csv_file_path = DATASETS_DIR / "spam_mail_raw_data.csv"
dataset_path = DATASETS_DIR / "spam_mail_dataset"
train_model_path = DATASETS_DIR / "spam_mail_model"

PRETRAINED_MODEL_NAME = "bert-base-multilingual-cased"

# 토큰화 (Tokenization)
tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)

def clean_text_for_dl(example):
    """
    허깅페이스 Dataset.map()에 적용할 클리닝 함수입니다.
    """
    
    text = str(example['text'])
    
    # 한글, 영문, 숫자, 공백을 제외한 모든 특수문자 제거 (주.식/투.자 -> 주식투자)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)
    
    # 다중 공백을 단일 공백으로 압축
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 깨끗해진 텍스트로 덮어쓰기
    example['text'] = text
    return example

@timer(log)
def vectorization():
    """
    텍스트 벡터화
    """
    
    # 원본 CSV 데이터 로드
    df = pd.read_csv(csv_file_path, encoding="utf-8-sig", sep=',')
    raw_dataset = Dataset.from_pandas(df)
    
    # 텍스트 클리닝 진행 (특수문자 노이즈 제거)
    cleaned_dataset = raw_dataset.map(clean_text_for_dl)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    tokenized_dataset = cleaned_dataset.map(tokenize_function, batched=True)
    split_dataset = tokenized_dataset.train_test_split(test_size=0.2, seed=42)
    
    tokenized_ds = split_dataset.remove_columns(["text"])
    tokenized_ds.set_format(type="torch")

    print("---------------- 커스텀 데이터셋 준비 완료 --------------------")
    print("출력 결과에 'input_ids', 'attention_mask', 'label'이 보여야 합니다.")
    print("\n컬럼 목록:", tokenized_ds['train'].column_names) 
    print("첫 번째 데이터 샘플:\n", tokenized_ds['train'][0])
    
    tokenized_ds.save_to_disk(str(dataset_path))
    print(f"데이터셋 저장 완료: {dataset_path}")

@timer(log)
def model_training():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"현재 사용 중인 장치: {device.upper()}")
    if device == "cpu":
        print("⚠️ 주의: GPU가 없습니다. 학습 속도가 매우 느릴 수 있습니다.")
    
    # 데이터 및 토크나이저 로드
    tokenized_ds = load_from_disk(str(dataset_path))
    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)

    # 모델 로드 및 장치 이동
    model = AutoModelForSequenceClassification.from_pretrained(PRETRAINED_MODEL_NAME, num_labels=2)
    model.to(device) # CPU면 CPU로, GPU면 GPU로 명시적 이동

    # 장치 맞춤형 동적 설정 (CPU vs GPU 분기)
    use_fp16 = True if device == "cuda" else False
    num_workers = 2 if device == "cuda" else 0 # CPU에서는 다중 프로세싱이 오히려 병목/에러를 유발할 수 있음

    # 학습 환경 설정
    training_args = TrainingArguments(
        output_dir=str(CHECKPOINT_DIR),  
        learning_rate=2e-5,             
        per_device_eval_batch_size=16,
        per_device_train_batch_size=8, 
        num_train_epochs=3,
        weight_decay=0.01,              
        
        # --- 장치별 동적 설정 적용 ---
        fp16=use_fp16,                       
        dataloader_num_workers=num_workers,  
        
        save_strategy="epoch",                  
        eval_strategy="epoch",                  
        load_best_model_at_end=True,            
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # 트레이너 정의
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_ds['train'], # 실제 학습에 사용할 데이터 전달
        eval_dataset=tokenized_ds['test'],   # 학습이 잘 되었는 검사할 데이터 전달
        data_collator=data_collator          # 텐서 묶음 처리기 알려주기
    )
    
    # 학습 시작
    mode_text = "고속 연산 모드(GPU)" if device == "cuda" else "최저 사양 호환 모드(CPU)"
    print(f"\n------------ {mode_text}로 학습을 시작합니다. ------------")
    try:
        trainer.train()
    except Exception as e:
        print(f"\n❌ 학습 중 에러 발생: {e}")
        raise e

    # 최종 학습 데이터 저장
    # 모델과 토크나이저를 함께 저장해야 나중에 예측(추론)할 때 문제가 생기지 않습니다.
    model.save_pretrained(train_model_path)
    tokenizer.save_pretrained(train_model_path)
    
    print(f"\n✅ 학습 및 모델 저장 완료: {train_model_path}")

def predict_sentiment(text):
    """문장을 입력받아 긍정/부정 결과를 반환하는 함수"""
    
    model = AutoModelForSequenceClassification.from_pretrained(train_model_path)
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding = True, max_length=128)
    
    with torch.no_grad():
        outputs = model(**inputs)

    # 결과 해석 (Logits -> Softmax 확률 변환)
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)            # 각 라벨(0, 1)에 대한 확률 계산
    
    prediction = torch.argmax(probs, dim=-1).item() # 가장 확률이 높은 값의 클래스 인덱스 선택
    conf = torch.max(probs).item() * 100 # 퍼센트로 변환
    
    sentiment = "긍정(Positive)" if prediction ==1 else "부정(Negative)"
    print(f"\n입력문자: {text}")
    print(f"분석 결과: {sentiment} ({conf:.2f}# 확신)")
    
if __name__ == "__main__":
    # vectorization()
    # model_training()
    
    while True:
        text = input("분석할 리뷰를 입력하세요: ")
        predict_sentiment(text)
    pass
from datasets import load_from_disk
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

from utils import timer, get_logger

from pathlib import Path
dir = Path(__file__).parent 
results_dir = dir / "results"
datasets_dir =  dir / "data" / "datasets"
my_dataset_path = datasets_dir / "my_custom_dataset"
my_train_path = dir / "my_movie_model"

results_dir.mkdir(parents=True, exist_ok=True)

log = get_logger(name="model_train.py", log_dir="./logs")

@timer(log)
def process():
        
    if not dir.exists():
        print(f"오류: {dir} 폴더가 없습니다.")

    # 데이터 로드
    tokenized_ds = load_from_disk(str(my_dataset_path))

    # 분류(긍정/부정) 모델 로드
    model_name = "bert-base-multilingual-cased"
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # 학습 환경 설정
    training_args = TrainingArguments(
        output_dir= str(results_dir),  # 학습중 생성되는 체크포인트 저장소
        learning_rate= 2e-5,            # 모델이 학습할 때 가중치를 얼마나 세밀하게 조정할지 결정하는 학습률
        per_device_eval_batch_size= 8,  # 한 번에 학습시킬 문장의 갯수
        num_train_epochs= 3,            # 반복 횟수=> 최적의 횟수를 찾아야 함!
        weight_decay=0.01,              # 과적합 방지(모델이 특정 데이터에 집착하는 경향이 있음)
        logging_dir="./logs",
        remove_unused_columns=False     # 데이터셋의 모든 열을 보존해서 학습시 발생할 수 있는 데이터 누락 방지
    )
    
    # 트레이너 정의
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_ds['train'], # 실제 학습에 사용할 데이터 전달
        eval_dataset=tokenized_ds['test'], # 학습이 잘 되었는 검사할 데이터 전달
    )
    
    # 학습 시작
    print("------------ 최저 사양 호환 모드로 학습을 시작합니다. ------------")
    try:
        trainer.train()
    except TypeError as e:
        print(f"TypeError> {e}")
        raise e

    # 최종 학습 데이터 저장
    model.save_pretrained(my_train_path)
    print(f"학습 데이터 저장 완료: {my_train_path}")
if __name__ == "__main__":
    process()
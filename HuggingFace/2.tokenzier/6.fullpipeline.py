import pandas as pd
from transformers import AutoTokenizer
from datasets import Dataset

def main():
    from pathlib import Path
    CACHE_DIR = Path(__file__).parent / "data" / "hf_datasets"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "content": [
            "이 영화 정말 최고! 꼭 보세요.",
            "시간 아까워요. 절대 보지 마세요!",
            "그냥 평범한 연기였습니다.",
            "연기력이 대박이네요. 감동적입니다.",
            "스토리가 너무 뻔해서 지루했어요."
        ],
        "label": [1, 0, 1, 1, 0] # 1: 긍정 / 0: 부정
    }

    df = pd.DataFrame(data=data)
    raw_dataset = Dataset.from_pandas(df)

    ds_split = raw_dataset.train_test_split(test_size=0.2)

    tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

    def preprocess_fn(examples):
        return tokenizer(examples["content"], padding="max_length", truncation=True, max_length=64)

    tokenized_ds = ds_split.map(preprocess_fn, batched=True)
    tokenized_ds = tokenized_ds.remove_columns(["content"])
    tokenized_ds.set_format(type="torch")

    print("---------------- 커스텀 데이터셋 준비 완료 --------------------")
    print(tokenized_ds)
    print(tokenized_ds['train'][0])
    tokenized_ds.save_to_disk(str(CACHE_DIR/"my_custom_dataset"))


if __name__ == "__main__":
    main()


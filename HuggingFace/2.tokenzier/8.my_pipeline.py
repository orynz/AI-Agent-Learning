import pandas as pd
from transformers import AutoTokenizer
from datasets import Dataset
from utils import get_logger, timer

log = get_logger(name="my_pipeline.py", log_dir="./logs")
@timer(log)
def main():
    from pathlib import Path
    CACHE_DIR = Path(__file__).parent / "data" / "datasets"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv("movie.csv", encoding="utf-8-sig", sep=',')
    raw_dataset = Dataset.from_pandas(df)

    ds_split = raw_dataset.train_test_split(test_size=0.2, seed=42)

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


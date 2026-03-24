from datasets import load_dataset
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "data" / "hf_datasets"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

dataset = load_dataset(
    "rotten_tomatoes",
    cache_dir=str(CACHE_DIR),
    download_mode="reuse_dataset_if_exists"
)

print(f"데이터 구조> {dataset}")
print(f"샘플: {dataset['train'][0]}")
print(f"문장: {dataset["train"][0]['text']}")
print(f"정답: {dataset["train"][0]['label']}")
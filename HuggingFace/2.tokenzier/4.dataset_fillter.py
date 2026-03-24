from datasets import load_dataset
from pathlib import Path

try:
    base_path = Path(__file__).parent
except NameError:
    base_path = Path.cwd()
    
CACHE_DIR = base_path / "data" / "hf_datasets"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

dataset = load_dataset(
    "rotten_tomatoes",
    cache_dir=str(CACHE_DIR),
    download_mode="reuse_dataset_if_exists"
)

# 데이터 가공 (필터링 및 정제)
clean_dataset = dataset["train"].filter(lambda x: len(x["text"]) > 50)
print(f"✅ 전체 리뷰 중 50자 이상 고품질 리뷰 개수: {len(clean_dataset)}")

# 셔플 (학습 편향 방지)
shuffled_dataset = dataset["train"].shuffle(seed=42)

# 데이터 분할 (Train / Test Split)
final_split = shuffled_dataset.train_test_split(test_size=0.1, seed=42)


# 결과 확인
train_data = final_split["train"]
test_data = final_split["test"]

print("-" * 30)
print(f"📝 최종 학습 데이터 개수: {len(train_data)}")
print(f"📝 최종 테스트 데이터 개수: {len(test_data)}")
print(f"💡 샘플 문장: {train_data[0]['text'][:50]}...")
print(f"💡 샘플 정답: {train_data[0]['label']} (0:부정, 1:긍정)")

# 참고용: 정렬 (데이터 특성 파악용)
sorted_dataset = train_data.sort("text")
print(f"📏 현재 세트에서 가장 짧은 리뷰: {sorted_dataset[0]['text']}")
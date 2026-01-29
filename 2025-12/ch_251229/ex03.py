import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie"],
    "score": [85, 90, 78]
}

df = pd.DataFrame(data)
print(df, end='\n\n')

print("평균 점수:", df["score"].mean())
print("최고 점수:", df["score"].max())
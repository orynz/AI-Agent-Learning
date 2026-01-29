import os, pandas as pd

base = "./"
os.makedirs(base, exist_ok=True)
csv_path = f"{base}sample.csv"

if not os.path.exists(csv_path):
    df = pd.DataFrame({
        "day": ["Mon","Tue","Wed","Thu","Fri"],
        "visitors": [120, 98, 143, 160, 132]
    })
    df.to_csv(csv_path, index=False)
else:
    print("이미 같은 파일이 존재합니다.")

print("CSV 위치:", csv_path)

def test():
    print("test method")
    
import matplotlib.pyplot as plt

df = pd.read_csv(csv_path)
print(df.head())

plt.figure()
plt.plot(df["day"], df["visitors"], marker="o")
plt.title("Weekday Visitors")
plt.xlabel("Day"); plt.ylabel("Visitors")
plt.grid(True)
plt.show()

test()

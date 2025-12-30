"""
워드클라우드 실습
"""


import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv("quotes.csv")
text = " ".join(df["Quote"])
print(text)
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    font_path=None
).generate(text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

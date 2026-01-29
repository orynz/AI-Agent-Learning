import matplotlib.pyplot as plt

labels = ["ChatGPT","Claude","Gemini"]
scores = [92, 89, 87]

plt.figure()
plt.bar(labels, scores)
plt.title("Model Scores (Example)")
plt.xlabel("Models"); plt.ylabel("Score")

for i, v in enumerate(scores):
    plt.text(i, v + 0.5, str(v), ha="center")

plt.show()
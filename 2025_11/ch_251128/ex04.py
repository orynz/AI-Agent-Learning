

nums = list(range(1, 21))
# 홀수만 골라 합계를 구하라(반복문 또는 컴프리헨션).

words = ["AI", "data", "python", "model"]
# 각 단어의 길이로 구성된 리스트를 생성하라.
lengths = [len(word) for word in words]
print(lengths)

views = [120, 98, 450, 310, 260]
# 오름차순 정렬 후 가장 큰 2개만 남겨 새 리스트를 만들라.
views.sort()
views = views[-2:]
print(views)
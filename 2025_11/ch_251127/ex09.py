scores = [88, 92, 79, 100, 86]
# 평균과 최댓값을 출력하라.
print("평균 : ", sum(scores)/len(scores), end = " / ")
print("최댓값 : ", max(scores))

nums = list(range(1, 21))
# 홀수만 골라 합계를 구하라(반복문 또는 컴프리헨션).
print("합계: ", sum(nums[::2]))

odds = [n for n in nums if n % 2 == 1]
print("합계: ", sum(odds))

words = ["AI", "data", "python", "model"]
# 각 단어의 길이로 구성된 리스트를 생성하라.
nums = [len(n) for n in words]
print("단어 길이 리스트", nums)

views = [120, 98, 450, 310, 260]
# 오름차순 정렬 후 가장 큰 2개만 남겨 새 리스트를 만들라.
views.sort()
print(views)
views = views[-2:]
print("가장 큰수 2개: ", views)
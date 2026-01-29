import numpy as np

scores = [70, 75, 80, 85, 90, 95]

print("데이터 개수:", len(scores))
print("평균:", np.mean(scores))
print("최댓값:", np.max(scores))
print("최솟값:", np.min(scores))

numbers = np.array([1, 2, 3, 4, 5])
print("합계:", np.sum(scores))


num = np.array([[1, 2, 3], [4, 5, 6]])
num = np.array(scores, ndmin=5)
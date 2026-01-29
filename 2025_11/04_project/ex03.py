import numpy as np, pandas as pd, matplotlib

# 패키지 버전 확인 : numby
print("NumPy:", np.__version__)

# 패키지 버전 확인 : pandas
print("Pandas:", pd.__version__)

# 패키지 버전 확인 : matplotblib
print("Matplotlib:", matplotlib.__version__)

# 리스트 a, b 생성
a = np.array([1,2,3]); b = np.array([4,5,6])

# 내적(dot) : 두 벡터의 각 요소를 곱한 후 그 값들을 모두 더하는 연산
print("내적:", np.dot(a,b))

# 평균(mean) : 배열의 모든 요소를 더한 뒤, 총 요소의 개수로 나누는 값
print("A 평균:", np.mean(a)) # (1+2+3) / 3 = 2
print("B 평균:", np.mean(b)) # (4+5+6) / 3 = 5
print("A+B 평균:", np.mean(a+b)) # (1+2+3+4+5+6) / 6 = 7


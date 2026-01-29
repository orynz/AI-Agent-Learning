scores = [80, 90, 100, 70]
print(scores)           # 모든 요소 출력
print(scores[0])        # 첫 번째(0번) 원소
print(scores[-1])       # 뒤에서 첫 번째 원소
print(len(scores))      # 길이(원소 개수) - `len`


# 반복문을 활용한 total 누적
total = 0
idx = 0
while idx < len(scores):
    total += scores[idx]
    idx += 1

print("total: ", total)

# 다양한 자료형과 혼합 저장
mix_l = [1, "AI", True, 3.14] # 리스트: 값을 접근, 수정 모두 가능.
mix_t = (1, "AI", True, 3.14) # 튜플: 값 접근 가능 그러나 수정 불가능.
print(mix_l)
print(mix_t)

mix_l[1] = "Apple"
print(mix_l)
mix_t[1] = "Orange"
print(mix_t)
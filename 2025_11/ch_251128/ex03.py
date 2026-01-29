# 5.2부터5.2.5Rkwl


scores = [80, 90, 100, 70, 20]
print(scores[0])
print(scores[-1])
print(len(scores))

total = 0
for s in scores:
    total += s

avg = total / len(scores)
print(total, avg, max(scores), min(scores))

for idx, s in enumerate(scores):
    print(idx, s)

scores = [80, 90, 100, 70]
scores.append(85)        # [80, 90, 100, 70, 85]
# scores.sort()            # [70, 80, 85, 90, 100]
# top = scores.pop(-1)     # 최댓값 꺼내기(삭제)
# print(scores, top)

if 85 not in scores:
    scores.append(85)
print(scores)
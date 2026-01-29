# 각 월의 일수 리스트 준비
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# print(len(days))

# 12달의 총 일수 출력
total = 0
for day in days:
    total+= day

# print(total)

# 4~8월 까지의 날짜를 while 문으로 누적
idx = 3
total = 0
while idx >= 3 and idx < 8:
    total += days[idx]
    idx += 1

print(total)

#  4~8월 까지의 날짜를 for 문으로 누적
total = 0
for day in days[3:8]:
    total += day
print(total)

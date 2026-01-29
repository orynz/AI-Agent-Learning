# 1~10까지 총합 출력

# 1. 1~10 출력
# num = 0
# for i in range(1, 11):
#     num += i
#     pass

# print(num)

# # 1부터 10까지의 총합을 출력
# # 1부터 10까지 출력
# # 특수문자 
# # '\n', '\t', '\a', '\\'
# num = 1
# # num을 누적하는 변수 (누적변수는 초기화 필수)
# total = 0
# while num <= 10:
#     print(num, end= (' + 'if num<10 else' = ') )
#     total += num
#     num += 1

# print(total)

# # 1~100까지 짝수의 합 - while문 사용
num = 1
total = 0

while num <= 100:
    if num % 2 == 0:
        print(num, end= ('+'if num<100 else'=') )
        total += num        
    num += 1
    pass
print(total)




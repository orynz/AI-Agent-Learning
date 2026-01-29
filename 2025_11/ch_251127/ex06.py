# 범위 출력
# for i in range(1, 5):
#     print(i)
#     pass

# i = 1
# while i < 5:
#     print(i)
#     i += 1
#     pass



#  구구단 2단 출력
# dan = 2
# i = 1
# while i <= 9:
#     print(f'{dan} x {i} = {2*i}')
#     i += 1


# 구구단 출력 - while문
# dan = 2
# while dan <= 9:
#     i = 1
#     print(f'{"-" * 5} {dan}단 {"-" * 5}')
    
#     while i <= 9:
#         print(f'{dan} x {i} = {2*i}')
#         i += 1
#     dan += 1


# 구구단 출력 - for문
# for i in range(1, 10): # 1~9 카운트
#     text = ''
#     for j in range(2, 10): # 2~9단
#         text += f"{j:2} {'*'}{i:2} = {i*j:2} |"
#     print(text)


# 시작단, 종료단을 일력 받아서 시작~ 종료까지 구구단 출력


dan = int(input("시작할 단: "))
e_dan = int(input("종료할 단: "))

if dan > e_dan:
    tmp = dan
    dan = e_dan
    e_dan = tmp    

while dan <= e_dan:
    i = 1
    print(f'{"-" * 5} {dan}단 {"-" * 5}')
    
    while i <= 9:
        print(f'{dan} x {i} = {2*i}')
        i += 1
    dan += 1
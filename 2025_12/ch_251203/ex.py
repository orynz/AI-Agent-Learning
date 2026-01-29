# 난수 발생기
import random
import time

# while True:
#     num = random.randint(0, 10)
#     print(num)
#     time.sleep(1)

# random 함수를 사용하며 정수형 난수 하나를 생성(1~100)
# 발생된 난수를 맞추기 게임
# 최대 5번 시도 가능
# 틀리면 높다, 낮다 출려, 
# 5번 초과시 게임 종료
# 정답이면 재시도, 종료 선택 가능



min = 1
max = 10
try_count = 0
num = 0

def run():
    global try_count
    global num
    
    try_count = 5
    num = random.randint(min, max)
    
    while try_count > 0:
        print(f"------------------- 남음 횟수: {try_count}")
        user_num = int(input(f"정수({min} ~ {max}) 입력: "))
        
        if user_num == num:
            text = f"짝!짝!짝! 정답~~"
            print(text)
            
            replay = input("다시 도전 할래? (y/n): ")
            if replay == "y":
                try_count = 5
                num = random.randint(min, max)
                continue
            else:
                break
            
        else:
            text = f"{user_num} 보다 크다" if num > user_num  else f"{user_num} 보다 작다"
            print(text)
        
        try_count -= 1
    
    if try_count <= 0:
        print(f"게임 종료! 정답은 {num} 입니다.")

run()























# # 도전 문제
# # menu() 함수에서 no 변수에 새값을 입력 받고 run() 함수에서 입력 받은 값을 확인하기
# # 6을 입력 받으면 반복문 종료


# no = 0

# def menu():
#     # 전역변수 no에 사용자의 입력값 할당
#     global no
#     no = int(input("선택: "))

# def run():
#     # 전역변수 no 값 출력
#     print(no)


# while no != 6 :
#     menu()
#     run()
    
    
# print("프로그램을 종료합니다.")
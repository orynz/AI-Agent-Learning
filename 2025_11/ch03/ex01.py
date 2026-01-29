'''
이름(name)과 나이(age)를 입력 받아
미성년인지 성인인지 판별하는 프로그램을 작성하세요.
'''

# name = input("이름: ")
# age = int(input("나이: "))

# if age >= 20:
#     print("당신은 성인입니다.")
# else:
#     print("당신은 미성년입니다.")


## 도전문제
# 정수를 입력 받는다.
# 입력된 정수가 양수인지, 음수인지, 0인지 판별하는 프로그램을 작성하세요.

# num = int(input("정수 입력: "))

# if num > 0:
#     print("'양수'입니다.")
# elif num < 0:
#     print("'음수'입니다.")
# else:
#     print("'0'입니다.")


# 정수를 입력받는다.
# 숫자가 0~100 사이이면 유효한 점수

# score = int(input("점수 입력: "))
# print(f"입력한 점수는 {score}점 입니다.")

# message = "유효하지 않은 접수 입니다."
# if(score > 0) and (score <=100):
#     message = "유효한 점수 입니다."

# print(f"{score}점은 {message}")


# 각각 다른 정수 3개를 입력
# 큰수 작은 수 중간수로 분류하여 출력
# if문 블럭안에 if문을 중첩해서 사용 가능
# 반복문은 아직 배우지 않았으니 사용하지 말 것.
# 논리 연산자 사용하지 말것

# 도전문제 2
# num1 = int(input("첫번째 정수: "))
# num2 = int(input("두번째 정수: "))
# num3 = int(input("세번째 정수: "))

# n_min = n_mid = n_max = 0

# if num1 < num2:
#     n_min = num1
    
#     if num2 < num3:
#         n_max = num3
#         n_mid = num2
#     else:
#         n_max = num2
#         n_mid = num3
        
# elif num1 < num3:
#     n_max = num3
#     n_min = num2
#     n_mid = num1
# else:
#     n_max = num1
    
#     if num2 < num3:
#         n_mid = num3
#         n_min = num2
#     else:
#         n_mid = num2
#         n_min = num3
        
# print(f"큰수: {n_max},  중간수: {n_mid}, 작은수: {n_min}")


num1 = int(input("첫번째 정수: ")) # 3
num2 = int(input("두번째 정수: ")) # 2
num3 = int(input("세번째 정수: ")) # 1
       
if num1 < num2:
   temp = num2
   num2 = num1
   num1 = temp

if num1 < num3:
    temp = num3
    num3 = num1
    num1 = temp

if num2 < num3:
    temp = num3
    num3 = num2
    num2 = temp

print(f"큰수 : {num1}, 중간수 : {num2}, 작은수 : {num3}")






varC = 1000

def funcA():
    global varC
    
    varA = 100
    print("varA의 값: ", varA)
    print("varC의 값: ", varC)
    
    varC = 2000
    print("varC의 값: ", varC)
    
def funcB():
    varB = 10
    print("varB의 값: ", varB)
    print("varC의 값: ", varC)

funcA()
funcB()
























# 연습문제 1
# 다음 함수 호출부를 보고 함수를 구현하세요

# # say_hello()
# def say_hello(name):
#     print("Hello, {0}".format(name))

# # 함수 호출부
# say_hello("철수") # Hello, 철수
# say_hello("영희") # Hello, 영희

# 직접 해보기
# 두 정수를 입력받아서 합한 결고를 반환하는 함수 'add(a+b)'를 구현하세요.

def add(a, b):
    # return a+b
    return a, b, a+b

a =  10
b = 2
sum_value = add(a, b)
print(f"{a} + {b} = {sum_value}")
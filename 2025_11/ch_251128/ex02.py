def mininum(x, y):
    return x if x<y else y

def maximum(x, y):
    return x if x > y else y

num1 = int(input("정수 입력1 : "))
num2 = int(input("정수 입력2 : "))
num3 = int(input("정수 입력3 : "))
num4 = int(input("정수 입력4 : "))

print("최소값 : ", mininum(num1, mininum(num2, mininum(num3, num4))))
print("최대값 : ", maximum(num1, maximum(num2, maximum(num3, num4))))

# 각각 다른 정수 3개를 입력받는다.
# 정수의 크기를 구분해서 max, mid, min 변수에 저장
# if~elif 만 사용. 논리 연산자 사용 제한

a = int(input("정수1: "))
b = int(input("정수2: "))
c = int(input("정수3: "))

print(f"입력된 정수는 {a}, {b}, {c}")

# 결과가 담겨질 변수 미리 선언
max = 0
mid = 0
min = 0


# 예/ (1, 2, 3)

# a가 제일 작은 경우
if a < b:
    if a < c :
        min = a
        
        if b < c :
            max = c
            mid = b
        else:
            max = b
            mid = c
    pass

# b가 제일 작은 경우
if b < a:
    if b < c :
        min = b
        
        if a < c :
            max = c
            mid = a
        else:
            max = a
            mid = c
    pass


# c가 제일 작은 경우
if c < a:
    if c < b :
        min = c
        
        if a < b :
            max = b
            mid = a
        else:
            max = a
            mid = b
    pass

        
print(f"입력된 정수는 {min}, {mid}, {max}")
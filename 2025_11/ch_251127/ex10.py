
num1 = int(input("첫번째 정수: ")) # 3
num2 = int(input("두번째 정수: ")) # 2
num3 = int(input("세번째 정수: ")) # 1

n_min = n_mid = n_max = 0

if num1 < num2:
    if num2 < num3:
        n_max = num3
        n_mid = num2
        n_min = num1
    else:
        n_max = num2
        n_min = num1
        n_mid = num3
elif num1 < num3:
    n_max = num3
    n_min = num2
    n_mid = num1
else:
    n_max = num1
    
    if num2 < num3:
        n_mid = num3
        n_min = num2
    else:
        n_mid = num2
        n_min = num3
        
print(f"큰수: {n_max},  중간수: {n_mid}, 작은수: {n_min}")
'''
1. 성명, 이메일, 전화번호
2.
3. 끝
'''


print(":" * 12, "개인 정보 입력",  ":" * 12)

# 입력
name = input("- 이름 입력: ")
email = input("- 이메일 입력: ")
phone = input("- 전화번호 입력: ")

print('=' * 40)

# 출력
# 1. 더하기 연결
print(name + " | " + email + " | " + phone, end=' /더한기 연결\n\n')

# 2. 콤마로 구분해서 출력
print(name, email, phone, sep=" | ", end = " /콤마 구분\n\n")

# 3. f-String
print(f"{name} | {email} | {phone}", end=" /f-string\n\n")

# 4. format() 함수
print("{0} | {1} | {2}".format(name, email, phone), end=" /format 함수\n\n")

# 5. % 변환 문자
print("%s | %s | %s" %(name, email, phone), end=" /%변환\n\n")
print("%10s | %15s | %s" %(name, email, phone), end=" /%변환-공간확보\n\n")

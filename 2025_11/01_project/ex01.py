
# Tip!
# 낙타봉 표기법 => currAge (자바, C 권장)
# 뱀 표기법 => curr_age (python 권장)

# Q. 도전문제 1
# 이름, 현재 나이, 현재 년도를 입력 받는다.
# 본인의 나이가 65세가 되는 해의 년도를 출력한다.

name = input("이름? ")
curr_age = input("현재 나이? ")
curr_year = input('올해 연도? ')

count = 65 - int(curr_age)
next_year = int(curr_year) + count

print(f"'{name}'님은 '{next_year}년'에 65세가 됩니다. 연금 실행!")

# Q. 도전문제 2
# 평을 입력 받아서 제곱미터를 환산하는 프로그램
# 제곱미터를 입력 받아서 평으로 환산하는 프로그램
# 힌트1: 문자열을 숫자로 형변환
# 힌트2: 평→㎡: 평×3.305785 / ㎡→평: ㎡×0.3025 

# 평→㎡: 평×3.305785
p = float(input("평수를 입력하세요: "))
s = p * 3.305785
print(f"{p} 평수는 {s:5.2f}㎡ 입니다.")

# ㎡→평: ㎡×0.3025 
s = float(input("㎡를 입력하세요: "))
p = s * 0.3025
print(f"{s}㎡는 {p:.3f} 평 입니다.")





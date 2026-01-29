print("-" * 25, "ex01.py", "-" * 25)

# 점수 입력 받기 (실수로 형변환)
score = float(input("점수 입력: "))
print(f"입력 받은 점수는 {score}점 입니다.")

while score < 0 or score > 100:
    print(f"점수는 0~100점 까지만 입력 할 수 있습니디.")
    score = float(input("점수 디시 입력: "))
    print(f"입력 받은 점수는 {score}점 입니다.")

# if ~ elif를 사용해서 점수를 학점으로 환산
grade = "F"
if score >=90 and score <= 100 :
    grade = 'A'
elif score >= 80 :
    grade = 'B' 
elif score >= 70 :
    grade = 'C'
elif score >= 60 :
    grade = 'D'
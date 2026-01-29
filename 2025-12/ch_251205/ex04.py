f = open("data.txt", "w", encoding='utf-8')
f.write("1, user01, 010-3304-1514\n")
f.write("2, user02, 010-2304-2514\n")
f.write("3, user03, 010-1304-3514\n")
f.close()

with open ("data.txt", "r", encoding="utf8") as f:
    text = f.read()
    print(text)

    


    # 반복문을 활용한 파일 쓰기
f = open("data.txt", 'w')
for i in range(1, 5):
    f.write(f"{i}번째 줄입니다.\n")
f.close()

# 리스트의 요소를 파일로 쓰기
lines = ["Hello, ", "Phthon", "고마워요."]
with open("data.txt", "w", encoding="utf8") as f:
    f.writelines(lines)
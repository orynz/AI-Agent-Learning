person1 = {"no":1, "name":"홍길동", "phone":"010-1111-1111" }

print(person1["name"]) # 홍길동
person1["name"] = "일지매"
print(person1)

# 새로운 아이템 추가 (그냥 키를 사용)
person1["address"] = "서울시 종로구 견지동"
print(person1)

del person1["address"]
print(person1)

no = int(input("번호: "))
name = input("성명: ")
phone = input("전화번호: ")
person2 = {
    "no": no,
    "name": name,
    "phone": phone
}

print(person2)
# CRUD : 생성, 검색, 갱신, 삭제
# 입력, 출력, 검색, 수정, 삭제

p_list = [
    {"no": 1, "name": "hong", "phone": "010-1234-5689"},
    {"no": 2, "name": "kim", "phone": "010-2341-2947"},
    {"no": 3, "name": "lee", "phone": "010-9586-4957"},
    {"no": 4, "name": "kim", "phone": "010-8637-3856"},
    {"no": 5, "name": "park", "phone": "010-1038-9474"},
    {"no": 6, "name": "lee", "phone": "010-9575-3865"}
]

seq = len(p_list)



while True:
    print("========== 1>입력 2>출력, 3>검색, 4>수정, 5>삭제, 6>종료 ==========")
    no = input("메뉴 선택: ")
    
    if no == '6':
        break
    
    if no == '1':
        print("------ 입력기능 ------")
        name = input("이름: ")
        phone = input("전화번호: ")
        new_person = {
            "no": seq + 1,
            "name": name,
            "phone": phone 
        }
        
        p_list.append(new_person)
        seq += 1
        
        # 전체 출력
        print(f'{"번호":3} | {"이름":12} | {"전화번호":12}')
        for p in p_list:
            print(f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}')
    elif no == '2':
        print("------ 출력기능 ------")
        # 전체 출력
        print(f'{"번호":3} | {"이름":12} | {"전화번호":12}')
        for p in p_list:
            print(f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}')
    elif no == '3':
        print("------ 검색기능 ------")
        name = input("이름: ")
        text = ""
        for p in p_list:
            if name in p["name"]:
                text += f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}\n'
        
        if text == "":
            text = f"'{name}' - 검색 결과가 없습니다."
        
        print(text)
    elif no == '4':
        print("------ 수정기능 ------")
        # 전체 출력
        print(f'{"번호":3} | {"이름":12} | {"전화번호":12}')
        for p in p_list:
            print(f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}')
            
        text = ""
        no = input("수정할 번호: ")
        idx = 0
        
        if not no.isdigit():
            print("번호만 입력하세요.")
            continue
        
        while idx < len(p_list):
            if int(no) == p_list[idx]['no']:
                text += f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}'
                break
            idx += 1
                
        if text != "":
            print(text)
            p_list[idx]['name'] = input("수정할 이름: ")
            p_list[idx]['phone'] = input("수정할 전화번호: ")
            for p in p_list:
                print(f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}')
        else:
            print("입력한 번호가 없습니다.")
            
    elif no == '5':
        print("------ 삭제기능 ------")
        # 전체 출력
        print(f'{"번호":3} | {"이름":12} | {"전화번호":12}')
        for p in p_list:
            print(f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}')
            
        text = ""
        no = int(input("삭제할 no: "))

        idx = 0
        while idx < len(p_list):
            if no == p_list[idx]['no']:
                del p_list[idx]
                break
            idx += 1
                
        # 전체 출력
        print(f'{"번호":3} | {"이름":12} | {"전화번호":12}')
        for p in p_list:
            print(f'{p["no"]:5} | {p["name"]:14} | {p["phone"]:15}')
    else:
        print("다시 입력하세요. (1~6번)")


    
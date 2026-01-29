
from typing import List, Dict

p_list: List[Dict] = [
    {"no": 1, "name": "user01", "phone":"010-1111-1111"},
    {"no": 2, "name": "user02", "phone":"010-1111-2222"},
    {"no": 3, "name": "user03", "phone":"010-1111-3333"}
]
print(p_list)

next_no  = len(p_list) + 1

def menu():
    print("*" * 60)
    print("1)Input   2)Output   3)Search   4)Modify   5)Delete   6)End".center(6, "-"))
    print("*" * 60)
    no = input("메뉴 선택: ")
    
    # 유효성 검사
    while True:
        if not no.isdigit() or int(no) < 1 or int(no) > 6:
            print("Erro : 1 ~ 6 번호만 입력하세요.")
            no = input("다시 선택: ")
        else:
            return int(no)


def inputFn():
    global next_no
    
    print("1 )Input".center(60, "-"))
    name = input("이름: ")
    phone = input("전화번호: ")
    p_list.append({'no': next_no,
                   'name': name,
                   'phone': phone
    })
                  
    next_no += 1

def outputFn():    
    print(f"NO. | {"Name"} | {"Phone"}")
    for idx, p in enumerate(p_list):
        print(f"{idx+1} | {p['name']} | {p['phone']}")

def serchFn():
    print("3) Search".center(60, "-"))
    new_p_list = []
    name = input("검색할 이름: ")
    idxs = [i for i, e in enumerate(p_list) if e['name'] == name]
    if len(idxs) > 0:
        for i in range(0, len(idxs)):
            print(p_list[idxs[i]])
    else:
        print('검색된 데이터가 없습니다.')

def modifyFn():
    outputFn()
    print("4) Modify".center(60, "-"))
    idx = int(input("수정할 idx 번호 입력: ")) - 1
    if idx < len(p_list):    
        p_list[idx]["name"] = input("이름: ")
        p_list[idx]["phone"] = input("전화번호: ")
        print("--- 수정 완료 ---")

def deleteFn():
    outputFn()
    print("5) Delete".center(60, "-"))
    idx = int(input("삭제할 idx 번호 입력: ")) - 1
    if idx < len(p_list):  
        del p_list[idx]
        print("--- 삭제 완료 ---")

def run():
    while True:
        no = menu()
        if no == 1:
            inputFn()
        elif no == 2:
            print("2) Output".center(60, "-"))
            outputFn()
        elif no == 3:
            serchFn()
        elif no == 4:
            modifyFn()
        elif no == 5:
            deleteFn()
        elif no == 6:
            print("Program End,".center(60, '='))
            break

def main():
    print("*" * 60)
    print("Book".center(60))
    print("*" * 60)
    
    run()

if __name__ == "__main__":
    main()
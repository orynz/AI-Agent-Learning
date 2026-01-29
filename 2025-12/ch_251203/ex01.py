import os

# 리스트(p_list)에 딕셔너리 형태로 사용자의 정보(no, name, age, mobile, job)가 담긴 임시 데이터를 세팅
p_list = [
    {
        'no': 1,
        'name': '홍길동',
        'age': 25,
        'mobile': '010-1234-5678',
        'job': '프로그래머'
    },
    {
        'no': 2,
        'name': '박정자',
        'age': 28,
        'mobile': '010-1234-5678',
        'job': '학원강사'
    },
    {
        'no': 3,
        'name': '이영희',
        'age': 22,
        'mobile': '010-1234-5678',
        'job': '축구선수'
    }
]


print(":"*30, " Phone Book ", ":"*30)

'''
1. 선택 메뉴 만들기
2. 제어문을 이용해서 선택 번호의 기능 분기
3. 반복되도록 코드 작성
'''

menus = [
    '전체보기',
    '검색',
    '수정',
    '추가',
    '삭제',
    '종료'
]

ALL = 1
SEARCH = 2
MODIFY = 3
ADD = 4
DELETE = 5
END = 6

search_menus = [
    '이름검색',
    '번호검색',
    '직업검색',
    '취소'
]

SEARCH_NAME = 1
SEARCH_MOBILE = 2
SEARCH_JOB = 3
SEARCH_CANCEL = 4

next_idx = len(p_list) + 1

# 메뉴틀 출력하는 함수
def menuFn(menu):
    # os.system("cls")
    print(":"*30, " Phone Book ", ":"*30)
    print(" | ".join(menu))
    no = input(f"* 메뉴 선택(1 ~ {len(menu)}번) : ")
    return int(no) if no.isdigit() and 1 <= int(no) <= len(menu) else menuFn(menu)

def viewFn():
    print("--- 전체보기 기능 실행 ---")
    msg = f"{'idx':3} | {'이름':9} | {'나이':2} | {'전화번호':11} | {'직업':20}\n"
    for idx, p in enumerate(p_list):
        msg += f"{idx+1:3} | {p['name']:8} | {p['age']:4} | {p['mobile']:15} | {p['job']:20}\n"
    print(msg)

def searchFn():
    print("--- 검색 기능 실행 ---")
    menuFn(search_menus)

def modifyFn():
    print("--- 수정 기능 실행 ---")
    viewFn()
    idx = int(input("수정할 idx 번호 입력: ")) - 1
    if idx < len(p_list):    
        p_list[idx]["name"] = input("이름: ")
        p_list[idx]["age"] = input("나이: ")
        p_list[idx]["mobile"] = input("전화번호: ")
        p_list[idx]["job"] = input("직업: ")
        print("--- 수정 완료 ---")

def addFn():
    print("--- 추가 기능 실행 ---")
    
    global next_idx
    
    name = input("이름: ")
    age = input("나이: ")
    mobile = input("전화번호: ")
    job = input("직업 ")
    new_p = {"no":next_idx, "name": name, "age": age, "mobile": mobile, "job": job}
    p_list.append(new_p)
    next_idx += 1

def deleteFn():
    print("--- 삭제 기능 실행 ---")
    viewFn()
    idx = int(input("삭제할 idx 번호 입력: ")) - 1
    if idx < len(p_list):  
        del p_list[idx]
        print("--- 삭제 완료 ---")


def run(no):
    if no == ALL:
        viewFn()
    elif no == SEARCH:
        searchFn()
    elif no == MODIFY:
        modifyFn()
    elif no == ADD:
        addFn()
    elif no == DELETE:
        deleteFn()


menu = [f"{i+1}. {menu}" for i, menu in enumerate(menus)] 
while True:
    no = menuFn(menu)
    if no == END:
        print("감사합니다 ^^")
        break
    run(no)

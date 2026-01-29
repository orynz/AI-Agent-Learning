print(":"*25, end=" ")
print("Phone Book ", end="")
print(":"*25)

'''
1. 선택 메뉴 만들기
2. 제어문을 이용해서 선택 번호의 기능 분기
3. 반복 되도록 한다.
'''

def menuFn() :
    menuItems = ["INPUT","OUTPUT","SEARCH","MODIFY","DELETE","END"]
    for i, item in enumerate(menuItems) :
        print(i+1,".",item, sep="", end="  ")
    no = int(input("\nChoice:") )
    # 입력 범위 체크
    while no < 1 or no > len( menuItems) :
        print("메뉴에 없는 번호가 선택되었습니다. ")
        no = int(input("다시 입력:") )
        
    # 함수 실행 후 결과를 돌려준다.
    return no

def inputFn():
    print("--- 입력 기능 실행 ---")
    
def outputFn():
    print("--- 출력 기능 실행 ---")
    
def searchFn():
    print("--- 검색 기능 실행 ---")
    
def modifyFn():
    print("--- 수정 기능 실행 ---")
    
def deleteFn():
    print("--- 삭제 기능 실행 ---")
    
def endFn():
    print("--- 종료 기능 실행 ---")

# 함수 내부의 no 변수 접근 불가능.
# 함수는 선언부, 호출부가 있다. 호출 하지 않으면 함수 실행 안한다.
def run(no):
    if no == 1:
        inputFn()
    elif no == 2:
        outputFn()
    elif no == 3:
        searchFn()
    elif no == 4:
        modifyFn()
    elif no == 5:
        deleteFn()

while True:
    no = menuFn()
    if(no == 6) : 
        print("감사합니다!")
        break
    
    run(no)
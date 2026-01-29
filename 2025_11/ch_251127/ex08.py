'''
# 수열문제 (과제1)
# 1+2+3+4+5+6+7+8+9+10=55
'''
hang = 10 # 항의 갯수
cnt = 1 # 반복 횟수
total = 0 # 합
text = '' # 결과값 출력

while cnt <= hang:
    text += f"{cnt}+" if cnt < hang else f"{cnt}="
    total += cnt
    cnt += 1
    pass

print(f"{text}", total , sep = " ") 


'''
# 수열문제 (과제2)
# 1-2+3-4+5-6+7-8+9-10=-5
'''
# hang = 10 # 항의 갯수
# cnt = 1 # 반복 횟수
# total = 0 # 합
# text = '' # 결과값 출력

# while cnt <= 10:
#     if cnt % 2 == 0:
#         text += f"{cnt}+"if cnt < 10 else f"{cnt}="
#         total -= cnt
#     else:
#         text += f"{cnt}-"if cnt < 10 else f"{cnt}="
#         total += cnt
#     cnt += 1

# print(f"{text}", total , sep = " ") 

num = 2
total = 1;
print(1, end= ('+' if num < 10 else '=') )
while num <= 10:
    
    if num % 2 == 0:
        print(num, end= ('-' if num < 10 else '=') )
        total += num
    else:
        print(num, end= ('+' if num < 10 else '=') )
        total -= num
    num += 1

print(total)

# # 1+1+2+3+5+8+13 = ? (피보나치 수열) 7항
# hang = 10

# num = 1
# prev_num = 0
# next_num = 1
# total = 0

# while num <= hang:
#     print(next_num, end= (' + 'if num < hang else' = ') )
#     total += next_num
    
#     tmp = prev_num
#     prev_num = next_num
#     next_num = tmp + next_num
#     num += 1
    
# print(total)


# 1+1-2+3-5+8-13 = ? (피보나치 수열) 7항
# 1 2 3 4 5 6 7
# hang = 7

# num = 1
# prev_num = 0
# next_num = 1
# total = 0

# text = "1"
# while num <= hang:
#     if num < 2:
#         total += next_num
#         text += f"+{next_num}"
#     else:
#         if num % 2 == 0:
#             total += next_num
#             text += f"+{next_num}"
#         else:
#             total -= next_num
#             text += f"-{next_num}"

#     tmp = prev_num
#     prev_num = next_num
#     next_num = tmp + next_num
    
    
#     num += 1
    
# print(text + f"={total}")


'''
# 1-2+3-4+5-6+7-8+9-10=-5
1. 변수 선언
2. while 문을 이용해서 변수 증가하기
3. total에 누적 (빼고 더하고를 교차되도록)
4. 부호등을 꾸며보기 (sep, end 사용)
5. 삼항연자로 바꿔보기
'''
# num = 1
# total = 0
# while num <= 10:
    
#     if num % 2 == 0:
        
#         if num < 10:
#             print(num, end="+")
#         else:
#             print(num, end="=")
#         total -= num
#     else :
#         if num < 10:
#             print(num, end="-")
#         else:
#             print(num, end="=")
#         total += num
#     num += 1 # 증감식은 한번만
    
# print(total)
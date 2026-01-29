# 파이썬 list 자료구조
li = [10, 20, 30, 60, 40, 50]

# print(li)
# print(li[0])
# print(li[1])
# print(li[2])
# print(li[3])
# print(li[4])
# print(f"리스트 길이: {len(li)}")

# # 리스트에 30 이 있나?
# if 30 in li:
#     print("yes!")

# 오름차순 정렬
# 작은 수를 오른쪽으로 이동

for i in range(len(li)):    
    for j in range(len(li)):
        
        if li[j] < li[i]:            
            tmp = li[i]
            li[i] = li[j]
            li[j] = tmp
    print(li)   
print(li)

# # 내림차순 정렬
# for i in range(len(li)):    
#     for j in range(len(li)):
        
#         if li[j] > li[i]:            
#             tmp = li[i]
#             li[i] = li[j]
#             li[j] = tmp
            
# print(li)



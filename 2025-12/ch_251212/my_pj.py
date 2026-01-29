from openai import OpenAI

client = OpenAI()

def main():
    print("OpenAI 테스트")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        
        messages=[
            {"role": "user", "content": ""}
        ]
        
    )

def cal(x: int):
    helth = x
    
    def heal(h : int):
        nonlocal helth
        helth += h
        return helth
        
    return heal

n = 100
c = cal(n)
print(c(10))



    
        
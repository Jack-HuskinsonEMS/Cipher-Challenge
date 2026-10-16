import re

def IC(text):
    texts=re.sub(r'[^A-Z]','',text)
    summ=0
    for i in range(0,26):
        Ni=(texts.count(chr(i+65)))
        summ+=Ni*(Ni-1)
    N=len(texts)
    return summ/(N*(N-1))
print(IC(input()))   


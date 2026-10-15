import re

def IC(text):
    text=re.sub(r'[^\w\s]','',s)
    summ=0
    for i in range(0,25):
        Ni=(text.count(chr(i+65)))
        summ+=Ni*(Ni-1)
    N=len(text)
    return summ/(N*(N-1))
    


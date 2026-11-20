import re

KEYLEN=int(input("KeyLen: "))
text=str(input("Cipher Text: ")).upper()
text=re.sub(r'[^A-Z]','',text)
key=["A"]*KEYLEN

def convert(key,text):
    Solv=""
    i=0
    for j in text:
        if i==KEYLEN:
            i=0
        Solv+=chr((((ord(j)-65)-(ord(key[i])-65))%26)+65)
        i+=1
    return(Solv)

import math
import random


cipher=text
cipher=re.sub(r'[^A-Z]','',cipher)
QuadCount={}
Total=0

with open("english_quadgrams.txt") as file:
    for line in file:
        parts=line.strip().split()
        QuadCount[parts[0]]=parts[1]
        Total+=int(parts[1])

QuadProbs={}
for Quads,Count in QuadCount.items():
    QuadProbs[Quads]=math.log10(int(Count)/Total)


Default=math.log10(0.1/Total)
def NgramAnalysis(cipher,QuadProbs):
    TotalScore=0
    Evaled=0
    for i in range(len(cipher)-3):
        if cipher[i:i+4] in QuadProbs:
            TotalScore+=QuadProbs[cipher[i:i+4]]
        else:
            TotalScore+=Default
        Evaled+=1
    return TotalScore/Evaled
Ngram=NgramAnalysis(cipher,QuadProbs)
Mappings=[]
Mapping={}
for i in range(KEYLEN):
    Mappings.append({chr(j+65): chr(j+65) for j in range(26)})

def Map(cipher,Mappings,KEYLEN):
    Solv=""
    for i in range(len(cipher)):
        Solv+=Mappings[i%KEYLEN][cipher[i]]
    return Solv
testCipher=""
tempCipher=""

for i in cipher:
        tempCipher+=i
        testCipher+=i
failed=0
N=50000
T=2
accepts=0
for i in range(N):
    Row=random.randint(0,KEYLEN-1)
    pos1=random.randint(0,25)
    pos2=pos1
    while pos1==pos2:
        pos2=random.randint(0,25)
    pos1=chr(pos1+65)
    pos2=chr(pos2+65)
    Mappings[Row][pos1],Mappings[Row][pos2]=Mappings[Row][pos2],Mappings[Row][pos1]
    testCipher=Map(cipher,Mappings,KEYLEN)
    diff=NgramAnalysis(testCipher,QuadProbs)-Ngram
    if diff>0:
        tempCipher=testCipher
        bestMappings = [row.copy() for row in Mappings]
        accepts+=1
    elif 10 ** (diff/T)>random.random():
        tempCipher=testCipher
        bestMappings = [row.copy() for row in Mappings]
        accepts+=1
    else:
        failed+=1
        Mappings[Row][pos2],Mappings[Row][pos1]=Mappings[Row][pos1],Mappings[Row][pos2]
        
    Ngram=NgramAnalysis(tempCipher,QuadProbs)
    T=max(0.0001,T*0.9998)
    if i%1000==0:
        print(i,Ngram,accepts/1000)
        accepts=0

print(tempCipher,Ngram)#,bestMappings)
print(len(tempCipher),len(cipher))
print(cipher)


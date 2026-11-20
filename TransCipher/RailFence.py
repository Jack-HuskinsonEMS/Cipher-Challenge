import math
import random
import re
import itertools

cipher=input("Cipher Text: ").upper()
cleanCipher=re.sub(r'[^A-Z]', '', cipher.upper())
cipher=re.sub(r'[^A-Z]', '', cipher.upper())
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

print(list(QuadProbs.items())[:3])
Default=math.log10(0.1/Total)
print(f"Default={Default}")
def NgramAnalysis(cipher,QuadProbs):
    cleanText = cipher
    TotalScore=0
    Evaled=0
    for i in range(len(cleanText)-3):
        if cleanText[i:i+4] in QuadProbs:
            TotalScore+=QuadProbs[cleanText[i:i+4]]
        else:
            TotalScore+=Default
        Evaled+=1
    try:
        return TotalScore/Evaled
    except:
        return TotalScore

bestScore=-100
bestSolv=""
bestRAIL=0
for r in range(2,100):
    RAILS=r
    Rails=[0]*RAILS
    for i in range(len(cleanCipher)):
        rail=0
        p=i%(2*RAILS-2)
        if p <RAILS:
            rail=p
        else:
            rail=(2*RAILS-2)-p
        Rails[rail]+=1
    Railed=[""]*RAILS
    offset = 0
    for i in range(RAILS):
        for j in range(Rails[i]):
            Railed[i] += cleanCipher[j + offset]
        offset += Rails[i]

    dir=1
    rail=0
    Solv=""
    pointers=[0]*RAILS
    curScore=0
    for i in range(len(cleanCipher)):
        Solv += Railed[rail][pointers[rail]]
        pointers[rail] += 1
        rail+=dir
        if rail==RAILS-1 or rail==0:
            dir*=-1
    curScore=NgramAnalysis(Solv,QuadProbs)
    if curScore>bestScore:
        bestScore=curScore
        bestSolv=Solv
        bestRAIL=r
    print(r)
print(bestSolv,bestScore,bestRAIL)
    

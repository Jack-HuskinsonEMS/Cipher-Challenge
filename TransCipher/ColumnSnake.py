import math
import random
import re
import itertools

dir=int(input("Dir 1 | 0 : "))
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
bestWIDTH=0

for i in range(1,100):
    Cols=["" for _ in range(i)]
    for j in range(i):
        for k in range(len(cleanCipher)):
            if k%i==j:
                Cols[j]+=(cleanCipher[k])
    Solv=""
    for j in range(len(Cols)):
        Solv+=Cols[j][::(1-2*((j%2+dir)%2))]
    curScore=NgramAnalysis(Solv,QuadProbs)
    if curScore>bestScore:
        bestScore=curScore
        bestSolv=Solv
        bestWIDTH=i
print(bestSolv,bestScore,bestWIDTH)
import math
import random
import re
import itertools

cipher=input("Cipher Text: ").upper()
cleanCipher=re.sub(r'[^A-Z]', '', cipher.upper())
cipher=cipher.split()
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
def NgramAnalysis(cleanCipher,QuadProbs):
    cleanText = cleanCipher
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

def Map(Mapping,WIDTH,cipher):
    Cols=[]
    Mapped=""
    Reordered=[]
    baseRows=len(cipher)//WIDTH
    numLongCols=len(cipher)%WIDTH
    start=0
    inverse = [0]*WIDTH
    for i, pos in enumerate(Mapping):
        inverse[pos] = i
    for i in range(WIDTH):
        currentHeight=baseRows
        if inverse[i] < numLongCols:
            currentHeight += 1
        Col=cipher[start:start+currentHeight]
        start+=currentHeight
        Cols.append(Col)
    for i in Mapping:
        Reordered.append(Cols[i])
    for i in range(baseRows+1):
        for j in range(WIDTH):
            if len(Reordered[j])>i:
                Mapped+=Reordered[j][i]
    return Mapped
TEST=[]
Solvs=[]
for i,j,k,h,a, in itertools.permutations(range(5),5):
    Solv=""
    Mapping=[i,j,k,h,a]
    for _ in cipher:
        Solv+=Map(Mapping,5,_)
    TEST.append(NgramAnalysis(Solv,QuadProbs))
    Solvs.append(Solv)
MaxVal=-100
MaxIndex=-1
for i in range(0,120):
    if TEST[i]>MaxVal:
        MaxVal=TEST[i]
        MaxIndex=i
print(Solvs[MaxIndex],MaxVal)

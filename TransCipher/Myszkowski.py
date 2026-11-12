import re
import itertools
import math

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

for c in range(3,10):
    Cols=[[] for _ in range(c)]
    print(Cols)
    for i in range(len(cleanCipher)):
        Cols[i%c].append(cleanCipher[i])
    ordered=[[] for _ in range(c)]

    TEST=[]
    Solvs=[]
    perms=[]
    for i in itertools.permutations(range(c),c):
        ordered=[[] for _ in range(c)]
        for j in range(len(i)):
            ordered[j]=(Cols[int(i[j])])
        Solv=""
        for k in range(0,len(Cols[0])):
            for l in range(c):
               if k<len(ordered[l]):
                Solv+=ordered[l][k]
        TEST.append(NgramAnalysis(Solv,QuadProbs))
        Solvs.append(Solv)
        perms.append(i)
    MaxVal=-100
    MaxIndex=-1
    for i in range(len(TEST)):
        if TEST[i]>MaxVal:
            MaxVal=TEST[i]
            MaxIndex=i
    print(Solvs[MaxIndex],MaxVal,perms[MaxIndex])



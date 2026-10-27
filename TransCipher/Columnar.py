import math
import random
import re


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

WIDTHS=[]
number=len(cleanCipher)
for i in range(2,int((number//40))):
        WIDTHS.append(i)
print(WIDTHS)





Ngram=NgramAnalysis(cipher,QuadProbs)

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


testCipher=""
tempCipher=""

workingScore = NgramAnalysis(tempCipher, QuadProbs)
globalBestScore = workingScore
globalBestCipher = tempCipher
overallBestScore = float("-inf")
overallBestCipher = None
overallBestMapping = None
for j in WIDTHS:
    for k in range(0,1):
        ROWS=len(cleanCipher)//j
        Mapping=list(range(j))
        tempCipher = Map(Mapping, j, cleanCipher)
        workingScore = NgramAnalysis(tempCipher, QuadProbs)
        if k==0:
            print(f"LEN={len(Mapping)}")
        temp = 0.15
        failed=0
        accepts=0
        globalBestScore = workingScore
        globalBestCipher = tempCipher
        globalBestMapping = Mapping[:]
        for i in range(5000):
            pos1, pos2 = random.sample(range(j), 2)
            Mapping[pos1],Mapping[pos2]=Mapping[pos2],Mapping[pos1]
            testCipher=Map(Mapping,j,cleanCipher)
            currentScore = NgramAnalysis(testCipher, QuadProbs)
            diff=currentScore-workingScore
            #if i>4900:
                #print(i,currentScore,pos1,pos2,tempCipher[:15],temp)
                #print(diff)
            if diff > 0:
                workingScore = currentScore
                tempCipher = testCipher
                accepts+=1
                if currentScore > globalBestScore:
                    globalBestScore = currentScore
                    globalBestCipher = testCipher
                    globalBestMapping = Mapping[:]
                    failed=0
                else:
                    failed+=1
            elif 10 ** (diff / temp) > random.random():
                workingScore = currentScore 
                tempCipher = testCipher
                accepts+=1
            else:
                Mapping[pos2],Mapping[pos1]=Mapping[pos1],Mapping[pos2]
                failed+=1
                #if failed>=100:
                #    temp=min(0.015,temp+0.01)
                #    failed=0
            temp = max(0.001, temp * 0.9998)
        if globalBestScore > overallBestScore:
            overallBestScore = globalBestScore
            overallBestCipher = globalBestCipher
            overallBestMapping = globalBestMapping
        print(f"Loop {k}={globalBestScore}, Accept Rate={accepts/5000}")
print(overallBestCipher,overallBestScore,overallBestMapping)
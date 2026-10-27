import math
import random
import re


cipher=input("Cipher Text: ").upper()
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
    cleanText = re.sub(r'[^A-Z]', '', cipher.upper())
    TotalScore=0
    Evaled=0
    for i in range(len(cleanText)-3):
        if cleanText[i:i+4] in QuadProbs:
            TotalScore+=QuadProbs[cleanText[i:i+4]]
        else:
            TotalScore+=Default
        Evaled+=1
    return TotalScore/Evaled


def Freq(text):
    MonoFreqs={}
    for i in range(0,26):
        MonoFreqs.update({chr(i+65):text.count(chr(i+65))})
    return dict(sorted(MonoFreqs.items(), key=lambda item: item[1],reverse=True))

EngMonoFreq=["E", "T", "A", "O", "I", "N", "S", "H", "R", "D", "L", "C", "U", "M", "W", "F", "G", "Y", "P", "B", "V", "K", "J", "X", "Q", "Z"]

MonoFreqs=Freq(cipher)
Mapping={}
for i in range(0,26):
    Mapping[list(MonoFreqs)[i]]=EngMonoFreq[i]



Ngram=NgramAnalysis(cipher,QuadProbs)

def Map(cipher, Mapping):
    plain = ""
    for i in cipher:
        if 'A' <= i <= 'Z':
            plain += Mapping[i]
        else:
            plain += i 
    return plain
testCipher=""
tempCipher=""

print(f"LEN={len(Mapping)}")

for i in cipher:
        tempCipher+=i
        testCipher+=i
failed=0
workingScore = NgramAnalysis(tempCipher, QuadProbs)
globalBestScore = workingScore
globalBestCipher = tempCipher
temp = 0.02
for i in range(50000):
    pos1=random.randint(0,25)
    pos2=pos1
    while pos1==pos2:
        pos2=random.randint(0,25)
    pos1=chr(pos1+65)
    pos2=chr(pos2+65)
    Mapping[pos1],Mapping[pos2]=Mapping[pos2],Mapping[pos1]
    testCipher=Map(cipher,Mapping)
    currentScore = NgramAnalysis(testCipher, QuadProbs)
    diff=currentScore-workingScore
    if i%10000==0:
        print(i,currentScore,pos1,pos2,tempCipher[:15],temp)
    if diff > 0:
        workingScore = currentScore
        tempCipher = testCipher
        failed=0
        if currentScore > globalBestScore:
            globalBestScore = currentScore
            globalBestCipher = testCipher
    elif 10**(diff/temp) > random.random():
        workingScore = currentScore 
        tempCipher = testCipher
        failed=0
    else:
        failed+=1
        Mapping[pos2],Mapping[pos1]=Mapping[pos1],Mapping[pos2]
        #if failed>=10000:
            #temp+=3
            #print(i)
            #failed=0
    temp = max(0.001, temp * 0.9999)

print(globalBestCipher,globalBestScore)



    
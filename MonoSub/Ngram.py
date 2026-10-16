import math
import random
import re


cipher=input("Cipher Text: ")
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


Default=math.log10(0.01/Total)
def NgramAnalysis(cipher,QuadProbs):
    TotalScore=0
    Evaled=0
    for i in range(len(cipher)-4):
        if cipher[i:i+4] in QuadProbs:
            TotalScore+=QuadProbs[cipher[i:i+4]]
        else:
            TotalScore+=Default
        Evaled+=1
    return TotalScore/Evaled

EngMonoFreq=["E", "T", "A", "O", "I", "N", "S", "H", "R", "D", "L", "C", "U", "M", "W", "F", "G", "Y", "P", "B", "V", "K", "J", "X", "Q", "Z"]

def Freq(text):
    MonoFreqs={}
    for i in range(0,26):
        MonoFreqs.update({chr(i+65):text.count(chr(i+65))})
    return dict(sorted(MonoFreqs.items(), key=lambda item: item[1],reverse=True))

MonoFreqs=Freq(cipher)
Mapping={}
for i in range(0,26):
    Mapping[list(MonoFreqs)[i]]=EngMonoFreq[i]
print(Mapping)

Ngram=NgramAnalysis(cipher,QuadProbs)

def Map(cipher,Mapping):
    plain=""
    for i in cipher:
        plain+=Mapping[i]
    return plain
testCipher=""
tempCipher=""

for i in cipher:
        tempCipher+=i
        testCipher+=i

while Ngram<-4:
    failed=0
    pos1=random.randint(0,25)
    pos2=pos1
    while pos1==pos2:
        pos2=random.randint(0,25)
    pos1=chr(pos1+65)
    pos2=chr(pos2+65)
    Mapping[pos1],Mapping[pos2]=Mapping[pos2],Mapping[pos1]
    testCipher=Map(cipher,Mapping)
    if NgramAnalysis(testCipher,QuadProbs) > NgramAnalysis(tempCipher,QuadProbs):
        tempCipher=testCipher
    else:
        failed+=1
        Mapping[pos2],Mapping[pos1]=Mapping[pos1],Mapping[pos2]
        if failed>20:
            for i in range(0,10):
                pos1=random.randint(0,25)
                pos2=pos1
                while pos1==pos2:
                    pos2=random.randint(0,25)
                pos1=chr(pos1+65)
                pos2=chr(pos2+65)
                Mapping[pos1],Mapping[pos2]=Mapping[pos2],Mapping[pos1]
    Ngram=NgramAnalysis(tempCipher,QuadProbs)

print(tempCipher,Ngram)



    
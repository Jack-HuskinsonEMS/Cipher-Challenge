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
    clean_text = re.sub(r'[^A-Z]', '', cipher.upper())
    TotalScore=0
    Evaled=0
    for i in range(len(clean_text)-3):
        if clean_text[i:i+4] in QuadProbs:
            TotalScore+=QuadProbs[clean_text[i:i+4]]
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
working_score = NgramAnalysis(tempCipher, QuadProbs)
global_best_score = working_score
global_best_cipher = tempCipher
temp = 0.02
cooling_rate = 0.001
for i in range(50000):
    pos1=random.randint(0,25)
    pos2=pos1
    while pos1==pos2:
        pos2=random.randint(0,25)
    pos1=chr(pos1+65)
    pos2=chr(pos2+65)
    Mapping[pos1],Mapping[pos2]=Mapping[pos2],Mapping[pos1]
    testCipher=Map(cipher,Mapping)
    current_score = NgramAnalysis(testCipher, QuadProbs)
    diff=current_score-working_score
    Flag=True
    if i%10000==0:
        print(i,current_score,pos1,pos2,tempCipher[:15],temp)
    if diff<-700:
        Flag=False
    if diff > 0:
        working_score = current_score
        tempCipher = testCipher
        failed=0
        if current_score > global_best_score:
            global_best_score = current_score
            global_best_cipher = testCipher
    elif Flag and math.exp(diff / temp) > random.random():
        working_score = current_score 
        tempCipher = testCipher
        failed=0
    else:
        failed+=1
        Mapping[pos2],Mapping[pos1]=Mapping[pos1],Mapping[pos2]
        if failed>=10000:
            temp+=3
            print(i)
            failed=0
    temp = max(0.001, temp * 0.99999)

print(tempCipher,working_score,Mapping)



    
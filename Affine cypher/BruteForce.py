import re
from AD import Decrypt
from IC import IC

cipher=input("Enter cipher text: ")

def Convert(cipher,a,b):
    plain=""
    for i in cipher:
        plain+=chr(Decrypt(a,b,(ord(i)-65))+65)
    return plain

def BruteForce(cipher):
    validAKeys=[1,3,5,7,9,11,15,17,19,21,23,25]
    for i in validAKeys:
        for j in range(1,26):
            ExTexts=re.findall("Q[^U]|J[CFGJQSTVWXZ]|V[BFHJKMPTWX]",Convert(cipher,i,j))
            InTexts=re.findall("A",Convert(cipher,i,j))
            if len(ExTexts)==0 and len(InTexts)>0:
                print("\n")
                print(Convert(cipher,i,j),i,j)
            
BruteForce(cipher)

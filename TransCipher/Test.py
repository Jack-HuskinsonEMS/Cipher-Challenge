import re

cipher=input("Cipher Text: ").upper()
cleanCipher=re.sub(r'[^A-Z]', '', cipher.upper())

for i in range(len(cleanCipher)//48+2 ):
    print(cleanCipher[44*i:44*(i+1)])

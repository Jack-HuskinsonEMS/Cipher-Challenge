import sys
import os
import re

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from AffineCipher.IC import IC

text=str(input("Cipher Text: ")).upper()
text=re.sub(r'[^A-Z]','',text)

for j in range(1,100):
    Total=0
    for k in range(1,j+1):
        Test=""
        for i in range(k-1,len(text),j):
            Test+=text[i]
        Total+=IC(Test)
    print(f"Len: {j} = {Total/j}")
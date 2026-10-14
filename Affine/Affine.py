alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

cipherText = input("cipher text: ")

print("using ax+b")
a = int(input("a: "))
b = int(input("b: "))

decoded = ""

def inverse(a):
    i = a%26
    inverse = {
        1:1,
        3:9,
        5:21,
        7:15,
        9:3,
        11:19,
        15:7,
        17:23,
        19:11,
        21:5,
        23:17,
        25:25
    }
    #now just use a lookup table
    if i in inverse:
        return inverse[i]
    else:
        return -1

for letter in cipherText:
    i = alphabet.find(letter.upper())
    i -= b
    i *= inverse(a)
    i %= 26
    decoded += alphabet[int(i)]
    
print("decoded:")
print(decoded)
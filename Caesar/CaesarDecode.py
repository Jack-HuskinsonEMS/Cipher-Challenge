alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

cipherText = input("cipher text: ")

shift = int(input("shift factor"))

decoded = ""

for letter in cipherText:
    if alphabet.find(letter) != -1:
        i = alphabet.find(letter)
        i += shift
        i %= 26
        decoded += alphabet[i]

print("Decoded:")
print(decoded)
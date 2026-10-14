alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

cipherText = input("cipher text: ")

shift = 14

decoded = ""

for letter in cipherText:
    if alphabet.find(letter) != -1:
        i = alphabet.find(letter)
        if alphabet.find(letter)+shift > 25:
            i -= 26
        decoded += alphabet[i+shift]

print("Decoded:")
print(decoded)
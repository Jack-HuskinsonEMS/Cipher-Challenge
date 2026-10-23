from ModularMultiplicativeInverse import MMI

def Decrypt(a,b,C):
    mod=26
    A=MMI(a,mod)
    Calc=(A*(C-b))
    while Calc<0:
        Calc+=mod
    return Calc%mod

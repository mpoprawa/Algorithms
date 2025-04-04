def KSA(K):
    n = len(K)
    j = 0
    T = [K[i%n] for i in range(256)]
    S = list(range(256))
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S,m):
    i = 0
    j = 0
    KS=[None]*m
    for b in range(m):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        KS[b] = hex(S[(S[i] + S[j]) % 256])
    return KS

def xor(m1,m2):
    res = [None]*len(m1)
    for i in range(len(m1)):
        res[i] = hex(int(m1[i], 16) ^ int(m2[i], 16))
    return res

def encrypt(key,message):
    hex_message=[hex(ord(message[i])) for i in range(len(message))]
    s=KSA(key)
    key_stream=PRGA(s,len(hex_message))
    cipher=xor(hex_message,key_stream)
    return "".join(cipher)

def decrypt(key,cipher):
    s=KSA(key)
    key_stream=PRGA(s,len(cipher))
    cipher=cipher.split("0x")
    cipher.pop(0)
    hex_message=xor(cipher,key_stream)
    message=[chr(int(h,0)) for h in hex_message]
    return "".join(message)

key=[1]*256
message="test message"
cipher=encrypt(key,message)
received=decrypt(key,cipher)
print("message:",message)
print("cipher:",cipher)
print("received message:",received)
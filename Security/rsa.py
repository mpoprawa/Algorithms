from random import randint
import math

def isPrime(n):
    for i in range(2,int(math.sqrt(n)+1)):
        if n%i==0:
            return False
    return True

def inverse(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = inverse(b%a,a)
    return (g, x - (b//a) * y, y)

def power(x, y):
    res = 1
    while (y > 0):
        if ((y & 1) == 1) :
            res = res * x
        y = y >> 1
        x = x * x
    return res

def keyGen(p,q):
    if not isPrime(p) or not isPrime(q):
        print("numbers are not prime")
        return 0,0
    n=p*q
    f=(p-1)*(q-1)
    while True:
        e=randint(2,f-1)
        if math.gcd(e,f)==1:
            break
    d=inverse(e,f)[1]%f
    return (n,e),(n,d)

def factors(pubA,secA):
    n=pubA[0]
    e=pubA[1]
    d=secA[1]
    f=e*d-1
    t=f
    while t%2==0:
        t=int(t/2)
    a=2
    while True:
        k=t
        while k<f:
            x=power(a,k)%n
            if x!=1 and x!=n-1 and (x*x)%n==1:
                p=math.gcd(x-1,n)
                q=int(n/p)
                return p,q
            k*=2
        a+=2

def attack(pubB,p,q):
    n=pubB[0]
    e=pubB[1]
    f=(p-1)*(q-1)
    d=inverse(e,f)[1]%f
    return n,d

p=463
q=179
keysA=keyGen(p,q)
keysB=keyGen(p,q)
print("p =",p,"q =",q,"\nA =",keysA,"\nB =",keysB)
p1,q1=factors(keysA[0],keysA[1])
print("found p =",p1,"q =",q1)
secKey=attack(keysB[0],p1,q1)
print("sec key B =",secKey)
import sys
import numpy as np
import math

def sort(array, p, q):
    c=s=0
    if p < q: 
        lPivot, rPivot, c, s = partition(array, p, q) 
        c1,s1=sort(array, p, lPivot - 1) 
        c2,s2=sort(array, lPivot + 1, rPivot - 1) 
        c3,s3=sort(array, rPivot + 1, q)
        c+=c1+c2+c3
        s+=s1+s2+s3
        if len(array)<40:
            print(array)
    return c,s
        
def partition(array, p, q): 
    comp = 1
    swap = 0
    if array[p] > array[q]: 
        array[p], array[q] = array[q], array[p]
        swap+=1
    lLoc = k = p + 1
    rLoc, lp, rp = q - 1, array[p], array[q]
    s = l = 0
    
    while k <= rLoc:
        if s>=l:
            if array[k] < lp: 
                comp+1
                swap+=1
                s+=1
                array[k], array[lLoc] = array[lLoc], array[k] 
                lLoc += 1
            elif array[k] >= rp:
                l+=1
                comp+=4
                swap+=1
                while array[rLoc] > rp and k < rLoc:
                    comp+=1
                    rLoc -= 1
                array[k], array[rLoc] = array[rLoc], array[k] 
                rLoc -= 1
                if array[k] < lp:
                    swap+=1
                    array[k], array[lLoc] = array[lLoc], array[k] 
                    lLoc += 1
            else:
                comp+=2
        else:
            if array[k] >= rp:
                comp+=3
                swap+=1
                l+=1
                while array[rLoc] > rp and k < rLoc:
                    comp+=1
                    rLoc -= 1
                array[k], array[rLoc] = array[rLoc], array[k] 
                rLoc -= 1
                if array[k] < lp:
                    swap+=1 
                    array[k], array[lLoc] = array[lLoc], array[k] 
                    lLoc += 1
            elif array[k] < lp:
                comp+=2
                swap+=1 
                s+=1
                array[k], array[lLoc] = array[lLoc], array[k] 
                lLoc += 1
            else:
                comp+=2
        k += 1

    lLoc -= 1
    rLoc += 1
    swap+=2
    array[p], array[lLoc] = array[lLoc], array[p] 
    array[q], array[rLoc] = array[rLoc], array[q] 
    return lLoc, rLoc, comp, swap 

def check(array):
    for i in range(len(array)-1):
        if array[i]>array[i+1]:
            print("failure")
            return 1
    return 0

def test(mode):
    failures = 0
    num = 0
    comp = []
    swap = []
    array=[]

    for i in sys.stdin:
        if i == "|\n":
            n = len(array)-1
            if n+1<40:
                array2 = array.copy()
                print(array)
            c,s=sort(array,0,n)
            comp.append(c)
            swap.append(s)
            print(c,s)
            failures+=check(array)
            if n+1<40:
                print(array2)
                print(array)
            array=[]
            num+=1
        else:
            array.append(int(i))

    if mode==0:
        if num == 5:
            np.savetxt('dualC1.txt',comp,fmt='%d')
            np.savetxt('dualS1.txt',swap,fmt='%d')
        elif num == 50:
            np.savetxt('dualC10.txt',comp,fmt='%d')
            np.savetxt('dualS10.txt',swap,fmt='%d')
        elif num == 500:
            np.savetxt('dualC100.txt',comp,fmt='%d')
            np.savetxt('dualS100.txt',swap,fmt='%d')
    else:
        if num == 50:
            np.savetxt('dual2C1.txt',comp,fmt='%d')
            np.savetxt('dual2S1.txt',swap,fmt='%d')
        elif num == 500:
            np.savetxt('dual2C10.txt',comp,fmt='%d')
            np.savetxt('dual2S10.txt',swap,fmt='%d')
        elif num == 5000:
            np.savetxt('dual2C100.txt',comp,fmt='%d')
            np.savetxt('dual2S100.txt',swap,fmt='%d')
    print(failures,"failures")

#test(0)
test(1)
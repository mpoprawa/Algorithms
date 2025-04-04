import sys
import numpy as np

def insertionSort(array, p, n):
    c = 0
    s = 0
    for i in range(p + 1, n + 1):
        key = array[i]
        j = i
        c+=1
        while j>p and array[j-1]>key:
            array[j]= array[j-1]
            s+=1
            j-= 1
            c+=1
        array[j]= key
    return c,s

def partition(array, p, q): 
    pivot = array[p] 
    i = p - 1
    j = q + 1
    c=0
    s=0
  
    while (True): 
        i += 1
        c += 1
        while (array[i] < pivot): 
            i += 1
            c +=1
        j -= 1
        c += 1
        while (array[j] > pivot): 
            j -= 1
            c += 1 
        if (i >= j): 
            return j,c,s
        s +=1
        array[i], array[j] = array[j], array[i] 

def hybridSort(array, p, q, size):
    c1=c2=c3=c4=s1=s2=s3=s4=0
    if p<q:
        pivot,c,s = partition(array, p, q)
        if pivot-p>size:
            c1,s1=hybridSort(array, p, pivot, size)
        else:
            c2,s2=insertionSort(array, p, pivot)
        if q-pivot>size:
            c3,s3=hybridSort(array, pivot + 1, q, size)
        else:
            c4,c4=insertionSort(array, pivot + 1, q)
    c+=c1+c2+c3+c4
    s+=s1+s2+s3+s4
    return c,s

def check(array):
    for j in range(len(array)-1):
        if array[j]>array[j+1]:
            print("failure")
            return 1
    return 0

def test1():
    size = 11 #optymalne 11 c~=172 s~=45
    failures = 0
    array=[]
    for i in sys.stdin:
        if i == "|\n":
            n = len(array)-1
            if n+1<40:
                print(array)
                array2 = array.copy()
            print(hybridSort(array,0,n,size))
            failures+=check(array)
            if n+1<40:
                print(array2)
                print(array)
            array=[]
        else:
            array.append(int(i))
    print(failures,"failures")

def test2(mode):
    size = 1
    failures = 0
    num = 0
    comp = []
    swap = []
    array=[]
    
    for i in sys.stdin:
        if i == "|\n":
            n = len(array)-1
            if n+1<40:
                print(array)
                array2 = array.copy()
            c,s=hybridSort(array,0,n,size)
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
            np.savetxt('hybridC1.txt',comp,fmt='%d')
            np.savetxt('hybridS1.txt',swap,fmt='%d')
        elif num == 50:
            np.savetxt('hybridC10.txt',comp,fmt='%d')
            np.savetxt('hybridS10.txt',swap,fmt='%d')
        elif num == 500:
            np.savetxt('hybridC100.txt',comp,fmt='%d')
            np.savetxt('hybridS100.txt',swap,fmt='%d')
    else:
        if num == 50:
            np.savetxt('hybrid2C1.txt',comp,fmt='%d')
            np.savetxt('hybrid2S1.txt',swap,fmt='%d')
        elif num == 500:
            np.savetxt('hybrid2C10.txt',comp,fmt='%d')
            np.savetxt('hybrid2S10.txt',swap,fmt='%d')
        elif num == 5000:
            np.savetxt('hybrid2C100.txt',comp,fmt='%d')
            np.savetxt('hybrid2S100.txt',swap,fmt='%d')
    print(failures,"failures")

#test1()
#test2(0)
test2(1)
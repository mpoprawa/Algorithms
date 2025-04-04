import sys
import numpy as np
from random import randrange
import math

def partition(arr, l, r):
    c=s=0 
    x = arr[r] 
    pivot = l 
    for j in range(l, r):
        c+=1
        if arr[j] <= x:
            s+=1 
            arr[pivot], arr[j] = arr[j], arr[pivot] 
            pivot += 1
    s+=1
    arr[pivot], arr[r] = arr[r], arr[pivot] 
    return c,s,pivot

def select(arr, l, r, k):
    if len(arr)<=50:
        print(arr)
    if k > 0 and k <= r - l + 1:
        c,s,pivot = partition(arr, l, r) 
        if pivot - l == k - 1: 
            return arr[pivot],c,s
        elif pivot - l > k - 1: 
            res,c1,s1=select(arr, l, pivot - 1, k)
            c+=c1
            s+=s1
            return res,c,s
        else:
            res,c1,s1=select(arr, pivot + 1, r, k - pivot + l - 1)
            c+=c1
            s+=s1
            return res,c,s
    print("pivot out of bound")
    return -1,0,0 

def check(array,res,k):
    array.sort()
    if res==-1 or array[k-1]!=res:
        print("failure")
        return 1
    return 0

def test(mode):
    num = 0
    comp = []
    swap = []
    array = []
    failures = 0

    for i in sys.stdin:
        if i == "|\n":
            n=len(array)-1
            if mode==0:
                k=math.ceil(0.1*n)
            if mode==1:
                k=math.ceil(0.5*n)
            array2 = array.copy()
            res,c,s=(select(array,0,n,k))
            comp.append(c)
            swap.append(s)
            if len(array)<=50:
                print("start ",array2)
                print("end   ",array)
            array.sort()
            if len(array)<=50:
                print("sorted",array)
                print(str(k)+"-ta statystyka pozycyjna =",res)
            print("comp count =",c,"swap count =",s)
            failures+=check(array,res,k)
            array=[]
            num+=1
        else:
            array.append(int(i))

    if mode == 0:
        np.savetxt('selectRandc.txt',comp,fmt='%d')
        np.savetxt('selectRands.txt',swap,fmt='%d')
    elif mode == 1:
        np.savetxt('selectRandc1.txt',comp,fmt='%d')
        np.savetxt('selectRands1.txt',swap,fmt='%d')
    print(failures,"failures")

mode=int(sys.argv[1])
test(mode)
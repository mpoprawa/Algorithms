import sys
import numpy as np
import random
import math

def sort(arr):
    comp=0
    swap=0
    for j in range(1,len(arr)):
        key=arr[j]
        i=j-1
        comp+=1
        while (arr[i]>key):
            arr[i+1]=arr[i]
            i=i-1
            swap+=1
            if (i<0):
                break
            comp+=1
        arr[i+1]=key
    return comp,swap

def findMedian(arr, l, r):
    L = []
    for i in range(l, r):
        L.append(arr[i])
    c,s=sort(L)
    return L[(r-l)//2],c,s

def partition(arr, l, r, med):
    c=s=0
    for i in range(l, r+1):
        c+=1 
        if arr[i] == med:
            s+=1 
            arr[i], arr[r] = arr[r], arr[i]
            break

    i = l - 1
    for j in range(l, r):
        c+=1
        if arr[j] <= arr[r]:
            i += 1
            s+=1 
            arr[i], arr[j] = arr[j], arr[i]
    s+=1
    arr[i+1], arr[r] = arr[r], arr[i+1]
    return i+1,c,s
    
def select(arr, l, r, k, num):
    n = r - l + 1
    median = []
    i = 0
    c=s=0
    while i < n//num:
        m,c1,s1=findMedian(arr, l+num*i, l+num*i+num)
        median.append(m)
        c+=c1
        s+=s1
        i += 1
    if i*num < n:
        m,c1,s1=findMedian(arr, l+num*i, l+num*i+(n%num))
        median.append(m)
        c+=c1
        s+=s1
        i += 1
    if i == 1:
        medOfmed = median[i-1]
    else:
        medOfmed,c3,s3 = select(median, 0, i-1, i//2, num)
    pivot,c2,s2 = partition(arr, l, r, medOfmed)
    i = pivot - l + 1 
    if i == k:
        return arr[pivot],c,s
    elif i > k:
        res,c1,s1=select(arr, l, pivot-1, k, num)
        c+=c1+c2+c3
        s+=s1+s2+s3
        return res,c,s
    else:
        res,c1,s1=select(arr, pivot+1, r, k-i, num)
        c+=c1+c2+c3
        s+=s1+s2+s3
        return res,c,s
    
def check(array,res,k):
    array.sort()
    if res==-1 or array[k-1]!=res:
        print("failure")
        return 1
    return 0

def test(mode):
    comp = []
    swap = []
    array = []
    failures = 0
    num=5
    if mode==2:
        num=3
    elif mode==4:
        num=7
    elif mode==5:
        num=9

    for i in sys.stdin:
        if i == "|\n":
            n=len(array)-1
            if mode==0:
                k=math.ceil(0.1*n)
            else:
                k=math.ceil(0.5*n)
            array2 = array.copy()
            res,c,s=(select(array,0,n,k,num))
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
        else:
            array.append(int(i))

    if mode == 0:
        np.savetxt('selectc.txt',comp,fmt='%d')
        np.savetxt('selects.txt',swap,fmt='%d')
    elif mode == 1:
        np.savetxt('selectc1.txt',comp,fmt='%d')
        np.savetxt('selects1.txt',swap,fmt='%d')
    elif mode == 2:
        np.savetxt('selectc3.txt',comp,fmt='%d')
        np.savetxt('selects3.txt',swap,fmt='%d')
    elif mode == 3:
        np.savetxt('selectc5.txt',comp,fmt='%d')
        np.savetxt('selects5.txt',swap,fmt='%d')
    elif mode == 4:
        np.savetxt('selectc7.txt',comp,fmt='%d')
        np.savetxt('selects7.txt',swap,fmt='%d')
    elif mode == 5:
        np.savetxt('selectc9.txt',comp,fmt='%d')
        np.savetxt('selects9.txt',swap,fmt='%d')
    print(failures,"failures")

mode=int(sys.argv[1])
test(mode)
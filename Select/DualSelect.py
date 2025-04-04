import numpy as np
import sys
import math

def sort(arr):
    comp=0
    for j in range(1,len(arr)):
        key=arr[j]
        i=j-1
        comp+=1
        while (arr[i]>key):
            arr[i+1]=arr[i]
            i=i-1
            if (i<0):
                break
            comp+=1
        arr[i+1]=key
    return comp

def findMedians(arr, l, r):
    L = []
    for i in range(l, r):
        L.append(arr[i])
    c=sort(L)
    return L[(r-l)//3],L[2*(r-l)//3],c

def findMedian(arr, l, r):
    L = []
    for i in range(l, r):
        L.append(arr[i])
    c=sort(L)
    return L[(r-l)//2],c

def select(arr, l, r):
    n = r - l + 1
    median = []
    i = 0
    c=0
    while i < n//5:
        m,c1=findMedian(arr, l+5*i, l+5*i+5)
        median.append(m)
        c+=c1
        i += 1
    if i*5 < n:
        m,c1=findMedian(arr, l+5*i, l+5*i+(n%5))
        median.append(m)
        c+=c1
        i += 1
    if i == 1:
        medOfmed = median[i-1]
    else:
        medOfmed,c1 = select(median, 0, i-1)
        c+=c1
    return medOfmed,c
    
def dualSelect(arr, l, r):
    n = r - l + 1
    median1 = []
    median2 = []
    i = 0
    c=0
    while i < n//5:
        m1,m2,c1=findMedians(arr, l+5*i, l+5*i+5)
        median1.append(m1)
        median2.append(m2)
        c+=c1
        i += 1
    if i*5 < n:
        m1,m2,c1=findMedians(arr, l+5*i, l+5*i+(n%5))
        median1.append(m1)
        median2.append(m2)
        c+=c1
        i += 1
    if i == 1:
        med1 = median1[0]
        med2 = median2[0]
    else:
        med1,c1 = select(median1, 0, i-1)
        med2,c2 = select(median2, 0, i-1)
        c+=c1+c2
    return med1,med2,c

def DualSort(arr, l, r):
    if l >= r:
        return 0
    if len(arr)<40:
        print(arr)
    med1,med2,c = dualSelect(arr, l, r)
    pivot1,pivot2,c1 = dualPartition(arr, l, r, med1,med2)
    c2=DualSort(arr, l, pivot1-1)
    c3=DualSort(arr, pivot1+1, pivot2-1)
    c4=DualSort(arr, pivot2+1, r)
    c+=c1+c2+c3+c4
    return c

def dualPartition(arr, l, r, med1, med2):
    comp=0
    found=False
    for i in range(l, r):
        comp+=1 
        if arr[i] == med1:
            arr[i], arr[l] = arr[l], arr[i]
            if not found:
                found==True
            else:
                break
        elif arr[i] == med2:
            arr[i], arr[r] = arr[r], arr[i]
            if not found:
                found==True
            else:
                break

    lLoc = k = l + 1
    rLoc = r - 1
      
    while k <= rLoc: 
        if arr[k] < med1: 
            arr[k], arr[lLoc] = arr[lLoc], arr[k] 
            lLoc += 1
        elif arr[k] >= med2: 
            while arr[rLoc] > med2 and k < rLoc: 
                rLoc -= 1         
            arr[k], arr[rLoc] = arr[rLoc], arr[k] 
            rLoc -= 1
            if arr[k] < med1: 
                arr[k], arr[lLoc] = arr[lLoc], arr[k] 
                lLoc += 1            
        k += 1

    lLoc -= 1
    rLoc += 1
    arr[l], arr[lLoc] = arr[lLoc], arr[l] 
    arr[r], arr[rLoc] = arr[rLoc], arr[r]
    return lLoc,rLoc,comp

def check(array):
    for j in range(len(array)-1):
        if array[j]>array[j+1]:
            print("failure")
            return 1
    return 0

#const~=6
def test(mode):
    failures = 0
    num = 0
    comp = []
    #comp2 = []
    array=[]
    for i in sys.stdin:
        if i == "|\n":
            n = len(array)-1
            if n+1<40:
                print(array)
                array2 = array.copy()
            c=DualSort(array,0,n)
            comp.append(c)
            #comp2.append(c/(n*math.log(n)))
            print(c)
            failures+=check(array)
            if n+1<40:
                print("starting:",array2)
                print("sorted:",array)
            array=[]
            num+=1
        else:
            array.append(int(i))

    if mode==0:
            np.savetxt('dualSelect.txt',comp,fmt='%d')
    print(failures,"failures")
    #print("stala:",np.average(comp2))

sys.setrecursionlimit(1000000)
test(1)

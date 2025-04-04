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

def findMedian(arr, l, r):
    L = []
    for i in range(l, r):
        L.append(arr[i])
    c=sort(L)
    return L[(r-l)//2],c

def partition(arr, l, r, med):
    c=0
    for i in range(l, r+1):
        c+=1 
        if arr[i] == med:
            arr[i], arr[r] = arr[r], arr[i]
            break

    i = l - 1
    for j in range(l, r):
        c+=1
        if arr[j] <= arr[r]:
            i += 1 
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[r] = arr[r], arr[i+1]
    return i+1,c
    
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

def QuickSort(a, l, r):
    if l >= r:
        return 0
    if len(a)<40:
        print(a)
    med,c = select(a, l, r)
    q,c1 = partition(a, l, r, med)

    c2=QuickSort(a, l, q-1)
    c3=QuickSort(a, q+1, r)
    c+=c1+c2+c3
    return c

def check(array):
    for j in range(len(array)-1):
        if array[j]>array[j+1]:
            print("failure")
            return 1
    return 0

#const~=15
def test(mode):
    failures = 0
    num = 0
    comp = []
    #comp2=[]
    array=[]

    for i in sys.stdin:
        if i == "|\n":
            n = len(array)-1
            if n+1<40:
                print(array)
                array2 = array.copy()
            c=QuickSort(array,0,n)
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
            np.savetxt('quickSelect.txt',comp,fmt='%d')
    print(failures,"failures")
    #print("stala:",np.average(comp2))

sys.setrecursionlimit(1000000)
test(1)
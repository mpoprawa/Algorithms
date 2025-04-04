import sys
import numpy as np

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(node, key, depth):
    comp=0
    if key <= node.key:
        if node.left is None:
            node.left=Node(key)
            count=2
            d=depth+1
        else:
            comp,count,d=insert(node.left,key,depth+1)
            count+=1
    else:
        if node.right is None:
            node.right=Node(key)
            count=2
            d=depth+1
        else:
            comp,count,d=insert(node.right,key,depth+1)
            count+=1

    return comp+1,count,d

def inorder(root):
    if root:
        inorder(root.left)
        print(root.key, end=" ")
        inorder(root.right)

def minValue(node):
    count=2
    current = node
    while current and current.left is not None:
        current = current.left
        count+=1
    return current,count

def delete(root, key):
    if root is None:
        return root,0,0,False
    
    if key < root.key:
        root.left,comp,count,found = delete(root.left, key)
        count+=1
        comp+=1
    elif key > root.key:
        root.right,comp,count,found = delete(root.right, key)
        count+=1
        comp+=2
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp,0,2,True
        elif root.right is None:
            temp = root.left
            root = None
            return temp,0,3,True
        temp,count = minValue(root.right)
        root.key = temp.key
        root.right,comp,count1,found = delete(root.right, temp.key)
        comp+=2
        count+=3
        count+=count1
    return root,comp,count,found

def inorder(root):
    if root:
        inorder(root.left)
        print(root.key, end=" ")
        inorder(root.right)

def treeHeight(root):
    if root is None:
        return 0
    else:
        return 1+max(treeHeight(root.left),treeHeight(root.right))

def show(root):
    global left_trace
    global right_trace
    depth=treeHeight(root)
    left_trace=[None]*depth
    right_trace=[None]*depth
    print_BST(root,0,"-")

def print_BST(root, depth, prefix):
    if root == None:
        return
    if root.left != None:
        print_BST(root.left, depth+1, '/')
    if prefix == '/':
        left_trace[depth-1]='|'
    if prefix == '\\':
        right_trace[depth-1]=' '
    if depth==0:
        print("-",end="")
    if depth>0:
        print(" ",end="")
    for i in range(depth-1):
        if left_trace[i]== '|' or right_trace[i]=='|':
            print("| ",end="")
        else:
            print("  ",end="")
    if depth>0:
        print(prefix+"-",end="")
    print("["+str(root.key)+"]")
    left_trace[depth]=' '
    if root.right != None:
        right_trace[depth]='|'
        print_BST(root.right, depth+1, '\\')

def test(mode):
    insC=[]
    insP=[]
    delC=[]
    delP=[]
    height=[]
    ins=True
    num=[]
    counter=1
    for i in sys.stdin:
        if i == "|\n":
            print(counter)
            counter+=1
            if ins:
                root=Node(num[0])
                num.pop(0)
                insC.append(0)
                insP.append(0)
                height.append(1)
                h=1
                for n in num:
                    res=insert(root, n, 1)
                    insC.append(res[0])
                    insP.append(res[1])
                    if res[2]>h:
                        h+=1
                    height.append(h)
                    if len(num)<=50:
                        print("insert",n)
                        show(root)
                ins=False
            else:
                for n in num:
                    res=delete(root, n)
                    delC.append(res[1])
                    delP.append(res[2])
                    if res[3]==True:
                        if mode==1:
                            h-=1
                        else:
                            h=treeHeight(root)
                    height.append(h)
                    if len(num)<=50:
                        print("delete",n)
                        show(root)
                ins=True
            num=[]
        else:
            num.append(int(i))
    if mode == 0:
        np.savetxt('bstInsC.txt',insC,fmt='%d')
        np.savetxt('bstInsP.txt',insP,fmt='%d')
        np.savetxt('bstdelC.txt',delC,fmt='%d')
        np.savetxt('bstdelP.txt',delP,fmt='%d')
        np.savetxt('bstHeight.txt',height,fmt='%d')
    elif mode == 1:
        np.savetxt('ascBstInsC.txt',insC,fmt='%d')
        np.savetxt('ascBstInsP.txt',insP,fmt='%d')
        np.savetxt('ascBstdelC.txt',delC,fmt='%d')
        np.savetxt('ascBstdelP.txt',delP,fmt='%d')
        np.savetxt('ascBstHeight.txt',height,fmt='%d')
sys.setrecursionlimit(100000)
test(2)
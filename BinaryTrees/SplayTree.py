import sys
import numpy as np

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return 0,0

        self.root,comp,pointers = self.splay(self.root, key)

        node = Node(key)

        if key <= self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None

        self.root = node
        return comp+1,pointers+3

    def delete(self, key):
        if self.root is None:
            return 0,0

        self.root,comp,pointers = self.splay(self.root, key)

        if self.root.key != key:
            return comp,pointers

        if self.root.left is None:
            self.root = self.root.right
            pointers+=3
        elif self.root.right is None:
            self.root = self.root.left
            pointers+=4
        else:
            temp = self.root.right
            self.root = self.root.left
            self.root,c,p = self.splay(self.root, key)
            self.root.right = temp
            comp+=c
            pointers+=p+6
        
        return comp,pointers

    def splay(self, root, key):
        comp=1
        pointers=0
        if root is None or root.key == key:
            return root,0,0

        if key < root.key:
            if root.left is None:
                return root,1,1

            if key < root.left.key:
                root.left.left,comp,pointers = self.splay(root.left.left, key)
                root = self.rotate_right(root)
                comp+=1
                pointers+=8
            elif key > root.left.key:
                root.left.right,comp,pointers  = self.splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self.rotate_left(root.left)
                    pointers+=5
                pointers+=3
                comp+=2

            if root.left is not None:
                return self.rotate_right(root),comp,pointers+6
            else:
                return root,comp,pointers+1

        else:
            if root.right is None:
                return root,1,1

            if key < root.right.key:
                root.right.left,comp,pointers  = self.splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self.rotate_right(root.right)
                    pointers+=5
                comp+=1
                pointers+=3
            elif key > root.right.key:
                root.right.right,comp,pointers  = self.splay(root.right.right, key)
                root = self.rotate_left(root)
                comp+=2
                pointers+=8

            if root.right is not None:
                return self.rotate_left(root),comp,pointers+6
            else:
                return root,comp,pointers+1

    def rotate_right(self, node):
        temp = node.left
        node.left = temp.right
        temp.right = node
        return temp

    def rotate_left(self, node):
        temp = node.right
        node.right = temp.left
        temp.left = node
        return temp

    def tree_height(self):
        return self.height(self.root)
    
    def height(self, node):
        if node is None:
            return 0
        else:
            return 1+max(self.height(node.left),self.height(node.right))

def show(tree):
    global left_trace
    global right_trace
    depth=tree.tree_height()
    left_trace=[None]*depth
    right_trace=[None]*depth
    print_Tree(tree.root,0,"-")

def print_Tree(root, depth, prefix):
    if root == None:
        return
    if root.left != None:
        print_Tree(root.left, depth+1, '/')
    if prefix == '/':
        left_trace[depth-1]='|'
    if prefix == '\\':
        print("-",end="")
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
        print_Tree(root.right, depth+1, '\\')

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
                tree = SplayTree()
                h=0
                for n in num:
                    res=tree.insert(n)
                    insC.append(res[0])
                    insP.append(res[1])
                    height.append(tree.tree_height())
                    if len(num)<=50:
                        print("insert",n)
                        show(tree)
                ins=False
            else:
                for n in num:
                    res=tree.delete(n)
                    delC.append(res[0])
                    delP.append(res[1])
                    height.append(tree.tree_height())
                    if len(num)<=50:
                        print("delete",n)
                        show(tree)
                ins=True
            num=[]
        else:
            num.append(int(i))
    #print(height)
    #print(insC)
    #print(insP)
    #print(delC)
    #print(delP)
    if mode == 0:
        np.savetxt('SplayInsC.txt',insC,fmt='%d')
        np.savetxt('SplayInsP.txt',insP,fmt='%d')
        np.savetxt('SplaydelC.txt',delC,fmt='%d')
        np.savetxt('SplaydelP.txt',delP,fmt='%d')
        np.savetxt('SplayHeight.txt',height,fmt='%d')
    elif mode == 1:
        np.savetxt('ascSplayInsC.txt',insC,fmt='%d')
        np.savetxt('ascSplayInsP.txt',insP,fmt='%d')
        np.savetxt('ascSplaydelC.txt',delC,fmt='%d')
        np.savetxt('ascSplaydelP.txt',delP,fmt='%d')
        np.savetxt('ascSplayHeight.txt',height,fmt='%d')
sys.setrecursionlimit(100000)
test(1)
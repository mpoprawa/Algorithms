import sys
import numpy as np

class Node():
    def __init__(self,key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1

class RBTree():
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.color = 0
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL

    def insert(self, key):
        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL

        y = None
        x = self.root
        h=1
        comp=0
        pointers=1

        while x != self.NIL:
            h+=1
            y = x
            comp+=1
            pointers+=1
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        pointers+=1
        node.parent = y

        if y == None:
            self.root = node
            return 0,0,1
        comp+=1
        pointers+=1
        if node.key < y.key:
            y.left = node
        else:
            y.right = node

        pointers+=1
        if node.parent == None:
            node.color = 0
            return comp,pointers,h
        pointers+=2
        if node.parent.parent == None:
            return comp,pointers,h

        p=self.fix_insert(node)
        pointers+=p

        return comp,pointers,h

    def fix_insert(self, node):
        pointers=0
        while node.parent.color == 1:
            pointers+=1
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                    pointers+=3
                else:
                    if node == node.parent.left:
                        node = node.parent
                        p=self.right_rotate(node)
                        pointers+=1+p
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    p=self.left_rotate(node.parent.parent)
                    pointers+=5+p
                pointers+=3
            else:
                uncle = node.parent.parent.right
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                    pointers+=3
                else:
                    if node == node.parent.right:
                        node = node.parent
                        p=self.left_rotate(node)
                        pointers+=1+p
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    p=self.right_rotate(node.parent.parent)
                    pointers+=5+p
                pointers+=3
            pointers+=4
            if node == self.root:
                break
        self.root.color = 0
        return pointers

    def left_rotate(self, x):
        pointers=9
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            pointers+=1
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
            pointers+=2
        else:
            x.parent.right = y
            pointers+=2
        y.left = x
        x.parent = y
        return pointers

    def right_rotate(self, x):
        pointers=9
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            pointers+=1
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            pointers+=2
            x.parent.right = y
        else:
            pointers+=2
            x.parent.left = y
        y.right = x
        x.parent = y
        return pointers

    def delete(self, key):
        z = self.NIL
        node = self.root
        comp = 0
        pointers = 0
        while node != self.NIL:
            comp+=1
            if node.key == key:
                z = node
                break
            if node.key <= key:
                node = node.right
            else:
                node = node.left
            comp+=1
            pointers+=1

        if z == self.NIL:
            return comp,pointers,False

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            p=self.transplant(z, z.right)
            pointers+=1+p
        elif z.right == self.NIL:
            x = z.left
            p=self.transplant(z, z.left)
            pointers+=2+p
        else:
            y,p = self.minimum(z.right)
            pointers+=p
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
                pointers+=1
            else:
                p=self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                pointers+=3+p

            p=self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            pointers+=7+p
        pointers+=1
        if y_original_color == 0:
            p=self.fix_delete(x)
            pointers+=p
        return comp,pointers,True

    def transplant(self, x, y):
        if x.parent == None:
            self.root = y
            pointers=1
        elif x == x.parent.left:
            x.parent.left = y
            pointers=4
        else:
            x.parent.right = y
            pointers=4
        y.parent = x.parent
        pointers+=1
        return pointers

    def minimum(self, node):
        p=1
        while node.left != self.NIL:
            node = node.left
            p+=1
        return node,p

    def fix_delete(self, x):
        pointers=0
        while x != self.root and x.color == 0:
            pointers+=4

            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    p=self.left_rotate(x.parent)
                    s = x.parent.right
                    pointers+=3+p

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                    pointers+=3
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        p=self.right_rotate(s)
                        s = x.parent.right
                        pointers+=3+p
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    p=self.left_rotate(x.parent)
                    x = self.root
                    pointers+=5+p
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    p=self.right_rotate(x.parent)
                    s = x.parent.left
                    pointers+=3+p

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                    pointers+=3
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        p=self.left_rotate(s)
                        s = x.parent.left
                        pointers+=3+p
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    p=self.right_rotate(x.parent)
                    x = self.root
                    pointers+=5+p
        x.color = 0
        return pointers

    def tree_height(self):
        return self.height(self.root)-1
    
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
    print_RB(tree.root,0,"-")

def print_RB(root, depth, prefix):
    if root == None:
        return
    if root.left != None and root.left.key != None:
        print_RB(root.left, depth+1, '/')
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
    if root.color == 1:
        print("["+str(root.key)+"R]")
    else:
        print("["+str(root.key)+"B]")
    left_trace[depth]=' '
    if root.right != None and root.right.key != None:
        right_trace[depth]='|'
        print_RB(root.right, depth+1, '\\')

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
                tree = RBTree()
                h=0
                for n in num:
                    res=tree.insert(n)
                    insC.append(res[0])
                    insP.append(res[1])
                    if res[2]>h:
                        h+=1
                    height.append(h)
                    if len(num)<=50:
                        print("insert",n)
                        show(tree)
                ins=False
            else:
                for n in num:
                    res=tree.delete(n)
                    delC.append(res[0])
                    delP.append(res[1])
                    if res[2]==True:
                        h=tree.tree_height()
                    height.append(h)
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
        np.savetxt('RBInsC.txt',insC,fmt='%d')
        np.savetxt('RBInsP.txt',insP,fmt='%d')
        np.savetxt('RBdelC.txt',delC,fmt='%d')
        np.savetxt('RBdelP.txt',delP,fmt='%d')
        np.savetxt('RBHeight.txt',height,fmt='%d')
    elif mode == 1:
        np.savetxt('ascRBInsC.txt',insC,fmt='%d')
        np.savetxt('ascRBInsP.txt',insP,fmt='%d')
        np.savetxt('ascRBdelC.txt',delC,fmt='%d')
        np.savetxt('ascRBdelP.txt',delP,fmt='%d')
        np.savetxt('ascRBHeight.txt',height,fmt='%d')
sys.setrecursionlimit(100000)
test(2)
import random
import numpy as np
import timeit

class Graph: 

    def __init__(self, v): 
        self.V = v 
        self.edges = []
        adj = [[0]*v for _ in range(v)]
        for i in range(v):
            for j in range(i):
                w=0
                while w==0 or w==1:
                    w=random.uniform(0,1)
                adj[i][j]=w
                adj[j][i]=w
                self.edges.append([i, j, w])
        self.adj = adj

    def find(self, parent, i): 
        if parent[i] != i: 
            parent[i] = self.find(parent, parent[i]) 
        return parent[i] 
 
    def union(self, parent, rank, x, y): 
        if rank[x] < rank[y]: 
            parent[x] = y 
        else:
            parent[y] = x 
            if rank[x]==rank[y]:
                rank[x] += 1

    def KruskalMST(self): 
        result = []
        parent = [] 
        rank = [] 
        i = 0
        e = 0
        edges = sorted(self.edges, key=lambda item: item[2]) 

        for node in range(self.V): 
            parent.append(node) 
            rank.append(0) 

        while e < self.V - 1: 
            u, v, w = edges[i] 
            x = self.find(parent, u) 
            y = self.find(parent, v) 

            if x != y: 
                e = e + 1
                result.append([u, v, w]) 
                self.union(parent, rank, x, y) 
            i = i + 1

        return result

    def PrimMST(self):
        INF = 1
        G=self.adj
        edge_count = 0
        selected_node = [False]*self.V
        selected_node[0] = True
        result=[]

        while edge_count < self.V - 1: 
            minimum = INF
            u = 0
            v = 0
            for i in range(self.V):
                if selected_node[i]:
                    for j in range(self.V):
                        w=G[i][j]
                        if not selected_node[j]:  
                            if minimum > w:
                                minimum = w
                                u = i
                                v = j
            result.append([u, v, G[u][v]]) 
            selected_node[v] = True
            edge_count += 1

        return result

class Tree:

    def __init__(self, v, mst):
        self.V = v
        self.adj = [[] for _ in range(v)]
        
        for e in mst:
            self.adj[e[0]].append(e[1])
            self.adj[e[1]].append(e[0])

    def notify(self, v, x):
        if x==1:
            self.checked=[False]*self.V
        self.checked[v]=True
        children=[]

        for child in self.adj[v]:
            if self.checked[child]==False:
                children.append(self.notify(child,0))
        
        if len(children)==0:
            return 0
        else:
            children.sort()
            for i in range(len(children)):
                children[i]+=i+1
            return(max(children))

def compare(kruskal,prim,size):
    eps=1e-15
    min1 = 0
    min2 = 0
    for u, v, weight in kruskal: 
        min1 += weight 
        if size<=20:
            print(u,"--",v, ":",weight)
    #print()
    
    for u, v, weight in prim: 
        min2 += weight
        if size<=20: 
            print(u,"--",v, ":",weight)
    
    if abs(min1-min2)<=eps:
        print("MST size:", min1)
        return 0
    else:
        print("FAILURE")
        return 1 

def mst(mode):
    rep=10
    start=20
    end=800
    step=20
    failures=0
    kruskalTime=[]
    primTime=[]

    for i in range(start,end+1,step):
        print(i)
        for _ in range(rep):
            g = Graph(i)

            startK = timeit.default_timer()
            kruskal=g.KruskalMST()
            stopK = timeit.default_timer()

            startP = timeit.default_timer()
            prim=g.PrimMST()
            stopP = timeit.default_timer()

            kruskalTime.append(stopK-startK)
            primTime.append(stopP-startP)
            failures+=compare(kruskal,prim,i)
            print(stopK-startK,stopP-startP)

    print("failures:",failures)
    if mode==1:
        np.savetxt('kruskal.txt',kruskalTime,fmt='%f')
        np.savetxt('prim.txt',primTime,fmt='%f')

def inform(mode):
    rep=25
    start=10
    end=1000
    step=10
    time=[]

    for i in range(start,end+1,step):
        print("i =",i)
        for _ in range(rep):
            g = Graph(i)
            mst = g.KruskalMST()
            tree = Tree(i, mst)
            v=random.randint(0,i-1)
            if i<=20:
                print(tree.adj)
            t=tree.notify(v,1)
            print("v =",v,"time =",t)
            time.append(t)
    if mode==1:
        np.savetxt('inform_time.txt',time,fmt='%d')
#mst(0)
inform(1)
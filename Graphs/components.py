import os
import time

def dfs(adj, s, n):
    visited = [False] * n
    marked = [False] * n
    stack=[]
    stack.append(s) 
    res=[]
    marked[s] = True

    while stack: 
        s = stack[len(stack)-1]
        tail = True

        if not visited[s]: 
            for x in adj[s]: 
                if not marked[x]:
                    stack.append(x)
                    marked[x] = True
                    tail = False
                    adj[s].remove(x)
                    break
            if tail:
                stack.pop()
                res.append(s)
                visited[s] = True
        else:
            stack.pop()
            
    return res

def transpose(adj, n):
    res = [[] for _ in range(n)]
    for i in range(n):
            for j in adj[i]:
                res[j].append(i)
    return res

def components(adj, order, n):
    visited = [False] * n
    components = []
    
    while order:
        c=[]
        v = order.pop()
        if not visited[v]:
            stack = []
            stack.append(v)

            while stack:
                v = stack.pop()
                if not visited[v]:
                    c.append(v+1)
                    visited[v] = True

                    for x in adj[v]:
                        if not visited[x]:
                            stack.append(x)
        if c:
            components.append(c)
    
    if n <= 200:
        print(components)
    print(len(components),"silnie spojnych skladowych")
    for c in range(len(components)):
        print(c+1,"skladowa zawiera",len(components[c]),"wierzcholkow")

def run(graph):
    if graph[0] == 'D':
        directional = True
    else:
        directional = False
    n = int(graph[1])
    del graph[:3]
    adj = [[] for _ in range(n)]
    adj2 = []
    start = 0

    for i in range(0, len(graph), 2):
        e1 = int(graph[i])-1
        e2 = int(graph[i+1])-1
        adj[e1].append(e2)
        if not directional:
            adj[e2].append(e1)

    for a in adj:
        adj2.append(a.copy())

    sTime = time.time()
    order = dfs(adj2, start, n)
    transposed = transpose(adj, n)
    components(transposed, order, n)
    eTime = time.time()
    print("t =",round(eTime-sTime,10))


path = './test/3/'
for root, dirs, files in os.walk(path, topdown=False):
    for name in sorted(files):
        print(os.path.join(root, name))
        file = open(os.path.join(root, name))
        data = file.read().split()
        print(data[0],data[1],data[2])
        run(data)
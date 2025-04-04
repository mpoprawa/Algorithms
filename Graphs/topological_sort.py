import sys
import os
import time

def topologicalSortVisit(s, adj, visited, stack):
    visited[s] = 1
    cycle = 0
    for i in adj[s]:
        if visited[i] == 0:
            cycle += topologicalSortVisit(i, adj, visited, stack)
        elif visited[i] == 1:
            cycle +=1

    visited[s] = 2
    stack.append(s)
    return cycle

def topologicalSort(adj, n):
    cycle = 0
    stack = []
    visited = [0] * n

    for i in range(n):
        if visited[i] == 0:
            cycle += topologicalSortVisit(i, adj, visited, stack)

    if n < 200:
        print("Topological sorting:", end=" ")
        while stack:
            print(stack.pop()+1, end=" ")
        print()
    
    if cycle > 0:
        print("Graph is cyclical")
    else:
        print('Graph is not cyclical')

def run(graph):
    if graph[0] == 'D':
        directional = True
    else:
        directional = False
    n = int(graph[1])
    del graph[:3]
    adj = [[] for _ in range(n)]
    start = 0

    for i in range(0, len(graph), 2):
        e1 = int(graph[i])-1
        e2 = int(graph[i+1])-1
        adj[e1].append(e2)
        if not directional:
            adj[e2].append(e1)
    
    sTime = time.time()
    topologicalSort(adj, n)
    eTime = time.time()
    print("t =",round(eTime-sTime,10))

sys.setrecursionlimit(100000)
path = './test/2/'
for root, dirs, files in os.walk(path, topdown=False):
    for name in sorted(files):
        print(os.path.join(root, name))
        file = open(os.path.join(root, name))
        data = file.read().split()
        run(data)
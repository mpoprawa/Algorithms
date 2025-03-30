import random
import time
import sys
import pandas as pd

class Graph:
    def __init__(self, size, print_flow):
        self.adj = [[] for _ in range(size)]
        self.capacity = [[0] * size for _ in range(size)]
        self.size = size
        self.print = print_flow
        self.path_num = 0
        if print_flow:
            self.flows = [[" "] * size for _ in range(size)]

    def add_edge(self, u, v, c):
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.capacity[u][v] = c
        if self.print:
            self.flows[u][v] = 0
            self.flows[v][u] = 0

    def print_path(self, sink, source, parent, path_flow):
        path = []
        v = sink
        while(v != source):
            path.append(str(v))
            v = parent[v]
        path.append(str(source))
        path.reverse()
        print("Path:", " -> ".join(path), ", Flow:", path_flow)

    def bfs(self, s, t, parent):
        visited = [False] * self.size
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v in self.adj[u]:
                if not visited[v] and self.capacity[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

        return visited[t]

    def edmonds_karp(self, source, sink):
        parent = [-1] * self.size
        max_flow = 0

        while self.bfs(source, sink, parent):
            self.path_num += 1
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.capacity[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while(v != source):
                u = parent[v]
                self.capacity[u][v] -= path_flow
                self.capacity[v][u] += path_flow
                if self.print:
                    self.flows[u][v] += path_flow
                    self.flows[v][u] -= path_flow
                v = parent[v]
            #self.print_path(sink, source, parent, path_flow)
        
        if self.print:
            print(pd.DataFrame(self.flows))
        return max_flow, self.path_num

def ones(num):
    return num.count('1')

def gen_cube(k, print_flow):
    size = 2**k
    cube = Graph(size, print_flow)
    for i in range(size-1):
        e = bin(i)[2:]
        e = e.zfill(k)
        h1 = ones(e)
        z1 = k - h1
        for pos,x in enumerate(e):
            if x == "0":
                e2 = list(e)
                e2[pos] = "1"
                e2 = "".join(e2)
                h2 = ones(e2)
                z2 = k - h2
                e2 = int(e2, 2)
                l = max(h1,z1,h2,z2)
                cube.add_edge(i, e2, random.randint(1,2**l))
    return cube

def gen_glpk(graph, model, source, sink):
    f = open("glpk/"+model, "w")
    l_count = 1

    f.write("/*zmienna decyzyjna xi_j - przeplyw na krawedzi od i do j*/\n\n")
    for u,edges in enumerate(graph.adj):
        for v in edges:
            if u<v:
                f.write("var x"+str(u)+"_"+str(v)+" >= 0;\n")

    f.write("\n/*maksymalizowany przeplyw na krawedziach wychodzacych ze zrodla*/\n\n")
    f.write("maximize max_flow : ")
    for index,v in enumerate(graph.adj[source]):
        f.write("x"+str(source)+"_"+str(v))
        if index+1<len(graph.adj[source]):
            f.write("+")
        else:
            f.write(";\n")

    f.write("\n/*pojemnosci krawedzi grafu*/\n\n")
    for u,edges in enumerate(graph.adj):
        for v in edges:
            if u<v:
                f.write("s.t. label"+str(l_count)+": x"+str(u)+"_"+str(v)+" <= "+str(graph.capacity[u][v])+";\n")
                l_count += 1

    f.write("\n/*ograniczenia przeplywu w wezlach*/\n\n")
    for u,edges in enumerate(graph.adj):
        if u != source and u != sink:
            f.write("s.t. label"+str(l_count)+": ")
            l_count += 1
            for v in edges:
                if u<v:
                    f.write(" + x"+str(u)+"_"+str(v))
                else:
                    f.write(" - x"+str(v)+"_"+str(u))
            f.write(" = 0;\n")

def run_test():
    if sys.argv[1] != "--size" or sys.argv[3] != "--repeat":
        print("invalid arguments")
        return
    if len(sys.argv) >= 7 and sys.argv[5] == "--glpk":
        glpk = sys.argv[6]
    else:
        glpk = None
    if (len(sys.argv) == 6 and sys.argv[5] == "--printflow") or len(sys.argv) == 8 and sys.argv[7] == "--printflow":
        print_flow = True
    else:
        print_flow = False
    k = int(sys.argv[2])
    n = int(sys.argv[4])
    times = []
    flows = []
    paths = []
    f = open("results/max_flow/result"+str(k)+".txt", "w")
    f.write("k "+str(k)+"\n")
    for _ in range(n):
        cube = gen_cube(k,print_flow)
        source = 0
        sink = 2**k-1
        if glpk is not None:
            gen_glpk(cube,glpk,source,sink)

        start = time.time()
        flow,path_num = cube.edmonds_karp(source, sink)
        t = time.time() - start

        times.append(t)
        flows.append(flow)
        paths.append(path_num)
        print("Time:",t)
        print("Max Flow:",flow)
        print("Number of Paths:",path_num)
        print()
    f.write(" ".join(str(t) for t in times)+"\n")
    f.write(" ".join(str(f) for f in flows)+"\n")
    f.write(" ".join(str(p) for p in paths))

run_test()
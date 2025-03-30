import random
import time
import sys

class Graph:
    def __init__(self, size, print_match):
        self.adj = [[] for _ in range(size)]
        self.capacity = [[0] * size for _ in range(size)]
        self.size = size
        self.print = print_match
        if print_match:
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
            for i in range(1,self.size-1):
                for j in range(1,self.size-1):
                    flow = self.flows[i][j]
                    if flow != " " and flow > 0:
                        print(i,j)
        return max_flow

def ones(num):
    return num.count('1')

def gen_graph(k, i, print_match):
    size = 2**(k+1)+2
    graph = Graph(size, print_match)

    for x in range(1,2**k+1):
        graph.add_edge(0,x,1)
        v2 = random.sample(range(2**k+1,2**(k+1)),i)
        for v in v2:
            graph.add_edge(x,v,1)

    for x in range(2**k+1,size-1):
        graph.add_edge(x,size-1,1)

    return graph

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
    if sys.argv[1] != "--size" or sys.argv[3] != "--degree" or sys.argv[5] != "--repeat":
        print("invalid arguments")
        return
    if len(sys.argv) >= 9 and sys.argv[7] == "--glpk":
        glpk = sys.argv[8]
    else:
        glpk = None
    if (len(sys.argv) == 8 and sys.argv[7] == "--printmatching") or (len(sys.argv) == 10 and sys.argv[9] == "--printmatching"):
        print_match = True
    else:
        print_match = False
    k = int(sys.argv[2])
    i = int(sys.argv[4])
    n = int(sys.argv[6])
    times = []
    flows = []
    f = open("results/bipartite/result"+str(k)+"_"+str(i)+".txt", "w")
    f.write("k "+str(k)+"\n")
    f.write("i "+str(i)+"\n")

    for _ in range(n):
        graph = gen_graph(k,i,print_match)
        source = 0
        sink = 2**(k+1)+1
        if glpk is not None:
            gen_glpk(graph,glpk,source,sink)

        start = time.time()
        flow = graph.edmonds_karp(source, sink)
        t = time.time() - start

        times.append(t)
        flows.append(flow)
        print("Time:",t)
        print("Max Flow:",flow)
        print()
    f.write(" ".join(str(t) for t in times)+"\n")
    f.write(" ".join(str(f) for f in flows))

run_test()
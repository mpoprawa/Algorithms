#include <bits/stdc++.h>
using namespace std;

vector<long long> dijkstra(long long V, vector<vector<long long>> adj[], long long S){ 
    priority_queue<pair<long long, long long>, vector<pair<long long, long long>>, greater<pair<long long, long long>>> queue;
    vector<long long> dist(V, LLONG_MAX);

    dist[S] = 0;
    queue.push({0, S});

    while (!queue.empty()){
        long long node = queue.top().second;
        long long dis = queue.top().first;
        queue.pop();
        if (dist[node] == dis) {
            for (vector<long long> k : adj[node]){
                long long v = k[0];
                long long w = k[1];
                if (dis + w < dist[v]){
                    dist[v] = dis + w;
                    queue.push({dis + w, v});
                }
            }
        }
    }
    return dist;
}
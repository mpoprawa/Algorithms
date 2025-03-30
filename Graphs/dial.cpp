#include<bits/stdc++.h>
using namespace std;

vector<long long> dial(long long V, vector<vector<long long>> adj[], long long S, long long C) {
    long long maxdist = C * V;
    vector<unordered_set<long long>> buckets(C+1);
    vector<long long> dist(V + 1, LLONG_MAX);
    dist[S] = 0;
    buckets[0].insert(S);

    long long curr_pos = 0;
    while (true) {
        while (curr_pos < maxdist && buckets[curr_pos%(C+1)].empty()) {
            curr_pos++;
        }

        if (curr_pos >= maxdist)
            break;

        long long v = *buckets[curr_pos%(C+1)].begin();
        buckets[curr_pos%(C+1)].erase(v);

        for (vector<long long> k : adj[v]) {

            long long u = k[0];
            long long w = k[1];

            long long altDist = dist[v] + w;
            long long currentDist = dist[u]; 

            if (altDist < currentDist) {
                if (currentDist != LLONG_MAX) {
                    buckets[currentDist%(C+1)].erase(u);
                }
                buckets[altDist%(C+1)].insert(u);
                dist[u] = altDist;
            }
        }
    }
    return dist;
}
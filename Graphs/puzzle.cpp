#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <queue>
#include <map>
#include <set>
using namespace std;

class Puzzle{
    public:
        int size;
        int visited_states;
        short total_moves;
        bool easy;
        vector<short> start_state;
        vector<short> end_state;
        map<vector<short>, pair<short, pair<short, short>>> visited;
        set<vector<short>> explored;
        vector<pair<short, short>> last_moves;
        
        Puzzle(int n, bool mode){
            size = n;
            easy = mode;
            for (short i=1; i<n*n; i++){
                start_state.push_back(i);
            }
            end_state = start_state;
            end_state.push_back(0);

            random_device rd;
            mt19937 gen(rd());
            if (!easy){
                shuffle(start_state.begin(), start_state.end(), gen);
                start_state.push_back(0);
            }
            else{
                start_state.push_back(0);
                vector<vector<short>> options;
                vector<short> prev = start_state;
                int next;
                for (int i=0; i<20; i++){
                    options = neigbours(start_state);
                    uniform_int_distribution<> dist(0, options.size()- 1);
                    while (true){
                        next = dist(gen);
                        if (options[next] != prev){
                            prev = start_state;
                            start_state = options[next];
                            break;
                        }
                    }
                }
            }
        }

        void show_state(vector<short> state){
            cout<<endl;
            for (int i=0; i<size*size; i++){
                cout<<state[i]<<" ";
                if (state[i]<10){
                    cout<<" ";
                }
                if (i % size == size - 1){
                    cout<<endl;
                }
            }
            cout<<endl;
        }

        bool is_solvable(){
            int inversion_count = 0;
            for (int i=0; i<size*size-2; i++){
                for (int j=i+1; j<size*size-1; j++){
                    if (start_state[i] > start_state[j]){
                        inversion_count++;
                    }
                }
            }

            if (inversion_count%2 == 0){
                return true;
            }
            else{
                return false;
            }
        }

        vector<vector<short>> neigbours(vector<short> state){
            vector<vector<short>> adj;
            vector<short> v;
            short xpos,x,y;
            for (short i=0; i<size*size; i++){
                if (state[i] == 0){
                    xpos = i;
                    x = xpos%size;
                    y = xpos/size;
                    break;
                }
            }
            last_moves.clear();

            //left
            if (x != 0){
                v = state;
                v[xpos] = v[xpos-1];
                v[xpos-1] = 0;
                adj.push_back(v);
                last_moves.push_back({xpos-1,xpos});
            }
            //right
            if (x != size-1){
                v = state;
                v[xpos] = v[xpos+1];
                v[xpos+1] = 0;
                adj.push_back(v);
                last_moves.push_back({xpos+1,xpos});
            }
            //top
            if (y != 0){
                v = state;
                v[xpos] = v[xpos-size];
                v[xpos-size] = 0;
                adj.push_back(v);
                last_moves.push_back({xpos-size,xpos});
            }
            //down
            if (y != size-1){
                v = state;
                v[xpos] = v[xpos+size];
                v[xpos+size] = 0;
                adj.push_back(v);
                last_moves.push_back({xpos+size,xpos});
            }

            return adj;
        }

        short hamming(vector<short> state){
            short h = 0;
            for (int i=0; i<size*size; i++){
                if (i+1 != state[i] && state[i] != 0){
                    h++;
                }
            }
            return h;
        }

        short manhattan(vector<short> state){
            short h = 0;
            short x1,x2,y1,y2, dist;
            for (int i=0; i<size*size; i++){
                if (state[i] != 0){
                    x1 = i % size;
                    y1 = i / size;
                    x2 = (state[i]-1) % size;
                    y2 = (state[i]-1) / size;
                    dist = abs(x1-x2)+abs(y1-y2);
                    h += dist;
                }
            }
            return h;
        } 

        //0 - no heurestic
        //1 - manhattan
        //2 - hamming
        void solve(int mode){
            show_state(start_state);
            if (!is_solvable() && !easy){
                cout<<"The puzzle is unsolvable"<<endl;
                return;
            }

            visited.clear();
            explored.clear();
            visited_states = 0;
            total_moves = 0;
            a_star(mode);
            
            print_moves();
            cout<<"Solved in "<<total_moves<<" moves"<<endl;
            cout<<"Visited "<<visited_states<<" states"<<endl;
        }

        void a_star(int mode){
            priority_queue<tuple<short, short, vector<short>>, vector<tuple<short, short, vector<short>>>, greater<tuple<short, short, vector<short>>>> queue;
            queue.push({0,0,start_state});
            vector<short> current;
            pair<short, short> prev;
            int dist,moves;

            while(current != end_state){
                moves = get<1>(queue.top());
                current = get<2>(queue.top());
                queue.pop();

                if (explored.find(current) == explored.end()){
                    for (vector<short> v : neigbours(current)){
                        prev = last_moves[0];
                        last_moves.erase(last_moves.begin());
                        if (visited.count(v) == 0 || moves+1 < visited[v].first){
                            visited[v] = {moves+1,prev};
                            if (mode == 1){
                                queue.push({manhattan(v)+moves+1,moves+1,v});
                            }
                            else if (mode == 2){
                                queue.push({hamming(v)+moves+1,moves+1,v});
                            }
                            else {
                                queue.push({moves+1,moves+1,v});
                            }
                        }
                    }
                    explored.insert(current);
                    visited_states++;
                }
            }
            total_moves = moves;
            show_state(current);
        }

        void print_moves(){
            vector<short> current = end_state;
            pair<short, short> move = visited[current].second;
            vector<pair<short, short>> moves;
            int move_count = 0;
            int m1,m2;

            while (current != start_state){
                moves.push_back(move);
                swap(current[move.first],current[move.second]);
                move = visited[current].second;
            }

            reverse(moves.begin(), moves.end());
            show_state(start_state);
            for (pair<short, short> m : moves){
                move_count++;
                m1 = m.first;
                m2 = m.second;
                cout<<move_count<<". ("<<m1%size+1<<" "<<m1/size+1<<") ("<<m2%size+1<<" "<<m2/size+1<<")"<<endl;
                swap(current[m.first],current[m.second]);
                show_state(current);
            }
        }
};

int main() {
    Puzzle p0(2,false);
    Puzzle p1(3,false);
    Puzzle p2(4,true);
    Puzzle p3(4,false);
    
    //p0.solve(1);
    p1.solve(1);
    p2.solve(1);
    p3.solve(1);
    
    //p0.solve(2);
    p1.solve(2);
    p2.solve(2);
    p3.solve(2);
    
    //p0.solve(0);
    //p1.solve(0);
    //p2.solve(0);
    //p3.solve(0);
}
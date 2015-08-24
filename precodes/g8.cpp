#include<stdio.h>
#include<string.h>
#include<iostream>
#include<algorithm>
#include<assert.h>
#include<math.h>
#include<stack>
#include<map>
#include<vector>
#include<string>
#include<set>
#include<queue>
#define MP(x,y) make_pair(x,y)
#define clr(x,y) memset(x,y,sizeof(x))
#define forn(i,n) for(int i=0;i<n;i++)
#define sqr(x) ((x)*(x))
#define MAX(a,b) if(a<b) a=b;
#define ll long long
using namespace std;

typedef pair<int,int> PI;
#define COLUMN 9
#define INF 2000000000

vector<PI> my_status[COLUMN];
vector<PI> rival_status[COLUMN];

bool cards[6][10];
bool cards_pool[6][10];

PI s2p(string s)
{
    int x = s[0] - 'A';
    int y = 0;
    if(s.length() == 2) y = s[1] - '1';
    else y = 9;
    return MP(x, y);
}
string p2s(PI p)
{
    string s = "";
    s += p.first + 'A';
    if(p.second == 9) s += "10";
    else s += '1' + p.second;
    return s;
}

void swap(PI &a, PI &b)
{
   PI temp = a; 
   a = b;
   b = temp;
}
void sort_PI(PI &a, PI &b, PI &c)
{
    if(a.second > b.second) swap(a, b);
    if(a.second > c.second) swap(a, c);
    if(b.second > c.second) swap(b, c);
}

bool is_skirmish_line(PI a, PI b, PI c)
{
    sort_PI(a, b, c);
    if(a.second + 1 == b.second && b.second + 1 == c.second) return true;
    return false;
}
bool is_battalion_order(PI a, PI b, PI c)
{
    if(a.first == b.first && b.first == c.first) return true;
    return false;
}
bool is_wedge(PI a, PI b, PI c)
{
    if(is_battalion_order(a, b, c) && is_skirmish_line(a, b ,c)) return true;
    return false;
}
bool is_phalanx(PI a, PI b, PI c)
{
    if(a.second == b.second && b.second == c.second) return true;
    else return false;
}

int calculate_score(PI a, PI b, PI c)
{
    int sum = a.second + b.second + c.second + 3;
    if(is_wedge(a, b ,c)) return sum << 24;
    if(is_phalanx(a, b ,c)) return sum << 18;
    if(is_battalion_order(a, b ,c)) return sum << 12;
    if(is_skirmish_line(a, b ,c)) return sum << 6;
    else return sum;
}

int read()
{
    int line_number;
    cin >> line_number;
    while(line_number--)
    {
        string type, card;
        int region;
        cin >> type;
        if(type == "cardget")
        {
            cin >> card;
            PI p = s2p(card);
            cards[p.first][p.second] = 1; 
        }
        else if(type == "rival")
        {
            cin >> region >> card; 
            rival_status[region].push_back(s2p(card));
        }
        else
        {
            return 0;
        }
    }
    return 1;
}


void write_result(int region, string card_name)
{
    cout << "act " << region << " " << card_name << endl;
}

stack<PI> cards_stack[9];
int result[9];
int vis[9];
int unused_number;
int rounds;
int order[] = {3, 5, 1, 7, 4, 2, 6, 0, 8};

void set_card_to_stack(int region, PI p)
{
    cards_stack[region].push(p);
    my_status[region].push_back(p);
    cards[p.first][p.second] = 0;
    vis[region]++;
}
void init()
{
    for(int i = 0; i < 6; i++)
        for(int j = 0; j < 10; j++)
            cards[i][j] = 0, cards_pool[i][j] = 1;
    unused_number = 30;
    rounds = 30;
}
PI find_a_card()
{
    for(int i = 0; i < 6; i++)
        for(int j = 0; j < 10; j++)
            if(cards[i][j])
                return make_pair(i, j);
    return make_pair(-1, -1);
}

int calculate2(PI a, PI b){
    int sum = 1;
    if(a.first == b.first && abs(a.second - b.second) == 1) return sum << 24;
    if(a.second == b.second) return sum << 18;
    if(a.first == b.first) return sum << 12;
    if(abs(a.second - b.second) == 1) return sum << 6;
    return sum;
}
int find_winning_region(int score)
{
    int pos = -1;
    for(int i = 0; i < COLUMN; i++)
    {
        if(vis[i] != 0) continue;
        if(rival_status[i].size() == 3 && !vis[i])
        {
            int rival_score = calculate_score(rival_status[i][0], rival_status[i][1], rival_status[i][2]);
            if(score >= rival_score)
            {
                pos = i;
            }
        }

        if(rival_status[i].size() == 2 && !vis[i])
        {
            int rival_score = calculate2(rival_status[i][0], rival_status[i][1]);
            if((score >> 6) >= rival_score)
            {
                pos = i;
            }
        }
    }
    return pos;
}

void update_stack()
{
    bool empty = true;
    for(int i = 0; i < 9; i++) if(cards_stack[i].size() > 0) empty = false;

    if(empty)
    {
        vector<PI> cards_in_hand;
        for(int i = 0; i < 6; i++) for(int j = 0; j < 10; j++) if(cards[i][j]) cards_in_hand.push_back(MP(i, j));
        int sz = cards_in_hand.size();
        PI a, b, c;
        int maxx = -1, from;
        int limit = (rounds >= 20) ? (1 << 18) : (1 << 12);

        int type = 0;
        for(int i = 0; i < 9; i++)
        {
            if(vis[i] == 1)
            {
                for(int j = 0; j < sz; j++) for(int k = j + 1; k < sz; k++) 
                {
                    int score = calculate_score(my_status[i][0], cards_in_hand[j], cards_in_hand[k]);

                    if(rival_status[i].size() == 2 && (score >> 6) >= calculate2(rival_status[i][0], rival_status[i][1]))
                    {
                        set_card_to_stack(i, cards_in_hand[j]);
                        set_card_to_stack(i, cards_in_hand[k]);
                        return ;
                    }
                    if(score > maxx)
                    {
                        maxx = score;
                        from = i;
                        type = 1;
                        a = cards_in_hand[j];
                        b = cards_in_hand[k];
                    }
                }
            }
            else if(vis[i] == 2)
            {
                for(int j = 0; j < sz; j++)
                {
                    int score = calculate_score(my_status[i][0], my_status[i][1], cards_in_hand[j]);
                    if(rival_status[i].size() == 2 && (score >> 6) >= calculate2(rival_status[i][0], rival_status[i][1]))
                    {
                        set_card_to_stack(i, cards_in_hand[j]);
                        return ;
                    }
                    if(score > maxx)
                    {
                        maxx = score;
                        from = i;
                        type = 2;
                        a = cards_in_hand[j];
                    }
                }
            }
        }
        if(maxx >=  limit)
        {
            if(type == 1)
            {
                set_card_to_stack(from, a);
                set_card_to_stack(from, b);
                return ;
            }
            else if(type == 2)
            {
                set_card_to_stack(from, a);
                return ;
            }
        }
        maxx = -1;
        for(int i = 0; i < sz; i++) for(int j = i + 1; j < sz; j++) for(int k = j + 1; k < sz; k++)
        {
            int score = calculate_score(cards_in_hand[i], cards_in_hand[j], cards_in_hand[k]);
            if(score > maxx)
            {
                maxx = score;
                a = cards_in_hand[i];
                b = cards_in_hand[j];
                c = cards_in_hand[k];
            }
        }

        int pos = -1;
        pos = find_winning_region(maxx);
        if(pos == -1 && maxx >= limit)
        {
            for(int i = 0; i < 9; i++)
            {
                if(vis[i] != 0) continue;
                if(rival_status[i].size() == 3 && calculate_score(rival_status[i][0], rival_status[i][1], rival_status[i][2]) > maxx) continue;
                pos = i;
                break;
            }
        }
        if(pos != -1)
        {
            set_card_to_stack(pos, a);
            set_card_to_stack(pos, b);
            set_card_to_stack(pos, c);
            return ;
        }



        int card_i = -1, reg = -1;
        maxx = -1;
        for(int i = 0; i < 9; i++)
        {
            if(vis[i] != 1) continue;
            for(int j = 0; j < sz; j++)  
            {
                int score = calculate2(my_status[i][0], cards_in_hand[j]);
                if(score > maxx)
                {
                    maxx = score;
                    card_i = j;
                    reg = i;
                }
            }
        }
        if(maxx >= limit)
        {
            set_card_to_stack(reg, cards_in_hand[card_i]);
            return ;
        }
        for(int j = 8; j >= 0; j--){ int i = order[j]; if(vis[i] == 0) {set_card_to_stack(i, cards_in_hand[0]); return;}}
        for(int j = 8; j >= 0; j--){ int i = order[j]; if(vis[i] == 1) {set_card_to_stack(i, cards_in_hand[0]); return;}}
        for(int j = 8; j >= 0; j--){ int i = order[j]; if(vis[i] == 2 && my_status[i][0].second != my_status[i][1].second && my_status[i][0].first != my_status[i][1].first) 
            {set_card_to_stack(i, cards_in_hand[0]); return;}}
        for(int j = 8; j >= 0; j--){ int i = order[j]; if(vis[i] == 2) {set_card_to_stack(i, cards_in_hand[0]); return;}}
        for(int j = 8; j >= 0; j--){ int i = order[j]; if(vis[i] < 3) {set_card_to_stack(i, cards_in_hand[0]); return;}}
    }
}
void solve()
{
    for(int i = 0; i < 9; i++)
    {
        if(my_status[i].size() == 3 && rival_status[i].size() == 3)  
        {
            if(calculate_score(my_status[i][0], my_status[i][1], my_status[i][2]) > calculate_score(rival_status[i][0], rival_status[i][1], rival_status[i][2]))
                result[i] = 1;
            else
                result[i] = -1;
        }
        else
        {
            result[i] = 0;
        }
    }
    update_stack();

    for(int i = 0; i < COLUMN; i++)
        if(cards_stack[i].size())
        {
            PI p = cards_stack[i].top();
            cards_stack[i].pop();
            write_result(i, p2s(p));
            return ;
        }
}

void test()
{
    PI a = make_pair(1, 1);
    PI b = make_pair(1, 1);
    PI c = make_pair(1, 0);
    printf("%d\n", calculate_score(a, b ,c));
}
int main() {
    //freopen("in", "r", stdin);
    //test();
    init();
    while(true)
    {
        if(read() == 0) break;

        solve();
//        printf("%d\n", rounds);
        rounds--;
    }
    return 0;
}

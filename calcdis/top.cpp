#include <bits/stdc++.h>

int N = 599816;
int REALN;
std::string folder = "porto_all";
std::string dist = "frechet";

const int ENUM = 100;

std::vector<std::vector<std::pair<double, int>>> vvall;
std::vector<double> dv;
int dv_pos;
//std::vector<std::pair<double, int>> v;

double r_readdouble(FILE *f){
    double res = 0, point = 0;
    char c = ' ';
    for (; c != '+' && c != '-' && !(c >= '0' && c <= '9'); c = getc(f));
    int minus = c == '-';
    if (c >= '0' && c <= '9')
        res = c - '0';
    for (; c = getc(f); ){
        if (c >= '0' && c <= '9'){
            res = res * 10 + c - '0';
            point *= 10;
        }
        else if (c == '.')
            point = 1;
        else break;
    }
    return (1 - minus * 2) * res / (point ? point : 1);
}

double readdouble(FILE *f){
    return dv[dv_pos ++ ];
}

void Main(FILE *f, int offset, int remain, std::vector<std::vector<int>> &vvmin, std::vector<std::vector<int>> &vvmax){
    std::cout << "Sorting... " << offset << " / " << remain + offset << '\n';
    for (int i = 0; i < N; i ++ ){
        //if (i % 100 == 0) std::cout << "doing " << i + offset << '\n';
        for (int j = 0; j < REALN; j ++ ){
            //v.push_back(std::make_pair(num, j));
            vvall[i][j].second = j;
            vvall[i][j].first = readdouble(f);
        }
        //vvall.push_back(v);
    }
    #pragma omp parallel for
    for (int i = 0; i < N; i ++ ){
        auto &v = vvall[i];
        std::sort(v.begin(), v.end());
        std::vector<int> vmax, vmin;
        auto ite = v.begin();
        for (int j = 0; j < ENUM; j ++ )
            //vmin.push_back((ite ++ )->second);
            vvmin[i + offset][j] = (ite ++ )->second;
        ite = v.end();
        for (int j = 0; j < ENUM; j ++ )
            //vmax.push_back(( -- ite)->second);
            vvmax[i + offset][j] = ( -- ite)->second;
        //vvmax[i + offset] = vmax;
        //vvmin[i + offset] = vmin;
    }
    
}

int main(int argc, char ** argv){
    if (argc > 1){
        N = atoi(argv[1]);
        folder = argv[2];
        dist = argv[3];
        std::cout << "setting changed\n";
    }
    FILE *f = fopen(("dis/" + folder + "/" + dist + ".txt").c_str(), "r");
    std::vector<std::vector<int>> vvmax, vvmin;
    vvmax.resize(N);
    vvmin.resize(N);
    
    for (auto &i : vvmin)
        i.resize(ENUM);
    for (auto &i : vvmax)
        i.resize(ENUM);
    

    dv.resize(((long long)N) * N);
    for (long long i = 0; i < 1LL * N * N; i ++ ){
        dv[i] = r_readdouble(f);
        if (i % 10000000 == 0) std::cout << i << " / " << 1LL * N * N << '\n';
    }

    REALN = N;
    N = 900;
    int remain = REALN;
    vvall.resize(N);
    for (auto &i : vvall)
        i.resize(REALN);
    for (int i = 0; remain; i += N){
        if (remain < N) N = remain;
        Main(f, i, remain, vvmin, vvmax);
        remain -= N;
    }

    N = REALN;
    freopen((folder + "_" + dist + ".txt").c_str(), "w", stdout);
    std::cout << N << ' ' << ENUM << '\n';
    for (int i = 0; i < N; i ++ ){
        for (auto j : vvmin[i])
            std::cout << j << ' ';
        std::cout << '\n';
    }
    for (int i = 0; i < N; i ++ ){
        for (auto j : vvmax[i])
            std::cout << j << ' ';
        std::cout << '\n';
    }
}

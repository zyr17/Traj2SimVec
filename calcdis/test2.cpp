//g++ -O2 -fopenmp -std=c++11 -o test test.cpp

#include <bits/stdc++.h>


std::vector<std::vector<double>> cmp_vec, res_vec, dis, vecdis;

double readdouble(FILE *f){
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

double calcvecdis(std::vector<double> &x, std::vector<double> &y){
    assert(x.size() == y.size());
    double tot = 0;
    for (int i = 0; i < x.size(); i ++ )
        tot += (x[i] - y[i]) * (x[i] - y[i]);
    return std::sqrt(tot);
}

void initvec(std::string v, std::vector<std::vector<double>> & vv){
    vv.clear();
    FILE *f = fopen(v.c_str(), "r");
    if (f == NULL) return;
    //std::cout << v << '\n'; return;
    int N, VNUM;
    fscanf(f, "%d%d", &N, &VNUM);
    for (int i = 0; i < N; i ++ ){
        std::vector<double> vvv;
        for (int j = 0; j < VNUM; j ++ ){
            double db = readdouble(f);
            //fscanf(f, "%f", &db);
            vvv.push_back(db);
        }
        vv.push_back(vvv);
    }
    fclose(f);
}

void init(std::string m, std::string res_v, std::string cmp_v){
    initvec(cmp_v, cmp_vec);
    initvec(res_v, res_vec);
    vecdis.clear();
    vecdis.resize(res_vec.size());
    auto start_time = clock();
    for (auto &i : vecdis)
        i.resize(cmp_vec.size());
    std::cout << res_vec.size() << ' ' << cmp_vec.size() << '\n';
    for (int i = 0; i < res_vec.size(); i ++ )
        #pragma omp parallel for
        for (int j = 0; j < cmp_vec.size(); j ++ )
            vecdis[i][j] = calcvecdis(res_vec[i], cmp_vec[j]);
    std::cout << clock() - start_time << "read vec\n";
    if (!dis.size()){
        //FILE *f = fopen(m.c_str(), "r");
        dis.resize(res_vec.size());
        for (auto &i : dis)
            i.resize(cmp_vec.size());
            /*
        for (int i = 0; i < res_vec.size(); i ++ ){
            for (int j = 0; j < cmp_vec.size(); j ++ )
                //fscanf(f, "%f", dis[i][j]);
                dis[i][j] = readdouble(f);
            if (i % (res_vec.size() / 100) == 0) std::cout << "reading " << i << ' ' << clock() <<'\n';
        }
        std::cout << "read dis\n";
        fclose(f);
        */
    }
    std::cout << m << ' ' << res_v << ' ' << cmp_v << '\n';
}

const int TOPX = 10, TOPY = 50;

void calc(){
    auto start_time = clock();
    long long stopx = 0, stopy = 0, stopxiny = 0;
    std::vector<long long> topx, topy, topxiny;
    topx.resize(res_vec.size());
    topy.resize(res_vec.size());
    topxiny.resize(res_vec.size());
    #pragma omp parallel for
    for (int i = 0; i < res_vec.size(); i ++ ){
        std::vector<std::pair<double, int>> real_rank, eval_rank;
        for (int j = 0; j < cmp_vec.size(); j ++ ){
            eval_rank.push_back(std::make_pair(dis[i][j], j));
            real_rank.push_back(std::make_pair(vecdis[i][j], j));
        }
        //std::sort(real_rank.begin(), real_rank.end());
        std::sort(eval_rank.begin(), eval_rank.end());
        std::set<int> set;
        for (int k = 1; k <= TOPX; k ++ )
            set.insert(real_rank[k].second);
        for (int k = 1; k <= TOPX; k ++ )
            topx[i] += set.find(eval_rank[k].second) != set.end();
        for (int k = 1; k <= TOPY; k ++ )
            topxiny[i] += set.find(eval_rank[k].second) != set.end();
        for (int k = 1; k <= TOPY; k ++ )
            set.insert(real_rank[k].second);
        for (int k = 1; k <= TOPY; k ++ )
            topy[i] += set.find(eval_rank[k].second) != set.end();
    }
    for (int i = 0; i < res_vec.size(); i ++ ){
        stopx += topx[i];
        stopy += topy[i];
        stopxiny += topxiny[i];
    }
    std::cout << clock() - start_time << '\n';
    std::cout << stopx * 1.0 / res_vec.size() / TOPX << ' ' << stopy * 1.0 / res_vec.size() / TOPY << ' ' << stopxiny * 1.0 / res_vec.size() / TOPX << '\n';
}

int main(int argc, char ** argv){
    std::string mat = argv[1];
    for (int i = 2; i < argc; i += 2){
        std::string result_vectors = argv[i];
        std::string cmp_vectors = argv[i + 1];
        init(mat, result_vectors, cmp_vectors);
        calc();
    }
}

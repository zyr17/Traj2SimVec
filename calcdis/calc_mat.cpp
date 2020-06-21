//g++ -std=c++11 -O2 -o calc_mat calc_mat.cpp -fopenmp
// ./calc_mat frechet < trajectories.txt
// txt: N lines, every line: k x1 y1 x2 y2 ... xk yk

#define SHANGHAI

#include <bits/stdc++.h>

std::vector<std::vector<double>> result;
std::vector<std::vector<std::pair<double, double>>> test_traj, all_traj;

#define pi 3.1415926535897932384626433832795
#define EARTH_RADIUS 6371004
double rad(double d)
{
    return d * pi /180.0;
}
double RealDistance1(double lat1,double lng1,double lat2,double lng2)
{
	
	double a;
   	double b;
   	double radLat1 = rad(lat1);
    double radLat2 = rad(lat2);
    a = radLat1 - radLat2;
    b = rad(lng1) - rad(lng2);
    double s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radLat1)*cos(radLat2)*pow(sin(b/2),2)));
    s = s * EARTH_RADIUS;
    //s = s * 1000;
    return s;
}

#ifdef SHANGHAI
    #define AREA_LAT 31.253
#else
    #define AREA_LAT 41.1579438
#endif

std::pair<double, double> geo2rect(double pos0, double pos1){
    double x = pi * EARTH_RADIUS * cos(AREA_LAT * pi / 180) / 180 * pos0;
    double y = pi * EARTH_RADIUS / 180 * pos1;
    return std::make_pair(x, y);
}

double calc_dis(std::pair<double, double> x, std::pair<double, double> y){
    x = geo2rect(x.second, x.first);
    y = geo2rect(y.second, y.first);
    return std::sqrt((x.first - y.first) * (x.first - y.first) + (x.second - y.second) * (x.second - y.second));
    //return RealDistance(x.second, x.first, y.second, y.first);
}
double RealDistance(double a, double b, double c, double d){
    return calc_dis(std::make_pair(a, b), std::make_pair(c, d));
}

double readdouble(){
    double res = 0, point = 0;
    char c = ' ';
    for (; c != '+' && c != '-' && !(c >= '0' && c <= '9'); c = getchar());
    int minus = c == '-';
    if (c >= '0' && c <= '9')
        res = c - '0';
    for (; c = getchar(); ){
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

double frechet(std::vector<std::pair<double, double>> &i, std::vector<std::pair<double, double>> &j){
    std::vector<std::vector<double>> d;
    d.resize(i.size());
    for (auto &k : d)
        k.resize(j.size());
    for (int k = 0; k < i.size(); k ++ )
        for (int l = 0; l < j.size(); l ++ ){
            double dis = calc_dis(i[k], j[l]);
            if (k + l == 0) d[k][l] = dis;
            else if (k == 0) d[k][l] = std::max(d[k][l - 1], dis);
            else if (l == 0) d[k][l] = std::max(d[k - 1][l], dis);
            else d[k][l] = std::max(std::min(std::min(d[k - 1][l], d[k][l - 1]), d[k - 1][l - 1]), dis);
        }
    return d[i.size() - 1][j.size() - 1];
}

double dtw(std::vector<std::pair<double, double>> &i, std::vector<std::pair<double, double>> &j){
    std::vector<std::vector<double>> d;
    d.resize(i.size());
    for (auto &k : d)
        k.resize(j.size());
    for (int k = 0; k < i.size(); k ++ )
        for (int l = 0; l < j.size(); l ++ ){
            double dis = calc_dis(i[k], j[l]);
            if (k + l == 0) d[k][l] = dis;
            else if (k == 0) d[k][l] = d[k][l - 1] + dis;
            else if (l == 0) d[k][l] = d[k - 1][l] + dis;
            else d[k][l] = std::min(std::min(d[k - 1][l], d[k][l - 1]), d[k - 1][l - 1]) + dis;
        }
    return d[i.size() - 1][j.size() - 1];
}

double haus(std::vector<std::pair<double, double>> &i, std::vector<std::pair<double, double>> &j){
    std::vector<std::vector<double>> d;
    d.resize(i.size());
    for (auto &k : d)
        k.resize(j.size());
    for (int k = 0; k < i.size(); k ++ )
        for (int l = 0; l < j.size(); l ++ )
            d[k][l] = calc_dis(i[k], j[l]);
    double resi = 0, resj = 0;
    for (int k = 0; k < i.size(); k ++ ){
        double nowmin = 1e100;
        for (int l = 0; l < j.size(); l ++ )
            nowmin = std::min(nowmin, d[k][l]);
        resi = std::max(nowmin, resi);
    }
    for (int l = 0; l < j.size(); l ++ ){
        double nowmin = 1e100;
        for (int k = 0; k < i.size(); k ++ )
            nowmin = std::min(nowmin, d[k][l]);
        resj = std::max(nowmin, resj);
    }
    return std::max(resi, resj);
}

void init(std::string fname, std::vector<std::vector<std::pair<double, double>>> &traj){
    int N;
    freopen(fname.c_str(), "r", stdin);
    scanf("%d", &N);
    traj.resize(N);
    for (auto &t : traj){
        int n = readdouble();
        t.resize(n);
        for (auto &i : t){
            i.first = readdouble();
            i.second = readdouble();
        }
    }
}

void save(std::string filename){
    std::cout << "calc done, saving...\n";
    freopen(filename.c_str(), "w", stdout);
    for (auto &i : result){
        for (auto j : i)
            printf("%.10f ", j);
        printf("\n");
    }
}

void Main(int argc, char ** argv){
    std::string way = argv[1];
    std::string test_trajf = argv[2];
    std::string all_trajf = argv[3];
    if (way != "frechet" && way != "dtw" && way != "hausdorff"){
        std::cout << "unknown way " << way << '\n';
        return;
    }
    init(test_trajf, test_traj);
    init(all_trajf, all_traj);
    result.resize(test_traj.size());
    for (auto &i : result)
        i.resize(all_traj.size());
    for (int i = 0; i < test_traj.size(); i ++ ){
        if (i % (test_traj.size() / 100) == 0)
            std::cout << "calc route " << i << '\n';
        #pragma omp parallel for
        for (int j = 0; j < all_traj.size(); j ++ ){
            if (way == "frechet")
                result[i][j] = frechet(test_traj[i], all_traj[j]);
            else if (way == "dtw")
                result[i][j] = dtw(test_traj[i], all_traj[j]);
            else if (way == "hausdorff")
                result[i][j] = haus(test_traj[i], all_traj[j]);
        }
    }
    save(way + ".txt");
}

int main(int argc, char ** argv){
    /*for (;;){
        double a, b, c, d;
        std::cin >> a >> b >> c >> d;
        std::cout << RealDistance(a, b, c, d) << '\n';
        std::cout << RealDistance1(a, b, c, d) << '\n';
    }*/
    Main(argc, argv);
}

#include<cstdio>
#include<algorithm>
#include<ctime>
#include<queue>
#include<cstdlib>
#include<utility>
#include<vector>
using namespace std;
// Customer Data Struct
typedef pair<int, int> pii;
struct Edge {
	int st, ed, w;
};

bool cmp(pii a, pii b) {
	return a.first > b.first;
}

struct Gain {
	int a, b, w;
};
// -------- 변수 ---------
FILE * inp = fopen("g20k.txt", "r");
FILE * out = fopen("KL_Result.txt", "w");

const int M_size = 20001; // 최대 vertex Size;
const int E_size = 120000; // 최대 Edge Size;
const int Process_Count = 5;
int N, M; // N, M
vector<pii> adj[M_size]; // 근접행렬
vector<int> G_A, G_B; // group A, group B
Edge edge[E_size]; // edge 저장
bool Check_A[M_size], Check_B[M_size]; // 분류 시킬때 O(1)로 그룹 구성 컴포넌트 학인을 위한 Check 배열
int InterCost[M_size], OuterCost[M_size]; // D(x) 를 구하기 위한 Outer, Inter 배열
int Dis[M_size]; // Dis(x) 
time_t starttime, endtime;
double alltime=0; // 프로그램 시작, 종료시간
// -------- 함수 ----------

void Initial(); // Input 값 받아오기
void get_Dis(); // Dis(a) 계산
Gain get_G(); // G(a,b) 값 얻기
int search_idx(vector<pii> cont, int st, int ed, int value); // pair<int,int>자료형 이분 탐색
void update_data(Gain tmp); // a,b교환에 따른 데이터 최신화
void Divide_group(); // 그룹 나누기
void Result_Print(int Max_Cut, int Min_Cut, int Avr_Cut); // 결과 출력

//----------------------------------------------------------------------
int main(void) {
	srand((unsigned int)time(NULL)); // 실행될때마다 랜덤 인풋 적용
	Gain DD;
	Initial(); // 인풋값 받아 오기
	int Max_Cut = 0, Min_Cut = 1e9, Avr_Cut = 0;
	for (int i = 0; i < Process_Count; i++) {
		starttime = clock();
		printf("%d 번째 실행중.......\n", i + 1);
		int ans = 0;
		Divide_group(); // Step 1. 그룹 나누기
		while (1) {
			get_Dis(); // Step 2. Distance 계산
			DD = get_G(); // Step 3. 가장 큰 G(a,b) 찾기
			if (DD.w > 0) { // Step 4. 찾은 G(a,b)가 양수이면 데이터 최신화(update_data) 후 Step 2로 이동 , 음수이면 break
				ans += DD.w;
				update_data(DD);
			}
			else break;
		}
		printf("%d 번째 종료.\n", i + 1);
		endtime = clock();
		printf("실행시간 : %lf초 \n", (double)(endtime - starttime) / (CLOCKS_PER_SEC));
		alltime += (double)(endtime - starttime) / (CLOCKS_PER_SEC);
		fprintf(out, "%d번째 KL 알고리즘 결과 값 : %d\n", i + 1, ans);
		Max_Cut = max(ans, Max_Cut);
		Min_Cut = min(ans, Min_Cut);
		Avr_Cut += ans;
	}
	printf("\n\n********************\n프로그램 종료\n************************\n");
	Result_Print(Max_Cut, Min_Cut, Avr_Cut / Process_Count);
	return 0;
}

void Initial() {
	fscanf(inp, "%d %d", &N, &M);
	for (int i = 0; i < M; i++) {
		fscanf(inp, "%d %d %d", &edge[i].st, &edge[i].ed, &edge[i].w);
	}
}

void Divide_group() {
	memset(Check_A, 0, sizeof(Check_A));
	memset(Check_B, 0, sizeof(Check_B));
	memset(OuterCost, 0, sizeof(OuterCost));
	memset(InterCost, 0, sizeof(InterCost));
	G_A.clear(); G_B.clear();
	for (int i = 0; i <= N; i++) adj[i].clear();
	for (int i = 0; i < N; i++) {
		int component;
		if (i % 2 == 0) { // 현재 i가 짝수이면 A그룹에 추가
			while (1) {
				component = rand() % N;
				if (!Check_A[component] && !Check_B[component]) break;
			}
			Check_A[component] = true;
			G_A.push_back(component);
		}
		else { // 홀수이면 B그룹에 추가
			while (1) {
				component = rand() % N;
				if (!Check_A[component] && !Check_B[component]) break;
			}
			Check_B[component] = true;
			G_B.push_back(component);
		}
	}

	for (int i = 0; i < M; i++) {
		int S = edge[i].st, T = edge[i].ed, W = edge[i].w;
		adj[S].push_back(pii(T, W));
		adj[T].push_back(pii(S, W));
		if (Check_A[S] && Check_A[T] || Check_B[S] && Check_B[T]) InterCost[S] += W, InterCost[T] += W; // 서로같은 그룹이면 Indegree 추가
		else OuterCost[S] += W, OuterCost[T] += W; // 다른그룹이면 Outdegree 추가
	}

	for (int i = 1; i <= N; i++) {
		sort(adj[i].begin(), adj[i].end()); // c(a,b) binary_search 탐색을 위한 정렬
	}
}

void get_Dis() {
	for (int i = 0; i < N; i++) {
		Dis[i] = OuterCost[i] - InterCost[i];
	}
}

Gain get_G() {
	vector<pii> D_A, D_B;
	for (int i : G_A) { // A그룹의 Distance 값 저장
		D_A.push_back(pii(Dis[i], i));
	}
	for (int i : G_B) { // B그룹의 Distance 값 저장
		D_B.push_back(pii(Dis[i], i));
	}
	sort(D_A.begin(), D_A.end(), cmp);  // 각각 정렬
	sort(D_B.begin(), D_B.end(), cmp);

	int max_g = 0, a_idx = -1, b_idx = -1;
	for (pii a : D_A) {
		for (pii b : D_B) {
			if (max_g >= a.first + b.first) break; // D(a) + D(b) 가 이제까지 max값 보다 작을시 break
			int c = search_idx(adj[a.second], 0, adj[a.second].size() - 1, b.second); // 공통되는 edge가 있으면 c는 edge가중치 값 없을시 0
			if (c == -1) c = 0;
			else c = adj[a.second].at(c).second;
			if (max_g < a.first + b.first - 2 * c) { // D(a) + D(b) 가 이제까지 max값 보다 크면 값 최신화
				a_idx = a.second;
				b_idx = b.second;
				max_g = a.first + b.first - 2 * c;
			}
		}
	}
	Gain result; // Result 값 저장
	result.a = a_idx, result.b = b_idx, result.w = max_g;
	return result;
}

int search_idx(vector<pii> cont, int st, int ed, int value) {
	if (ed < st) return -1;
	if (cont.at(st).first == value) return st;
	if (st == ed) return -1;
	int mid = (st + ed) / 2;\

	if (cont.at(mid).first > value) {
		return search_idx(cont, st, mid, value);
	}
	else {
		return search_idx(cont, mid + 1, ed, value);
	}
}

void update_data(Gain tmp) { // A 에속한 a , B에 속한 b 바꾸기, check, G_A, G_B , (Outer, Inter)Cost 최신화
	int a = tmp.a;
	int b = tmp.b;
	// 교체되는 컴포넌트에 연결된 vertex들의 OuterCost, InterCost 업데이트.
	for (int k : G_A) {
		if (k == a) continue;
		int k_idx = search_idx(adj[k], 0, adj[k].size() - 1, a);
		if (k_idx != -1) {
			OuterCost[k] += adj[k].at(k_idx).second;
			OuterCost[a] += adj[k].at(k_idx).second;
			InterCost[k] -= adj[k].at(k_idx).second;
			InterCost[a] -= adj[k].at(k_idx).second;
		}
		k_idx = search_idx(adj[k], 0, adj[k].size() - 1, b);
		if (k_idx != -1) {
			OuterCost[k] -= adj[k].at(k_idx).second;
			OuterCost[b] -= adj[k].at(k_idx).second;
			InterCost[k] += adj[k].at(k_idx).second;
			InterCost[b] += adj[k].at(k_idx).second;
		}
	}
	for (int k : G_B) {
		if (k == b) continue;
		int k_idx = search_idx(adj[k], 0, adj[k].size() - 1, b);
		if (k_idx != -1) {
			OuterCost[k] += adj[k].at(k_idx).second;
			OuterCost[b] += adj[k].at(k_idx).second;
			InterCost[k] -= adj[k].at(k_idx).second;
			InterCost[b] -= adj[k].at(k_idx).second;
		}
		k_idx = search_idx(adj[k], 0, adj[k].size() - 1, a);
		if (k_idx != -1) {
			OuterCost[k] -= adj[k].at(k_idx).second;
			OuterCost[a] -= adj[k].at(k_idx).second;
			InterCost[k] += adj[k].at(k_idx).second;
			InterCost[a] += adj[k].at(k_idx).second;
		}
	}
	// 선택된 a,b 각각 그룹에서 제외
	Check_A[a] = false;
	Check_B[b] = false;
	vector<int> ::iterator iter_1;
	for (iter_1 = G_A.begin(); iter_1 != G_A.end(); iter_1++) {
		if ((*iter_1) == a) break;
	}
	G_A.erase(iter_1);
	for (iter_1 = G_B.begin(); iter_1 != G_B.end(); iter_1++) {
		if ((*iter_1) == b) break;
	}
	G_B.erase(iter_1);
}

void Result_Print(int Max_Cut, int Min_Cut, int Avr_Cut) {
	fprintf(out, "\n\n\n----------------Result---------------\n");
	fprintf(out, "Min_Cut 값 : %d\n", Min_Cut);
	fprintf(out, "Max_Cut 값 : %d\n", Max_Cut);
	fprintf(out, "Avr_Cut 값 : %d\n", Avr_Cut);
	fprintf(out, "총 실행 시간 : %lf초\n", alltime);
	fprintf(out, "평균 실행 시간 : %lf초\n", alltime / (double)Process_Count);
	fprintf(out, "-------------------------------------\n");
}

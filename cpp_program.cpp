#include <iostream>
#include <vector>
#include <stack>
#include <unordered_map>
#include <queue>
#include <fstream>
#include <csignal>
using namespace std;


    

class Solution {
    public:
        int bulbSwitch(int n) {
            vector<int> arr(n, 0);
            int flag = 0;
            for (int i = 1; i <= n; i++) {
                for (int j = i - 1; j < n; j += i) {
                    arr[j] = 1 - arr[j];
                }
            }
            for (int i = 0; i < n; i++) {
                flag += arr[i];
            }
            return flag;
        }
};void segfault_handler(int signal) {     std::ofstream fout("exceptionLog.txt", std::ios_base::app);     fout << "Segmentation fault occurred!" << std::endl;     fout.close();     exit(signal);};int main() {signal(SIGSEGV, segfault_handler);
 Solution sol; cout << sol.bulbSwitch(1);
 };
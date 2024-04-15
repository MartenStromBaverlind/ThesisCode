#include <iostream>
#include <vector>
using namespace std;
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};
class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        if(head == NULL) return NULL;
        if(head->next == NULL) return head;

        vector<ListNode*> v;
        ListNode* temp = head;

        while(temp){
            v.push_back(temp);
            temp = temp->next;
        }
        
        int n = v.size();
        k = k % n;

        if(k == 0) return head;
        
        v[n-1]->next = head;
        v[n-k-1]->next = NULL;
        
        return v[n-k];
    }
};

// Add a main function that calls the solution class
int main() {
    Solution sol;
    vector<int> input1 = {1, 2, 3, 4, 5};
    vector<int> input2 = {0, 1, 2};

    ListNode* head1 = new ListNode(input1[0]);
    ListNode* curr = head1;
    for(int i = 1; i < input1.size(); i++) {
        curr->next = new ListNode(input1[i]);
        curr = curr->next;
    }

    ListNode* result1 = sol.rotateRight(head1, input2[0]);

    // Check the result
    while(result1) {
        cout << result1->val << " ";
        result1 = result1->next;
    }
    cout << endl;

    ListNode* head2 = new ListNode(input2[0]);
    ListNode* curr2 = head2;
    for(int i = 1; i < input2.size(); i++) {
        curr2->next = new ListNode(input2[i]);
        curr2 = curr2->next;
    }

    ListNode* result2 = sol.rotateRight(head2, input2[1]);

    // Check the result
    while(result2) {
        cout << result2->val << " ";
        result2 = result2->next;
    }
    cout << endl;

    return 0;
}


    


#include <iostream>
#include <vector>
using namespace std;

int main() {
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
     
    if(head==NULL) return NULL;
    if(head->next==NULL) return head;
    vector<ListNode*> v;
    ListNode* temp=head;

    while(temp){
        v.push_back(temp);
        temp=temp->next;
    }
    int n=v.size()-1;
    int indx=abs(n-k)+1;
    
    if(indx==0) return head;
    else{
        v[indx-1]->next=NULL;
        v[n]->next=head;
        head=v[indx];
        return head;
    }
}};
 



    
    return 0;
}
    


#include<bits/stdc++.h>
using namespace std;
class node
{
   public:
   vector<pair<int, char>> animal;
   node * parent;
   node * child;

   node()
   {
      this->animal = vector<pair<int, char>> ();
      this->child = NULL;
      this->parent = NULL;
   }

   node(int data, char x)
   {
      this->animal.push_back(pair<int,char>(data,x));
      this->child = NULL;
      this->parent = NULL;
   }
};


vector<int> solve (int N, vector<string> &input)
{
   // Your code goes here
   vector<int> ans;
   node * prev = NULL;
   node *current = new node();
   current->parent = NULL;
   for (auto i : input)
   {
      if (i == "{")
      {
         prev = current;
         current = new node();
         prev->child = current;
         current->parent = prev;
      }
      else if (i == "}")
      {
         current = prev;
         prev = current->parent;
      }
      else if(i.size() == 7)
      {
         int flag = 0;
         node *prev2 = current;
         while(prev2!= NULL)
         {
            for(auto x: prev2->animal)
            {
               if(x.second ==i[6])
               {
                  ans.push_back(x.first);
                  flag = 1;
                  break;
               }
            }
            if(flag == 1)
            {
               break;
            }
            prev2 = prev->parent;
      }
      if(flag == 0)
      {
         cout << "undefined";
      }

   }
   else
   {
      current->animal.push_back(pair<int,char> (stoi(i.substr(9)),char(i[7])));
   }
   return ans;
    }
}
int main()
{
    int N=5;
    vector<string> command(N);
    command.push_back("{");
    command.push_back("assign a 4");
    command.push_back("print a");
    command.push_back("}");
    command.push_back("print a");

    vector<int> out;
    out = solve(N, command);
    cout << out[0];
    for(int iout = 1; iout < out.size(); iout++)
    {
        cout << "\n" << out[iout];
    }
    return 0;
}

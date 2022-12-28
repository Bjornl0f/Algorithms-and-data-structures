#include <iostream>
#include <string.h>

using namespace std;


struct Node
{
    char* word;
    Node *left, *right;
};


int ArrayLen(const char* _text)
{
    int count = 0;
    for(int i = 0; _text[i] != '\0'; i++)
    {
        count++;
    }
    return count;
}


void addElement(Node* &root, char* w)
{
    if(!root)
    {
        root = new Node;
        root->word = strdup(w);
        root->left = nullptr;
        root->right = nullptr;
        return;
    }
    
    if(ArrayLen(root->word) > ArrayLen(w))
    {
        addElement(root->right, w);
    }
    else
    {
        addElement(root->left, w);
    }
}


void printTree(Node* root)
{
    if(root)
    {
        printTree(root->left);
        printTree(root->right);
        cout << "Node's word: " << root->word << endl;
    }
}


int countWord(Node* root, char* w)
{
    int count = 0;
    if(root)
    {
        count += countWord(root->left, w);
        count += countWord(root->right, w);
        if(strcmp(root->word, w) == 0)
        {
            count++;
        }
    }
    return count;
}


int main()
{
    Node* root = NULL;
    char line[100];
    char word[50];
 
    cout << "Enter string: ";
    cin.getline(line, 100);
    for (char *ptr = strtok(line, " ,!?"); ptr != NULL; ptr = strtok(NULL, " ,!?"))
    {
        addElement(root, ptr);
    }
    
    printTree(root);
    
    cout << "Enter word: ";
    cin.getline(word, 50);
    
    cout << countWord(root, word);

    return 0;
}
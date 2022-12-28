#include <iostream>
#include <cmath>

using namespace std;


struct Node
{
    int value;
    struct Node* next;
    struct Node* prev;
};


struct NodeIterator
{
    Node* pointer;
};


int isValid(NodeIterator it)
{
    return it.pointer != NULL;
}


void moveNext(NodeIterator &it)
{
    if(isValid(it))
    {
        it.pointer = it.pointer->next;
    }
    return;
}


void movePrev(NodeIterator &it)
{
    if(isValid(it))
    {
        it.pointer = it.pointer->prev;
    }
    return;
}


int getValue(const NodeIterator &it)
{
    if(isValid(it))
    {
        return it.pointer->value;
    }
    return 0;
}


NodeIterator getBegin(Node* head)
{
    NodeIterator temp;
    temp.pointer = head;
    return temp;
}


void push(Node &n, const NodeIterator &it, int value)
{
    if(isValid(it))
    {
        return;
    }
    Node *tmp = new Node;
    tmp->value = value;
    tmp->next = it.pointer->next;
    if(it.pointer->next != NULL)
    {
        it.pointer->next->prev = tmp;
    }
    it.pointer->next = tmp;
}


void push(struct Node** head_ref, int new_data)
{
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));

    new_node->value = new_data;

    new_node->prev = NULL;

    new_node->next = (*head_ref);

    if ((*head_ref) != NULL)
    {
        (*head_ref)->prev = new_node;
    }

    (*head_ref) = new_node;
}


int MaxNode(NodeIterator &it)
{
    int max = getValue(it);
    while(isValid(it))
    {
        if(getValue(it) > max)
        {
            max = getValue(it);
        }
        moveNext(it);
    }
    return max;
}


int main()
{
    struct Node* head = NULL;
    push(&head, 3);
    push(&head, 5);
    push(&head, 2);
    
    NodeIterator it = getBegin(head);
    
    while(isValid(it))
    {
        cout << getValue(it) << ",";
        moveNext(it);
    }
    
    NodeIterator it2 = getBegin(head);
    
    cout << endl;
    cout << MaxNode(it2);

    return 0;
}
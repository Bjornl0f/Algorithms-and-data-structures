#include <iostream>
#include <cmath>

using namespace std;


struct Node
{
    int x;
    int y;
    struct Node* next;
    struct Node* prev;
};


struct NodeIterator
{
    Node* pointer;
};


bool isValid(NodeIterator it, Node* start)
{
    return it.pointer != start;
}


void moveNext(NodeIterator &it, Node* start)
{
    if(isValid(it, start))
    {
        it.pointer = it.pointer->next;
    }
    return;
}


void movePrev(NodeIterator &it, Node* start)
{
    if(isValid(it, start))
    {
        it.pointer = it.pointer->prev;
    }
    return;
}


int getX(const NodeIterator &it, Node* start)
{
    if(isValid(it, start))
    {
        return it.pointer->x;
    }
    return 0;
}


int getY(const NodeIterator &it, Node* start)
{
    if(isValid(it, start))
    {
        return it.pointer->y;
    }
    return 0;
}


NodeIterator getBegin(Node* head)
{
    NodeIterator temp;
    temp.pointer = head;
    return temp;
}


void push(struct Node** start, int x1, int y1)
{
    if (*start == NULL) {
        struct Node* new_node = new Node;
        new_node->x = x1;
        new_node->y = y1;
        new_node->next = new_node->prev = new_node;
        *start = new_node;
        return;
    }
    
    Node* last = (*start)->prev;

    struct Node* new_node = new Node;
    new_node->x = x1;
    new_node->y = y1;

    new_node->next = *start;

    (*start)->prev = new_node;

    new_node->prev = last;

    last->next = new_node;
}


float LongestSegment(NodeIterator &it, Node* start)
{
    float sum = 0.0;
    while(isValid(it, start))
    {
        sum += sqrt((getX(it, start) - it.pointer->next->x) * (getX(it, start) - it.pointer->next->x) + (getY(it, start) - it.pointer->next->y) * (getY(it, start) - it.pointer->next->y));
    }
    sum += sqrt((getX(it, start) - it.pointer->next->x) * (getX(it, start) - it.pointer->next->x) + (getY(it, start) - it.pointer->next->y) * (getY(it, start) - it.pointer->next->y));
    
    return sum;
}


int main()
{
    struct Node* start = NULL;
    
    push(&start, 3, 4);
    push(&start, 5, 4);
    push(&start, 7, 1);
    push(&start, 2, 9);
    
    NodeIterator it = getBegin(start);
    
    while(isValid(it, start))
    {
        cout << "[x = " << getX(it, start) << ", y = " << getY(it, start) << "]   ";
        moveNext(it, start);
    }

    NodeIterator it2 = getBegin(start);
    cout << "The length segment that goes through every dot = " << LongestSegment(it2, start) << endl;

    return 0;
}
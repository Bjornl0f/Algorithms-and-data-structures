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


void output(struct Node* start)
{
    struct Node* temp = start;

    while(temp->next != start)
    {
        cout << "[x = " << temp->x << ", y = " << temp->y << "]   ";
        temp = temp->next;
    }
    cout << "[x = " << temp->x << ", y = " << temp->y << "]   " << endl;
}


float LongestSegment(struct Node* start)
{
    struct Node* temp = start;
    float sum = 0.0;
    while(temp->next != start)
    {
        sum += sqrt((temp->x - temp->next->x) * (temp->x - temp->next->x) + (temp->y - temp->next->y) * (temp->y - temp->next->y));
        temp = temp->next;
    }
    sum += sqrt((temp->x - temp->next->x) * (temp->x - temp->next->x) + (temp->y - temp->next->y) * (temp->y - temp->next->y));

    return sum;
}


int main()
{
    struct Node* start = NULL;
    
    push(&start, 3, 4);
    push(&start, 5, 4);
    push(&start, 7, 1);
    push(&start, 2, 9);
    
    output(start);
    
    cout << "The length segment that goes through every dot = " << LongestSegment(start) << endl;

    return 0;
}
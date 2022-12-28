#include <iostream>
#include <cmath>
using namespace std;


struct TQueueItem
{
    int value;
    TQueueItem *next;
};


struct TQueue
{ 
    TQueueItem *head;
    TQueueItem *tail;
};


TQueue initQueue()
{ 
    TQueue q; 
    q.head = NULL;
    q.tail = NULL;
    return q;
}


int isEmpty(const TQueue&q)
{
    return q.head == NULL;
}


void enQueue(TQueue &q, int value)
{ 
    if(isEmpty(q))
    {
        q.head = new TQueueItem();
        q.head->value = value;
        q.head->next = NULL;
        q.tail = q.head;
    }
    else
    { 
        q.tail->next = new TQueueItem();
        q.tail->next->value = value;
        q.tail->next->next = NULL;
        q.tail = q.tail->next;
    }
}


int deQueue(TQueue &q)
{ 
    if(isEmpty(q))
    {
        return 0;
    }
    else
    { 
        int result = q.head->value;
        q.head = q.head->next;
        if(q.head==NULL)
        {
            q.tail = q.head;
        }
        return result;
    }
}


int countEl(TQueueItem* q, int count){
    if(q == NULL)
    {
        return count;
    }
    else
    { 
        count++;
        return countEl(q->next, count);
    }
}


TQueue input()
{
    struct TQueue q;
    int x, n;
    cout << "Enter number of elements: ";
    cin >> n;
    for(int i = 0; i < n; i++)
    {
        cout << "Enter element №" << i+1 << ": ";
        cin >> x;
        enQueue(q, x);
    }
    return q;
}


void output(TQueue &q)
{
    struct TQueue tmp;
    tmp.head = q.head;
    while(!isEmpty(q))
    {
        cout << q.head->value << " ";
        q.head = q.head->next;
    }
    cout << endl;
    q.head = tmp.head;
}


bool isContained(TQueue &q, int val)
{
    struct TQueue tmp;
    tmp.head = q.head;
    
    while (!isEmpty(q))
    {
        if (q.head->value == val)
        {
            return true;
        }
        q.head = q.head->next;
    }
    q.head = tmp.head;
    
    return false;
}


TQueue UniqueNum(TQueue &q1, TQueue &q2)
{
    struct TQueue q3;
    q3 = initQueue();
    struct TQueue tmp;
    struct TQueue tmp2;
    //struct TQueue tmp3;
    tmp.head = q1.head;
    tmp2.head = q2.head;
    //tmp3.head = q3.head;
    
    while(!isEmpty(q1))
    {
        if(!isContained(q2, q1.head->value))// && !isContained(q3, q1.head->value))
        {
            enQueue(q3, q1.head->value);
        }
        q1.head = q1.head->next;
    }
    q1.head = tmp.head;
    q2.head = tmp2.head;
    //q3.head = tmp3.head;
    
    while(!isEmpty(q2))
    {
        if(!isContained(q1, q2.head->value))// && !isContained(q3, q2.head->value))
        {
            enQueue(q3, q2.head->value);
        }
        q2.head = q2.head->next;
    }
    q1.head = tmp.head;
    q2.head = tmp2.head;
    //q3.head = tmp3.head;
    
    return q3;
}


int main()
{
    TQueue q;
    q = initQueue();
    q = input();
    output(q);
    
    TQueue q2;
    q2 = initQueue();
    q2 = input();
    output(q2);
    
    TQueue q3;
    q3 = UniqueNum(q, q2);
    output(q3);
    
    return 0;
}
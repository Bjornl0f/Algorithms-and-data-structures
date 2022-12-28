#include <stdio.h>
#include <stdlib.h>
#define STACK_OVERFLOW -100
#define STACK_UNDERFLOW -101
#define OUT_OF_MEMORY -102


typedef struct Node
{
    int value;
    struct Node *next;
} Node;


void push(Node **head, int value)
{
    Node *tmp = malloc(sizeof(Node));
    if(tmp == NULL)
    {
        exit(STACK_OVERFLOW);
    }
    tmp->next = *head;
    tmp->value = value;
    *head = tmp;
}


Node* pop(Node **head)
{
    Node *out;
    if((*head) == NULL)
    {
        exit(STACK_UNDERFLOW);
    }
    out = *head;
    *head = (*head)->next;
    return out;
}


int peek(const Node *head)
{
    if(head == NULL)
    {
        exit(STACK_UNDERFLOW);
    }
    return head->value;
}


void printStack(const Node* head)
{
    printf("Stack values: ");
    while(head)
    {
        printf("%d ", head->value);
        head = head->next;
    }
}


size_t getSize(const Node *head)
{
    size_t size = 0;
    while(head)
    {
        size++;
        head = head->next;
    }
    return size;
}


int main()
{
    Node *head = NULL;
    Node *tmp;
    for(int i = 0; i < 10; i++)
    {
        push(&head, i);
    }
    
    printStack(head);

    return 0;
}
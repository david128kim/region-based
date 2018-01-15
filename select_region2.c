#include <pthread.h>
#include <stdio.h>
#include <assert.h>
int Global = 10;
int main() { 
	Global -= 10;
}

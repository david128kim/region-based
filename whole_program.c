#include <assert.h>
#include <pthread.h>
#include <stdio.h>
#include <assert.h>
int Global = 10;
int main() { 
  	Global *= 2;
	Global -= 10;
assert(Global == 10); return 0; }
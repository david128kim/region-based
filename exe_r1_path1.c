#include <pthread.h>
#include <stdio.h>
#include <assert.h>
int Global = 10;
int main(){	if(Global > 0) {
  	Global *= 2;
	}
/* end of branch */
return 0; }
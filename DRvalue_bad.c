#include <pthread.h>
#include <stdio.h>
#include <assert.h>
int Global = 10;
void *Thread1(void *x) {
  Global *= 2;
  return x;
}
void *Thread2(void *y) {
  Global -= 10;
  return y;
}
int main() {
  pthread_t t1, t2;

  pthread_create(&t1, NULL, Thread1, NULL);
  pthread_create(&t2, NULL, Thread2, NULL);

  pthread_join(t1, NULL);
  pthread_join(t2, NULL);
  
  printf("%d\n", Global);
  return Global;
}

# C Skill — Examples
## 1. Safe Memory Allocation
```c
#include <stdlib.h>
#include <stdio.h>
int *arr = malloc(10 * sizeof(int));
if (!arr) {
perror("malloc failed");
exit(1);
}
free(arr);
```
## 2. Lint with clang-tidy
```text
clang-tidy myfile.c --
```
## 3. Static Analysis with cppcheck
```sh
cppcheck myfile.c
```

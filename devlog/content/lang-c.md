# C

A low-level, manually-memory-managed language that underlies most operating systems and runtimes, minimal abstraction between your code and the machine.

## Setup

```bash
gcc --version    # or clang --version
```

## Compiling

```bash
gcc main.c -o main -Wall -Wextra
./main
```

`-Wall -Wextra` enables warnings that catch a large share of real bugs (uninitialized variables, signed/unsigned mismatches), always compile with them on.

## Core syntax

```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main(void) {
    int count = 0;
    char name[] = "Ada";

    printf("Hello, %s! Count: %d\n", name, count);

    int nums[3] = {1, 2, 3};
    for (int i = 0; i < 3; i++) {
        printf("%d\n", nums[i] * 2);
    }
    return 0;
}
```

## Pointers and manual memory management

```c
#include <stdlib.h>

int *make_array(int size) {
    int *arr = malloc(size * sizeof(int));
    if (arr == NULL) return NULL; // always check malloc's return
    for (int i = 0; i < size; i++) arr[i] = i * i;
    return arr;
}

int main(void) {
    int *arr = make_array(5);
    if (arr) {
        printf("%d\n", arr[2]);
        free(arr); // you own it, you free it, exactly once
    }
    return 0;
}
```

There's no garbage collector, every `malloc` needs exactly one matching `free`. Freeing twice, forgetting to free, or using memory after freeing it are the classic C bug categories; tools like **Valgrind** or `-fsanitize=address` catch these during development.

## Structs

```c
typedef struct {
    char name[32];
    int age;
} Person;

Person p = { "Ada", 30 };
printf("%s is %d\n", p.name, p.age);
```

## Header files

```c
// math_utils.h
#ifndef MATH_UTILS_H
#define MATH_UTILS_H
int add(int a, int b);
#endif
```

The include guard (`#ifndef`/`#define`/`#endif`) prevents a header being processed twice if it's included from multiple files, which would otherwise cause "redefinition" errors.

## Common gotchas

- Array bounds are **not** checked, reading/writing past an array's end is undefined behavior, not a caught exception, and can corrupt unrelated memory silently.
- Strings are just `char` arrays terminated by a `\0` byte, forgetting to size a buffer for that extra byte is a classic off-by-one bug.
- Comparing floats with `==` is unreliable due to representation error, compare against a small epsilon instead (`fabs(a - b) < 1e-9`).

See also: [C++](lang-cpp.html), which extends C with classes, templates, and RAII-based memory management.

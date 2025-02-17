#include <cstdio>

// kernel definition
__global__ void HelloWorld() {
    printf("Hello, World!\n");
}

int main() {
    const auto nBlock = 1;
    const auto nThread = 1;
    HelloWorld<<< nBlock, nThread >>> ();
    return 0;
}
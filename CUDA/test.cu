/* * @file_name HelloWorld.cu  后缀名称.cu */
#include <stdio.h>
#include <cuda_runtime.h>
//头文件

//核函数声明，前面的关键字__global__

__global__ void kernel( void ) {
}

int main1( void ) {
    //核函数的调用，注意<<<1,1>>>，第一个1，代表线程格里只有一个线程块；第二个1，代表一个线程块里只有一个线程。
    kernel<<<1,1>>>();
    printf( "Hello, World!\n" );
    return 0;
}

__global__ void add( int a, int b, int *c ) {
    *c = a + b;
}


int main( void ) {
    int c;
    int *dev_c;
    //cudaMalloc()
    cudaMalloc( (void**)&dev_c, sizeof(int) );
    //核函数执行
    add<<<1,1>>>( 2, 7, dev_c );
    //cudaMemcpy()
    cudaMemcpy( &c, dev_c, sizeof(int),cudaMemcpyDeviceToHost ) ;
    printf( "2 + 7 = %d\n", c );
    //cudaFree()
    cudaFree( dev_c );

    return 0;
}
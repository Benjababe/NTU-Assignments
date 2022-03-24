#include <stdio.h>

__global__ void hello_gpu(void)
{
    if (blockIdx.x == 0 && threadIdx.x > 3)
        return;
    printf("Hello from GPU%d[%d]!\n", blockIdx.x + 1, threadIdx.x);
}

int main()
{
    printf("Hello from CPU!\n");
    hello_gpu<<<2, 6>>>();

    cudaDeviceSynchronize();
    return 0;
}
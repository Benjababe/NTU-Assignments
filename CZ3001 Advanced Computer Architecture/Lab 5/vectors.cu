#include <stdio.h>

const int N = 4;

__global__ void vector_add(int *h_c, int *h_a, int *h_b)
{
    int i = threadIdx.x;
    h_c[i] = h_a[i] + h_b[i];
}

__global__ void vector_dot_product(int *d_c, int *d_a, int *d_b)
{
    __shared__ int tmp[N];
    int i = threadIdx.x;
    tmp[i] = d_a[i] * d_b[i];

    __syncthreads();

    // only thread 0 sums up multiplication values
    if (i == 0)
    {
        for (int j = 0; j < N; j++)
            *d_c += tmp[j];
    }
}

int main()
{
    int a[N] = {22, 13, 16, 5},
        b[N] = {5, 22, 17, 37},
        cAdd[N],
        cDot = 0;

    // address pointers for vram
    int *d_a, *d_b, *d_c, *d_c_dot;

    // allocate video memory for values to be passed in
    cudaMalloc((void **)&d_a, sizeof(int) * N);
    cudaMalloc((void **)&d_b, sizeof(int) * N);
    cudaMalloc((void **)&d_c, sizeof(int) * N);

    // pass in our declared variables into vram
    cudaMemcpy(d_a, a, sizeof(int) * N, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, b, sizeof(int) * N, cudaMemcpyHostToDevice);
    cudaMemcpy(d_c, cAdd, sizeof(int) * N, cudaMemcpyHostToDevice);

    // vector addition is done in 1 block
    vector_add<<<1, N>>>(d_c, d_a, d_b);
    cudaDeviceSynchronize();

    // copy back the added matrix into main memory
    cudaMemcpy(cAdd, d_c, sizeof(int) * N, cudaMemcpyDeviceToHost);
    cudaFree(d_c);

    printf("[Addition]\tOutput of C: { %d %d %d %d }\n", cAdd[0], cAdd[1], cAdd[2], cAdd[3]);

    // allocation video memory for our dot product sum
    cudaMalloc((void **)&d_c_dot, sizeof(int));
    cudaMemcpy(d_c_dot, &cDot, sizeof(int), cudaMemcpyHostToDevice);

    // vector dot product is done in 1 block as well
    vector_dot_product<<<1, N>>>(d_c, d_a, d_b);
    cudaDeviceSynchronize();

    // copy back the final sum back to main memory
    cudaMemcpy(&cDot, d_c, sizeof(int), cudaMemcpyDeviceToHost);
    cudaFree(d_c);

    printf("[Dot Product]\tOutput of C: %d", cDot);

    return 0;
}
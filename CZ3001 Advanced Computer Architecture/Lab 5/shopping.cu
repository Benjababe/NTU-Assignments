#include <stdio.h>

const int M = 4,
          N = 7;

// d_sales will be treated as 1D array because I'm too lazy to figure out what is a pitch for cudaMemcpy2D
__global__ void calc_sales(float *d_sales_figure, float *d_sales, float *d_prices)
{
    __shared__ float tmp[N * M];
    int i = threadIdx.x;

    tmp[i] = d_sales[i] * d_prices[i / N];
    __syncthreads();

    if (i == 0)
    {
        for (int j = 0; j < (M * N); j++)
            *d_sales_figure += tmp[j];
    }
}

int main()
{
    float sales[M][N] = {
        {3, 2, 0, 3, 4, 10, 8},  // HD
        {5, 4, 3, 5, 5, 13, 11}, // EP
        {2, 5, 3, 4, 5, 21, 15}, // SP
        {0, 1, 1, 4, 3, 16, 8}   // TD
    };

    float sales_figure = 0;
    float prices[M] = {29.99, 14.99, 9.99, 24.99};
    float *d_sales, *d_prices, *d_sales_figure;

    cudaMalloc((void **)&d_sales, sizeof(float) * M * N);
    cudaMalloc((void **)&d_prices, sizeof(float) * M);
    cudaMalloc((void **)&d_sales_figure, sizeof(float));

    cudaMemcpy(d_sales, sales, sizeof(float) * M * N, cudaMemcpyHostToDevice);
    cudaMemcpy(d_prices, prices, sizeof(float) * M, cudaMemcpyHostToDevice);
    cudaMemcpy(d_sales_figure, &sales_figure, sizeof(float), cudaMemcpyHostToDevice);

    calc_sales<<<1, M * N>>>(d_sales_figure, d_sales, d_prices);
    cudaDeviceSynchronize();

    cudaMemcpy(&sales_figure, d_sales_figure, sizeof(float), cudaMemcpyDeviceToHost);

    cudaFree(d_sales);
    cudaFree(d_prices);
    cudaFree(d_sales_figure);

    printf("Total sales: $%.2f\n", sales_figure);
    return 0;
}
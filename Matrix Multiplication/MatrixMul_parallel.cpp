#include <stdio.h>
#include <Windows.h>
#include <pthread.h>
#include <time.h>

#define MAXTHREADS 10
int N = 500;
long nelems_per_thread;
int* matrix1 = (int*)malloc((N * N) * sizeof(int));
int* matrix2 = (int*)malloc((N * N) * sizeof(int));
int* matrix3 = (int*)malloc((N * N) * sizeof(int));
int* matrix4 = (int*)malloc((N * N) * sizeof(int));
void printMatrix(int* m, int size);
void* pmulti(void* arg);

int main()
{
	clock_t start1, end1, start2, end2;
	//N = atoi(argv[2]);
	/*matrix initialization*/
	/*if (NULL==matrix1)
		exit(-1);
	if (NULL==matrix2)
		exit(-1);
	if (NULL==matrix3)
		exit(-1);*/
	srand((unsigned)time(NULL));
	int a, b;
	for (a = 0; a < N; a++)
		for (b = 0; b < N; b++)
		{
			matrix1[a * N + b] = rand() % 11;
			matrix2[a * N + b] = rand() % 11;
			matrix3[a * N + b] = 0;
			matrix4[a * N + b] = 0;
		}
	
	/*---------------------Sequential matrix multiplication---------------------*/
	start1 = clock();
	/*(ijk)*/
	int k, i, j, tmp;
	for (i = 0; i < N; i++)
	{
		for (j = 0; j < N; j++)
		{
			tmp = 0;
			for (k = 0; k < N; k++)
				tmp += matrix1[i * N + k] * matrix2[k * N + j];
			matrix3[i * N + j] = tmp;
		}
	}
	end1 = clock();
	/*(kij)*/
	/*int k, i, j, tmp;
	for (k = 0; k < N; k++) 
	{
		for (i = 0; i < N; i++)
		{
			tmp = matrix1[i * N + k];
			for (j = 0; j < N; j++)
				matrix3[i * N + j] += tmp * matrix2[k * N + j];
		}
	}*/


	/*printf("A:\n");
	printMatrix(matrix1, N);
	printf("B:\n");
	printMatrix(matrix2, N);
	printf("------Sequential matrix multiplication------\n");
	printf("C:\n");
	printMatrix(matrix3, N);*/
	/*---------------------Sequential matrix multiplication---------------------*/


	/*---------------------Parallel matrix multiplication---------------------*/
	start2 = clock();
	int nthreads = 4;
	nelems_per_thread = N * N / nthreads;
	int myid[MAXTHREADS];
	pthread_t tid[MAXTHREADS];
	for (i = 0; i < nthreads; i++) {
		myid[i] = i;
		pthread_create(&tid[i], NULL, pmulti, &myid[i]);
	}
	for (i = 0; i < nthreads; i++)
		pthread_join(tid[i], NULL);
	end2 = clock();

	/*printf("------Parallel matrix multiplication------\n");
	printf("D:\n");
	printMatrix(matrix4, N);*/
	/*---------------------Parallel matrix multiplication---------------------*/
	double time1 = (double(end1) - double(start1)) / CLOCKS_PER_SEC;
	printf("Sequential multiplication time: %3f\n", time1);
	double time2 = (double(end2) - double(start2)) / CLOCKS_PER_SEC;
	printf("Parallel multiplication time: %3f\n", time2);

    bool equal = memcmp(matrix3, matrix4, N * N * sizeof(int)) == 0;
    printf("Matrices are %s\n", equal ? "equal" : "not equal");

	free(matrix1);
	free(matrix2);
	free(matrix3);
	free(matrix4);
	exit(0);
}

void printMatrix(int *m, int size)
{
	for (int i = 0; i < size; i++)
	{
		for (int j = 0; j < size; j++)
			printf("%d\t", m[i * size + j]);
		printf("\n");
	}
}

void* pmulti(void* arg)
{
	int i, j, k, n, tmp;
	int tid = *((int*)arg);
	int starti = (tid / 2) * N / 2;
	int endi = starti + N / 2;
	int startj = (tid % 2) * N / 2;
	int endj = startj + N / 2;
	for (n = 0; n < 2; n++)
	{
		for (i = starti; i < endi; i++)
		{
			for (j = startj; j < endj; j++)
			{
				tmp = 0;
				for (k = n * N / 2; k < (n + 1) * N / 2; k++)
					tmp += matrix1[i * N + k] * matrix2[k * N + j];
				matrix4[i * N + j] += tmp;
			}
		}
	}
	return NULL;
}

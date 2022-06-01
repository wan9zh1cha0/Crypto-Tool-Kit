import math
import time
import random
import tools

#Miller Rabin
def check_prime(x,p):
    if(tools.fast_power(x,p-1,p)!=1):
        #print(fast_pow(x,p-1,p))
        #print('here')
        return 0
    y=p-1
    while y&1==0:   #当y为偶数时循环
        y>>=1
        z=tools.fast_power(x,y,p)
        if z!=1 and z!=p-1:
            return 0
        if z==p-1:
            return 1
    return 1

def Pollard_rho(N):
    #c=random.randint(1,10)
    #y=x=random.randint(1,10)
    #print(x,y,c)
    x=y=1
    c=5
    i,k=1,2
    while True:
        i+=1
        x=(tools.fast_mul(x,x,N)+c)%N
        d=math.gcd(abs(x-y),N)
        if(d!=1):
            print('x =',x)
            print('y =',y)
            return d
        if(i==k):
            y=x
            k<<=1

start = time.time()    #获取当前时间
d3=Pollard_rho(135107421725854039500365153)
#if (check_prime(2,d3)==1 and check_prime(2,d3)==1 and check_prime(2,d3)==1 and
#    check_prime(2,d3)==1 and check_prime(2,d3)==1 and check_prime(2,d3)==1 and check_prime(2,d1)==1):
if (check_prime(2,d3)==1 and check_prime(3,d3)==1 and check_prime(7,d3)==1 and
    check_prime(61,d3)==1 and check_prime(24251,d3)==1 and d3!=46856248255981):
    print('d3 =',d3)
print('Time Used:', time.time() - start) #输出所用时间

start = time.time()    #获取当前时间
d4=135107421725854039500365153//d3
if (check_prime(2,d4)==1 and check_prime(3,d4)==1 and check_prime(7,d4)==1 and
    check_prime(61,d4)==1 and check_prime(24251,d4)==1 and d4!=46856248255981): 
    print('d4 =',d4)
else:
    d4=Pollard_rho(d4)
    print('left =',d4)
print('Time Used:', time.time() - start) #输出所用时间

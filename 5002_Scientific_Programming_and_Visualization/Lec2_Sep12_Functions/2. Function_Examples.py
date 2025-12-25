# @author: Junwei Liu

# def function_name():
#    1st block lines
#    2nd block lines
#    ...

# def function_name(1st_argu, 2nd_argu, ...):
#    1st block lines
#    2nd block lines
#    ...


# def function_name(1st_argu, 2nd_argu, ...):
#    1st block lines
#    2nd block lines
#    ...
#    return var1, var2, ...

########################################################################
#Example 1: the simplest function with a return value
def my_sum(a,b):
    s = a + b
    return s

a = 1
b = 2
s = my_sum(a,b);
print(a,'+',b,'=', s)

######################################################################
# #Example 2: multiple returns
a = 1
b = 3

def my_sum_product(a,b):
    s = a + b
    p = a * b
    a = 4
    b = 10
    return s,p,a,b

#
r1,r2,r3,r4=my_sum_product(a,b)
print(a,'+',b,'=', r1)
print(a,'*',b,'=', r2)

#######################################################################
# Example 3: test the function names, you can overwrite the existing function
# However, do not do it
def print(a,b):
    # print(a+b,a*b)
    return a+b,a*b

r2=print(1,3)
print(r2)

#########################################################################
#Example 4: Optional arguments and default value
def my_sum(a,b=0,c=0):
    s=a+b+c
    return s
a='a'
b='b'
c='c'
s=my_sum(a,b,c);
print(a,'+',b,'+',c,'=', s)

#######################################################################
# Example 5: better to confirm the variable type and use return as the end
def my_sum(a,b,c=0):
    if (type(a)!=int and type(a)!=float) or (type(b)!=int and type(b)!=float):
        print("your input are not numbers")
        return
    s=a+b+c
    print('run successfully')
    return s

a=1
b=3
c=10
s=my_sum(a,b);
print(a,'+',b,'=', s)
s2=my_sum(a,b,c);
print(a,'+',b,'+',c,'=', s2)

b=my_sum(1,2)
c=my_sum(1,'a')
if (type(c)==int):
    my_sum(1,2)

print('It is done')

#########################################################################
# Example 6: test the life of a variable
def my_sum_test(a,b): ##A4, A5
    c=a+b  #A6
    print("c in the function: ",c) #A6
    a=100 #A4
    print("a in the function: ",a) #A4
    print("d in the function: ",d) #A0
    # d=10  ## can we define it here?? #A7
    
    return c #A6

d=1000 #A0
a=1  #A1
b=3  #A2
c=10 #A3

print("a in main code: ",a) #A1
my_sum_test(a,b)

print("d in main code: ",d) #A0
print("c in the main code: ", c) #A3
print("a in main code after calling the function: ",a) #A1



########################################################################
#Example 7: pass the parameter with the keyword
def my_sum_scale(a=0,b=0,third=0,scaler=1):
    print('a=',a,'b=',b,'third=',third,'scaler=',scaler)
    s=(a+b+third)*scaler
    return s

print('my_sum_scale(1,2)=',my_sum_scale(1,2))
print('my_sum_scale(1,2,3)=',my_sum_scale(1,2,3))
print('my_sum_scale(1,2,3,4)=',my_sum_scale(1,2,3,4))
my_sum_scale(1,2,third=3,scaler=4)
my_sum_scale(1,2,scaler=4,third=3)


#######################################################################
# Example 8: test the recursive functions
def my_recursive_function(n): 
    print('n=',n)
    if n == 0:
        return 0
    if n == 1:
        return 1
    return my_recursive_function(n - 1) + my_recursive_function(n - 2)

for ni in range(10):
    print(my_recursive_function(ni))

def fibonacci(n):
    current, nextone = 0, 1
    for i in range(n):
        current, nextone = nextone, current + nextone
    return current

for ni in range(10):
    print(fibonacci(ni))


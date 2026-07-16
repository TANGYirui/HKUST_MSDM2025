%Newton's method in 1D with stopping criterion
x0=2;
eps=0.001;
n=1
x1=x0-(sin(x0)-1)/(cos(x0))
while abs(x1-x0)>=eps
    n=n+1
    x0=x1;
    x1=x0-(sin(x0)-1)/(cos(x0))
end;
%Newton's method in 1D
x0=2;
n=6;
for i=1:n
    x1=x0-(sin(x0)-1)/(cos(x0))
    x0=x1;
end;
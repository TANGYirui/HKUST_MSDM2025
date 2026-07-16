% Q1(2)

f = @(x) 1 - 4*(exp(x)-1)*cos(x) + 2*x^2 + cos(2*x);
df = @(x) -4*(exp(x)*cos(x) - (exp(x)-1)*sin(x)) + 4*x - 2*sin(2*x);

x_old = 0.6; 
tol = 1e-5;  % accuracy
max_iter = 100; 
iter = 0;

while iter < max_iter
    fx = f(x_old);
    dfx = df(x_old);
    
    x_new = x_old - fx/dfx; % Newton
    
    if abs(x_new - x_old) < tol
        break;
    end
    
    x_old = x_new;
    iter = iter + 1;
    fprintf('Iteration %d: x = %.6f\n', iter, x_new);
end

fprintf('Final Result: %.6f (after %d iterations)\n\n', x_new, iter);


% Q4
x = [1.0700; 1.2270; 1.5410; 1.8550; 2.4830; 2.7970];
y = [1.8547; 1.9347; 2.1013; 2.2613; 2.5880; 2.7480];

A = [x.^2, x, ones(size(x))];
[U, S, V] = svd(A, 'econ');
coeffs = V * (S \ (U' * y));

fprintf('The polynomial is: y = %.6fx^2 + %.6fx + %.6f\n', ...
        coeffs(1), coeffs(2), coeffs(3));
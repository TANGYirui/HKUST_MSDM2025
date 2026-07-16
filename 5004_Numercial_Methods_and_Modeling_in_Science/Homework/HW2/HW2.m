% Homework 2 Part I - Question 2

A = [4 1 1 1;
     1 4 1 1;
     1 1 4 1;
     1 1 1 4];
b = [1; 1; 1; 1];

n = length(b);
x0 = zeros(n, 1);
tol = 1e-5;     
max_iter = 1000; 

%% (1) Jacobi Method
x_jac = x0;
iter_jac = 0;
while iter_jac < max_iter
    x_new = zeros(n, 1);
    for i = 1:n
        sum_val = b(i) - A(i, [1:i-1, i+1:n]) * x_jac([1:i-1, i+1:n]);
        x_new(i) = sum_val / A(i,i);
    end

    if norm(x_new - x_jac, inf) <= tol
        x_jac = x_new;
        break;
    end
    x_jac = x_new;
    iter_jac = iter_jac + 1;
end

fprintf('--- Jacobi Method ---\n');
fprintf('Iterations: %d\n', iter_jac);
disp('Solution:'); disp(x_jac);

%% (2) SOR Method (omega = 1.3)
omega = 1.3;
x_sor = x0;
iter_sor = 0;
while iter_sor < max_iter
    x_old = x_sor;
    for i = 1:n
        sum1 = A(i, 1:i-1) * x_sor(1:i-1); 
        sum2 = A(i, i+1:n) * x_old(i+1:n); 
        
        x_gs = (b(i) - sum1 - sum2) / A(i,i);
        
        x_sor(i) = (1 - omega) * x_old(i) + omega * x_gs;
    end
    
    if norm(x_sor - x_old, inf) <= tol
        break;
    end
    iter_sor = iter_sor + 1;
end

fprintf('--- SOR Method (omega = 1.3) ---\n');
fprintf('Iterations: %d\n', iter_sor);
disp('Solution:'); disp(x_sor);


% Homework 2 Part II - Question 3
f = @(x) exp(x)./x;
df_exact = (2*exp(2) - exp(2))/(2^2); 

x0 = 2;
h_values = 0.1 ./ (2.^(0:10)); 
errors = zeros(size(h_values));

fprintf('%-10s %-15s %-15s %-10s\n', 'h', 'Approx', 'Error', 'Ratio');

for i = 1:length(h_values)
    h = h_values(i);
    
    df_approx = (f(x0 + h) - f(x0 - h)) / (2*h);
    
    errors(i) = abs(df_approx - df_exact);
    
    if i > 1
        ratio = errors(i-1) / errors(i);
        fprintf('%.4e   %.10f   %.4e   %.2f\n', h, df_approx, errors(i), ratio);
    else
        fprintf('%.4e   %.10f   %.4e   ---\n', h, df_approx, errors(i));
    end
end

% plot
figure;
loglog(h_values, errors, '-o', 'LineWidth', 2);
grid on;
xlabel('Step size h'); ylabel('Absolute Error');
title('Convergence of Central Difference (Slope should be 2)');

p = polyfit(log(h_values), log(errors), 1);
fprintf('\nCalculated Convergence Order: %.4f\n', p(1));


% Homework 2 Part II - Question 4
h = 1/128;
t = 2:h:4;
N = length(t);

% (1) Forward Euler Method
y_fe = zeros(1, N);
y_fe(1) = 2; 

for n = 1:N-1
    f_n = (2/t(n)^2) * (t(n)*y_fe(n) - 2*y_fe(n)^2);
    y_fe(n+1) = y_fe(n) + h * f_n;
end

% (2) Backward Euler Method
y_be = zeros(1, N);
y_be(1) = 2;

for n = 1:N-1
    tn1 = t(n+1);
    a = 4 * h / (tn1^2);
    b = 1 - (2 * h / tn1);
    c = -y_be(n);
    
    y_be(n+1) = (-b + sqrt(b^2 - 4*a*c)) / (2*a);
end

% plot
plot(t, y_fe, 'r--', t, y_be, 'b-', 'LineWidth', 1.5);
legend('Forward Euler', 'Backward Euler');
xlabel('t'); ylabel('y(t)');
title('Numerical Solution of ODE');
grid on;
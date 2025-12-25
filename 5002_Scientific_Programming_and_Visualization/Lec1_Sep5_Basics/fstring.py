a=2
b=10
c='string'
print(f'{a:<20.2f}: {b:>10}:') # < left aligned
print(f'{a:>20.2f}: {c:<10}:') # > right aligned
print(f'{a:^20.2f}:') #middle aligned
print(f'{a:T^20.2f}:') #middle aligned with T as fill character
print(f'{a:_^20.2f}:') #middle aligned with _ as fill character
print(f'Test an interesting usage: {a + b = }')


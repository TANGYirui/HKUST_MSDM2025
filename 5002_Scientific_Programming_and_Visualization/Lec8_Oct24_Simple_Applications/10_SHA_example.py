from hashlib import sha256
# from hashlib import sha512
#data = input('Enter plaintext data: ')
data = 'abbbbbbbbbbbbbbbbbbbbbbbbbbbdfjosjfdoisajfodwajfogesgjegjoeaijgoewrjgoewjrg9oibbbbbbbbbbbbc'
data = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab'
output = sha256(data.encode('utf-8'))

val=output.hexdigest();
int_val=int(val,16)
binary_val=bin(int_val)
print(val)
# print(int_val)
# print(binary_val)

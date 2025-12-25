
h = float(input("Enter the height:"))
while h < 0:
    print("You need to input a POSITIVE number")
    h = float(input("Enter the height:"))

t = float(input("Enter the time:"))   
while t < 0:
    print("You need to input a POSITIVE number")
    t = float(input("Enter the time:"))

s = h - 9.81 * t**2 / 2

print("\nThe initial height of the ball is ", h, " meters")
if s < 0:
    print("Before", t, " seconds, the ball has already hit the ground.")
else:
    print("After", t, " seconds, the height is ",s, " meters")
    
    
    





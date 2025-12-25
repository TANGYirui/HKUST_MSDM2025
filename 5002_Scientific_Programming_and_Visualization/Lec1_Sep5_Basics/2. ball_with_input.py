
h = float(input("Enter the height:")) # if the input is not a number, it will raise an error
t = float(input("Enter the time:")) # if t = int(input("Enter the time:")) then it will raise an error

s = h-9.81*t**2/2 # the h and t must be float, otherwise it will raise an error
# becareful about the ending type, if h is int, then s will be int, which is not what we want 

print("\nThe initial height of the ball is ", h, " meters")
print("After", t, " seconds, the height is ",s, " meters")







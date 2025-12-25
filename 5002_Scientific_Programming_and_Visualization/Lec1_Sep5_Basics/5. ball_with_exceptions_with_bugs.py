#My first complete code

#get the height of the ball h, and the falling time t

input_right = 0
count_num = 0
while input_right == 0:
    h_tmp = input("Enter the height:")
    try:
        h_val = float(h_tmp)
        input_right = 1
    except ValueError:
        print("Your input should be a number")
    count_num = count_num + 1
    
    if input_right == 1 and h_val < 0:
        print("Your input should be a POSITIVE number")
        input_right = 0
    
    if count_num > 3:
        h_val = 10
        print("You are so stupid! I have to stop you and set the initial height as 10 meters")
        break
h = h_val

input_right = 0
count_num = 0
while input_right == 0:
    t_tmp = input("Enter the time:")
    try:
        t_val = float(t_tmp)
        input_right = 1
    except ValueError:
        print("Your input should be a number")
    count_num = count_num + 1
    
    if input_right == 1 and t_val < 0:
        print("Your input should be a POSITIVE number")
        input_right = 0
    
    if count_num > 3:
        t_val = 1
        print("You are so stupid! I have to stop you and set the time as 1 second")
        break

t = t_val


    
#do the calculations
s = h - 9.81 * t**2 / 2


#print out the results
print("\nThe initial height of the ball is ", h, " meters")
if s < 0:
    print("Before", t, " seconds, the ball has already hitted the groud.")
else:
    print("After", t, " seconds, the height is ",s, " meters")





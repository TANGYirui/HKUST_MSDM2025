import datetime
TODAY = str(datetime.date.today())

def my_copyright():
    print("*****************************************")
    print("***  programmed by LIU for MSDM5002   ***")
    print("-----------------------------------------")
    print("***  You can use it as you like, but  ***")
    print("***  there might be many bugs. If you ***")
    print("***  find some bugs, please send them ***")
    print("***  to liuj@ust.hk.                  ***")
    print("*****************************************")

def my_copyright2(date):
    print("*****************************************")
    print("***  programmed by XXX for MSDM5002   ***")
    print("***        date:",   date, "          ***")
    print("***-----------------------------------***")
    print("***  You can use it as you like, but  ***")
    print("***  there might be many bugs. If you ***")
    print("***  find some bugs, please send them ***")
    print("***  to XXX@ust.hk.                   ***")
    print("*****************************************")

def my_copyright3(name='J. LIU',email='liuj@ust.hk',date=TODAY):
    #how can we make it neat since Name and email may have flexibel length?
    print("******************************************")
    print("***  programmed by",name,"for MSDM5002 ***")
    print("***         date:",   date, "          ***")
    print("***------------------------------------***")
    print("***  You can use it as you like, but   ***")
    print("***  there might be many bugs. If you  ***")
    print("***  find some bugs, please send them  ***")
    print("***  to ",    email,"                  ***")
    print("******************************************")

def my_copyright4(name='J. LIU',email='liuj@ust.hk',date=TODAY):
    len_name=len(name)
    str_len=len_name+27
    
    str_star='*'*(5+str_len+5)
    str_slash='***--'+'-'*str_len+'--***'

    print(str_star)
    print("***  Programmed by "+name+" for MSDM5002  ***")
    str_date="date: "+date
    print("***  "+" "*int((str_len-len(str_date))/2)+str_date+" "*int((str_len-len(str_date))/2+0.5)+"  ***")
    print(str_slash)
    
    
    statements='You can use it as you like, but there might be ' + \
        'many bugs. If you find some bugs, please send them to'
    statements=statements+' "'+email+'"'

    # ### you may improve this part
    start_point = 0
    end_point = start_point + str_len + 1
    while start_point < len(statements):        
        print("***  " + statements[start_point:end_point] + " ***")     
        start_point = end_point
        end_point = start_point + str_len + 1
       
    print(str_star)  

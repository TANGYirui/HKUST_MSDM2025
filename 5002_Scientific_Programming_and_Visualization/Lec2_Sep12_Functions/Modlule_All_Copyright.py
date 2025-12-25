import datetime
TODAY = str(datetime.date.today())

def my_copyright():
    print("*****************************************")
    print("***  programmed by XXX for MSDM5002   ***")
    print("-----------------------------------------")
    print("***  You can use it as you like, but  ***")
    print("***  there might be many bugs. If you ***")
    print("***  find some bugs, please send them ***")
    print("***  to XXX@ust.hk.                   ***")
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

### This will be imported by import *
print('I can write everything here, outside main')
a=100
### This cannot be imported by import *, but can be imported by import _b or use it by XXX._b
_b=1000

if __name__ == '__main__':
    print('I can write everything here, inside main')
    a=1
    print(a)
# my_copyright()
# my_copyright2('11/09/2020')
# my_copyright3('J. Liu', 'liuj@ust.hk','11/09/2020')
# my_copyright4('J Liu', 'liuj@ust.hk','11/09/2020')

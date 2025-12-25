#################################################################   
#### Example 1: Underscore in import
#### try import Usage_Underscore
#################################################################

def func1(x):
    print("you are testing function 1, your input is ", x**1)
    
def func2(x):
    print("you are testing function 2, your input is ", x**2)


## According to PEP8, single leading underscore _var is intended for 
## internal use. from M import * doesn’t import objects whose names 
## start with an underscore.
## this function will not be imported using conventional way, while you
## still import it explicitly like 
## from test_modules import _fun3, you can directly use the func3()
## or import test_modules, you can access is through test_modules._func3()
def _func3(x):
    print("you are testing function 3, your input is ", x**3)

external_var = 'external'
_internal_var = 'internal'

print('Everything here will run when this file is imported')
b=2
print(b)

def func__name__():
	print(__name__)


## https://www.tutorialsteacher.com/python/main-in-python
if __name__ == '__main__':
    print('The codes here will only run as a main function')
    a=1
    print(a)
    

print('Simiarly, everything here will also run when this file is imported')
c=3
print(c)
 

#################################################################   
#### Example 2: Usage of double Underscore in class
#################################################################
class Time:
    def __init__(self, year, month):
        self.year = year
        self._month = month
        self.__day = 1
        
    
    def get_day(self):
        return self.__day

    @property ## make the function be called like an attribute
    def day_property(self):
        return self.__day
    
    def __str__(self):
        return f"year: {self.year}, month: {self._month}, day: {self.__day}"

time = Time(2020, 7)
# print(dir(time))

print(time.year)
print(time._month)
# print(time.__day)  ## this will give wrong warning
print(time._Time__day)
# print(time.get_day())
# print(time.day_property)


class TimeSubclass(Time):
    def __init__(self, year, month, day):
        
        # The super() function is used to give access to
        # methods and properties of a parent or sibling class.
        # The super() function returns an object 
        # that represents the parent class.
        # super().__init__(year, month)
        self.year = year
        self._month = month
        self.__day = day  ### this is differetn _Time__day in the parent class
        
time_subclass = TimeSubclass(2025, 9, 19)
# # print(dir(time_subclass))

# print(time_subclass._TimeSubclass__day)
# print(time_subclass._Time__day)  ##It cannot be overwritten


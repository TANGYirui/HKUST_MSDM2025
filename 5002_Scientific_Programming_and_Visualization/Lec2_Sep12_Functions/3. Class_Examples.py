# ## -*- coding: utf-8 -*-
# #"""
# #
# #@author: Junwei Liu
# #"""
# #

# ########################################################################
# #Example of a class

import datetime # we will use this for date objects

class Person:
    '''
    Define a class of Person
    '''
    def __init__(self, name='', surname='', birthdate=datetime.date(2021, 9, 1), address='HKUST', telephone='', email=''):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate

        self.address = address
        self.telephone = telephone
        self.email = email
    

    def age(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year

        if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
            age -= 1

        return age

# # # #######################################################################

class Person2:
    '''
    Define a class of Person
    '''
    def __init__(self):
        self.name = 'Name'
        self.surname = 'Surname'
        self.birthdate = datetime.date(2021, 9, 1)

        self.address = 'HKUST'
        self.telephone = '2358XXXX'
        self.email = 'XXX@ust.hk'
    

    def age(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year

        if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
            age -= 1

        return age

Jane = Person(
    "Jane",
    "Doe",
    datetime.date(1992, 3, 12), # year, month, day
    "No. 12 Short Street, Greenville",
    "555 456 0987",
    "jane.doe@example.com"
)

# Jack = Person(
#     "Jack",
#     "Doe",
#     datetime.date(1992, 3, 12), # year, month, day
#     "No. 12 Short Street, Greenville",
#     "555 456 0923",
#     "jack.doe@example.com"
# )

Jack = Person2()
Jack.name='Jack'
Jack.surname='Jack'
Jack.birthdate=datetime.date(1992, 3, 12)
Jack.address="No. 12 Short Street, Greenville"
Jack.telephone="555 456 0987"
Jack.email="jack.doe@example.com"

### You can even add a new attribute outside the class
# Jack.new_attr='Anything'


class Person3:
    '''
    Define a class of Person
    '''
    def age(self):
        today = datetime.date.today()
        age = today.year - self.birthdate.year

        if today < datetime.date(today.year, self.birthdate.month, self.birthdate.day):
            age -= 1

        return age

Jack = Person3()
Jack.name='Jack'
Jack.surname='Jack'
Jack.birthdate=datetime.date(1992, 3, 12)
Jack.address="No. 12 Short Street, Greenville"
Jack.telephone="555 456 0987"
Jack.email="jack.doe@example.com"



# # print(type(Jack))
# # print(Jack.name)
# # print(getattr(Jack,'name'))
# # print(Jack.email)
# # print(Jack.age())

# ### get all the attribute
# # print(dir(Jack))
# # print(vars(Jack))
# # print(Jack.__dir__())
# # print(Jack.__dict__)



# #######################################################################
# #Example of class attribute

class Person_with_title:
    TITLES = ('Dr', 'Mr', 'Mrs', 'Ms', 'Prof')
    def __init__(self, title, name, surname, allow_title= TITLES):
        if title not in self.TITLES:
        # if title not in allow_title:
            raise ValueError("%s is not a valid title." %title)
        self.title=title
        self.name = name
        self.surname = surname

# # Dr_Jane = Person_with_title('Prof',"Jane","Doe")
Dr_Jane = Person_with_title('Dr',"Jane","Doe")

#####################################################################
# Example of class attribute

class Person21:
    pets = []
    def add_pet(self, pet):
        self.pets.append(pet)
    def get_pet(self):
        print(self.pets)
        
class Person22:
    # pets=['cat']
    def __init__(self):
        self.pets = []
    def add_pet(self, pet):
        self.pets.append(pet)
    def get_pet(self):
        print(self.pets)
        
jane1 = Person21()
bob1 = Person21()

jane1.add_pet("cat")

print("\n")
print(jane1.pets)
print(bob1.pets) # oops!

bob1.add_pet("dog")
print()
print(jane1.pets)
print(bob1.pets) # oops!

print("\n")


jane2 = Person22()
bob2 = Person22()

jane2.add_pet("cat")
bob2.add_pet("dog")
print(jane2.pets)
print(bob2.pets)

###########################################


class FrozenClass(object):
    __isfrozen = False
    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError( "%r is a frozen class" % self )
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True
        
    def _unfreeze(self):
        self.__isfrozen = False

class Person_FrozenClass(FrozenClass):
    def __init__(self):
        self.name=''
        self.title=''
        self.surname=''
        self._freeze() # no new attributes after this point.
        
        
a = Person_FrozenClass()
print(vars(a))
print(dir(a))
a.aaa='a'

a._FrozenClass__isfrozen=False
a.bbb='b'

a._FrozenClass__isfrozen=True

a.ccc='c'



# ------------------------------------------------------
# Alhamdulillah
# Data Classes
# ------------------------------------------------------

# ----------------------------------- Data Classes -------------------------------------------
# >> a special type of classes used mainly to store, represent, and transfer data.
# >> Provides many advantages, some of them describe below
# >> Resource: https://www.youtube.com/watch?v=HJkY_Bbiqcc
# ------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass

print()
print()

class PersonNormal:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email


class PersonNormalCompleted:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"{self.__class__.__name__}(name = {self.name}, age = {self.age}, email = {self.email})"
    
    def __eq__(self, other):
        return (
            self.name,
            self.age,
            self.email
        ) == (
            other.name,
            other.age,
            other.email
        )


@dataclass
class PersonDataClass:
    name : str
    age  : int
    email: str


# Advantage_1: Pre-implemented __reper__ method
print("Pre-implemented __repr__ method: ")

normal_person = PersonNormal("Ahmed", 20, "ahmed@gmail.com")
normal_person_cmp = PersonNormalCompleted("Ahmed", 20, "ahmed@gmail.com")
datacs_person = PersonDataClass("Ahmed", 20, "ahmed@gmail.com")

print(f"\t>> Normal Class                         : {normal_person}")
print(f"\t>> Normal Class with methods Implemented: {normal_person_cmp}")
print(f"\t>> Data Class                           : {datacs_person}")
print()
print()


# Advantage_2: Pre-implemented __eq__ method for comparison
print("Pre-implemented __eq__ method: ")
normal_person1 = PersonNormal("Ahmed", 20, "ahmed@gmail.com")
normal_person2 = PersonNormal("Ahmed", 20, "ahmed@gmail.com")
print(f"\t>> Normal Class                         : {normal_person1 == normal_person2}") # compare by ID

normal_person_cmp1 = PersonNormalCompleted("Ahmed", 20, "ahmed@gmail.com")
normal_person_cmp2 = PersonNormalCompleted("Ahmed", 20, "ahmed@gmail.com")
print(f"\t>> Normal Class with methods Implemented: {normal_person_cmp1 == normal_person_cmp2}")

datacs_person1 = PersonDataClass("Ahmed", 20, "ahmed@gmail.com")
datacs_person2 = PersonDataClass("Ahmed", 20, "ahmed@gmail.com")
print(f"\t>> Data Class                           : {datacs_person1 == datacs_person2}")
print()
print()


# Agvantage_3: Easy Comparison
from dataclasses import field
@dataclass(order = True) 
class PersonDataClass:
    name : str = field(compare = False)
    age  : int
    email: str = field(compare = False)

persons = [
    PersonDataClass('ahmed', 20, "ahmed@gmail.com"),
    PersonDataClass('mohammedd', 30, "mohammedd@gmail.com"),
    PersonDataClass('mohsen', 10, "mohsen@gmail.com"),
]

print("Sorting: ")
print(f"\t>> ASC : {sorted(persons)}")
print()
print(f"\t>> DESC: {sorted(persons, reverse = True)}")
print()
print()


# Agvantage_4: Freeze the attbs -> cannot change them
@dataclass(frozen = True) 
class PersonDataClass:
    name : str
    age  : int
    email: str

person1 = PersonDataClass("Ahmed", 25, "ahmed@gmail.com")

print("Changing Attbs: ")
try:
    person1.name = "Mohammed"
    print(f"\t>> Success: Person name changed.")
except Exception as e:
    print(f"\t>> Error     : {e}")
    print(f"\t>> Error Type: {type(e)}")

print()
print()
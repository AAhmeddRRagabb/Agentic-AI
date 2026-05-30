# ------------------------------------------------------
# Alhamdulillah
# Type Hints in Python
# ------------------------------------------------------

# ---------------- Type Hints (Type Annotations) -------------------------------------------
# >> a method used to document the variables written in the Python code and improves its readability
# >> Useful for documenting the type of:
#    - arguments passed to a function
#    - return types of a function
#    - API request/response schemas
#    - ...

# >> Resource: https://www.youtube.com/watch?v=QORvB-_mbZ0


## 1. basic type hinting
def func(
    x: list[int], 
    y: list[float],
    t: tuple[int, int, int], # --> a tuple of three integers
    z: tuple[int, ...],      # --> a tuple of any number of integers
) -> dict[str, int]:
    pass

func()



## 2. custom types
Vector = list[int]
Vectors = list[Vector]
def func_2(x: Vector, y: Vectors) -> None:
    pass

func_2()


## 3. special types
from typing import Sequence, Callable
def func_3(
    x: str | None,
    y: Sequence[int],               # --> can be anytype of sequence (list, set, tuple, or string),
    func: Callable[[int, int], int] # --> a func as parameter. It takes two int arguments and return int value
):
    pass



## 4. Generic types
# -> A generic type variable such as T can represent different concrete types, such as str, int, or list[int]. 
# -> However, within the same generic usage or function call, every occurrence of T must refer to the same concrete type.

from typing import TypeVar
T = TypeVar("T")

def func_4(
    x: list[T],
) -> T:
    return x[0]

func_4([1, 2,3])
    
